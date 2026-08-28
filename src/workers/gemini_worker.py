import os
import time
import queue
import threading
import json
import re
import cv2
from google import genai
from google.genai import types
from src.db.database import update_detection_status, get_pending_gemini_detections

# Queue for passing tasks from main CCTV thread to Gemini worker
gemini_task_queue = queue.Queue()

def compute_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) of two boxes [x1, y1, x2, y2].
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter_w = max(0, x2 - x1)
    inter_h = max(0, y2 - y1)
    inter_area = inter_w * inter_h
    
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    union_area = area1 + area2 - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area

def draw_gemini_boxes(image_path, boxes, yolo_boxes=None):
    """
    Draw orange bounding boxes (BGR: 0, 140, 255) for Gemini verified unhelmeted persons
    ONLY if they do not overlap significantly with existing YOLO boxes (IoU < 0.3).
    boxes format expected: [[ymin, xmin, ymax, xmax]] normalized 0..1000 or 0..1.
    """
    if not boxes or not os.path.exists(image_path):
        return
    
    img = cv2.imread(image_path)
    if img is None:
        return
        
    h, w = img.shape[:2]
    drawn_count = 0
    
    for idx, box in enumerate(boxes):
        if not isinstance(box, (list, tuple)) or len(box) != 4:
            continue
        ymin, xmin, ymax, xmax = box
        
        # Normalize coordinates if given in 0..1000 range
        if ymin > 1.0 or xmin > 1.0 or ymax > 1.0 or xmax > 1.0:
            ymin, xmin, ymax, xmax = ymin / 1000.0, xmin / 1000.0, ymax / 1000.0, xmax / 1000.0
            
        x1 = max(0, int(xmin * w))
        y1 = max(0, int(ymin * h))
        x2 = min(w, int(xmax * w))
        y2 = min(h, int(ymax * h))
        
        g_box = [x1, y1, x2, y2]
        
        # Check overlap with existing YOLO boxes
        overlaps = False
        if yolo_boxes:
            for y_box in yolo_boxes:
                if compute_iou(g_box, y_box) > 0.3:
                    overlaps = True
                    break
                    
        if overlaps:
            print(f"Gemini box [{x1},{y1},{x2},{y2}] overlaps with existing YOLO box. Skipping drawing to avoid duplicate box.")
            continue
            
        drawn_count += 1
        orange_color = (0, 140, 255) # BGR: Orange
        cv2.rectangle(img, (x1, y1), (x2, y2), orange_color, 2)
        
        label = f"Gemini Verified #{drawn_count}"
        cv2.putText(img, label, (x1, max(y1 - 5, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, orange_color, 2)
        
    cv2.imwrite(image_path, img)

def recover_pending_tasks():
    try:
        pending_records = get_pending_gemini_detections()
        if pending_records:
            print(f"Recovered {len(pending_records)} pending Gemini verification tasks from database.")
            for record in pending_records:
                gemini_task_queue.put({
                    "detection_id": record["id"],
                    "image_path": record["image_path"]
                })
    except Exception as e:
        print(f"Error recovering pending Gemini tasks: {e}")

def gemini_worker_loop():
    print("Gemini Background Worker started.")
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found. Gemini verification will fallback to YOLO confirmation.")
    else:
        client = genai.Client()

    # Recover any unverified tasks from previous run
    recover_pending_tasks()
        
    while True:
        try:
            # Block until an item is available
            task = gemini_task_queue.get(block=True)
            
            # If we receive a None task, it's a signal to exit
            if task is None:
                print("Gemini Background Worker stopping.")
                gemini_task_queue.task_done()
                break
                
            detection_id = task.get("detection_id")
            image_path = task.get("image_path")
            yolo_boxes = task.get("yolo_boxes", None)
            
            if not api_key:
                # Offline fallback
                print(f"Fallback: Auto-confirming detection {detection_id} (No API key)")
                update_detection_status(detection_id, "CONFIRMED_BY_YOLO", violation_count=1)
                gemini_task_queue.task_done()
                continue
                
            # Wait briefly if image is still being written by AsyncImageWriter thread pool
            wait_count = 0
            while not os.path.exists(image_path) and wait_count < 20:
                time.sleep(0.1)
                wait_count += 1
                
            if not os.path.exists(image_path):
                print(f"Error: Image {image_path} not found for Gemini verification.")
                update_detection_status(detection_id, "REJECTED", "Error: Image file not found", violation_count=0)
                gemini_task_queue.task_done()
                continue
                
            max_retries = 3
            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    # Upload file to Gemini
                    print(f"Sending image {image_path} to Gemini for verification (Attempt {attempt}/{max_retries})...")
                    file = client.files.upload(file=image_path)
                    
                    prompt = (
                        "Locate all persons in this image who are NOT wearing a safety helmet (hard hat). "
                        "Return your response ONLY as a JSON object with the following keys:\n"
                        "1. 'has_violation': boolean (true if someone is not wearing a helmet, false otherwise)\n"
                        "2. 'violation_count': integer (count of people not wearing helmets)\n"
                        "3. 'boxes': array of bounding boxes for each person without a helmet, formatted as [ymin, xmin, ymax, xmax] on a 0-1000 scale.\n"
                        "4. 'description_th': concise string description of the violation(s) in Thai (ภาษาไทย).\n"
                        "Example format: {\"has_violation\": true, \"violation_count\": 2, \"boxes\": [[200, 100, 500, 400]], \"description_th\": \"พบพนักงาน 2 คนไม่สวมหมวกนิรภัย...\"}"
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[file, prompt]
                    )
                    
                    reply = response.text.strip()
                    print(f"Gemini response for {detection_id}: {reply[:60]}...")
                    
                    # Parse JSON response
                    json_match = re.search(r"\{.*\}", reply, re.DOTALL)
                    if json_match:
                        try:
                            parsed_data = json.loads(json_match.group(0))
                            has_violation = parsed_data.get("has_violation", False)
                            boxes = parsed_data.get("boxes", [])
                            v_count = int(parsed_data.get("violation_count", len(boxes) if boxes else (1 if has_violation else 0)))
                            description_th = parsed_data.get("description_th", reply)
                            
                            if has_violation:
                                status = "CONFIRMED_BY_GEMINI"
                                # Draw orange boxes for Gemini groundings if no overlap with YOLO
                                if boxes:
                                    draw_gemini_boxes(image_path, boxes, yolo_boxes=yolo_boxes)
                            else:
                                status = "REJECTED"
                                v_count = 0
                                
                            update_detection_status(detection_id, status, description_th, violation_count=v_count)
                        except Exception as json_err:
                            print(f"JSON Parsing Warning for {detection_id}: {json_err}. Using plain text parsing.")
                            status = "CONFIRMED_BY_GEMINI" if "true" in reply.lower() or "yes" in reply.lower() else "REJECTED"
                            update_detection_status(detection_id, status, reply, violation_count=1 if status == "CONFIRMED_BY_GEMINI" else 0)
                    else:
                        status = "CONFIRMED_BY_GEMINI" if "true" in reply.lower() or "yes" in reply.lower() else "REJECTED"
                        update_detection_status(detection_id, status, reply, violation_count=1 if status == "CONFIRMED_BY_GEMINI" else 0)

                    success = True
                    break
                    
                except Exception as e:
                    print(f"Gemini API Error (Attempt {attempt}/{max_retries}) for detection {detection_id}: {e}")
                    if attempt < max_retries:
                        time.sleep(2 ** attempt) # Exponential backoff
            
            if not success:
                print(f"Gemini verification failed after {max_retries} attempts for detection {detection_id}. Fallback to YOLO.")
                update_detection_status(detection_id, "CONFIRMED_BY_YOLO", "Gemini API Timeout/Error. Fallback to YOLO.", violation_count=1)
                
            # Mark task as done
            gemini_task_queue.task_done()
            
        except Exception as e:
            print(f"Unexpected error in Gemini worker: {e}")
            time.sleep(1) # Prevent tight loop on unexpected errors

def start_gemini_worker():
    worker_thread = threading.Thread(target=gemini_worker_loop, daemon=True)
    worker_thread.start()
    return worker_thread

def stop_gemini_worker():
    gemini_task_queue.put(None)
