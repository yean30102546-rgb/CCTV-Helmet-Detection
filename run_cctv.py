import time
import cv2
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file automatically
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

# Ensure src modules can be imported
sys.path.append(base_dir)

import numpy as np
from concurrent.futures import ThreadPoolExecutor
from ultralytics import YOLO
from src.db.database import init_db, insert_detection
from src.workers.gemini_worker import start_gemini_worker, stop_gemini_worker, gemini_task_queue
from src.utils.storage_manager import start_storage_manager, get_evidence_path
from src.workers.notifier import start_notifier
from src.utils.stream_reader import VideoStreamReader

def parse_roi(roi_str, frame_w, frame_h):
    """
    Parse normalized ROI coordinates string e.g. "0.1,0.1;0.9,0.1;0.9,0.9;0.1,0.9"
    Default to full frame if not specified or invalid.
    """
    if not roi_str:
        return np.array([[0, 0], [frame_w - 1, 0], [frame_w - 1, frame_h - 1], [0, frame_h - 1]], np.int32)
    try:
        pts = []
        for pt in roi_str.split(";"):
            x, y = map(float, pt.split(","))
            pts.append([int(x * frame_w), int(y * frame_h)])
        return np.array(pts, np.int32)
    except Exception as e:
        print(f"Error parsing CCTV_ROI ({roi_str}): {e}. Fallback to full frame.")
        return np.array([[0, 0], [frame_w - 1, 0], [frame_w - 1, frame_h - 1], [0, frame_h - 1]], np.int32)

def is_center_in_roi(box, roi_poly):
    """
    Check if the center point of a bounding box lies inside the RoI polygon.
    """
    x1, y1, x2, y2 = map(float, box.xyxy[0])
    cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
    return cv2.pointPolygonTest(roi_poly, (cx, cy), False) >= 0, (cx, cy)

def main():
    # 0. Initialize System
    print("Initializing Database...")
    init_db()
    
    print("Starting Background Workers...")
    start_storage_manager()
    start_gemini_worker()
    start_notifier()

    # Async image writer thread pool (P1.2)
    image_writer_pool = ThreadPoolExecutor(max_workers=2)

    # 1. Load Model
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "helmet_training_results", "weights", "best_openvino_model")
    
    if not os.path.exists(model_path):
        print(f"WARNING: OpenVINO model not found at {model_path}.")
        model_path = os.path.join(base_dir, "helmet_training_results", "weights", "best.pt")
        if not os.path.exists(model_path):
            model_path = "yolo11n.pt"

    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # 2. Camera Setup with Decoupled Stream Reader (P1.1)
    cctv_source = os.getenv("CCTV_SOURCE", "0")
    rtsp_url = int(cctv_source) if cctv_source.isdigit() else cctv_source
    print(f"Connecting to CCTV stream (Decoupled Reader): {rtsp_url}")
    
    stream = VideoStreamReader(rtsp_url).start()
    time.sleep(1.0) # Warm up camera

    if not stream.is_opened():
        print("Error: Could not open video stream.")
        return

    frame_count = 0
    process_every_n_frames = 2
    
    alerted_track_ids = set()
    track_history_timestamps = {}
    TRACK_MEMORY_TIMEOUT = 300  # 5 minutes memory timeout

    cctv_roi_env = os.getenv("CCTV_ROI", None)
    roi_polygon = None

    print("Starting Inference... Press 'q' to stop.")
    prev_time = time.time()

    try:
        while True:
            success, frame = stream.read()
            if not success or frame is None:
                time.sleep(0.01)
                continue

            frame_count += 1
            annotated_frame = frame
            frame_h, frame_w = frame.shape[:2]

            if roi_polygon is None:
                roi_polygon = parse_roi(cctv_roi_env, frame_w, frame_h)

            if frame_count % process_every_n_frames == 0:
                results = model.track(frame, conf=0.2, persist=True, tracker="bytetrack.yaml", device="cpu", verbose=False)
                annotated_frame = results[0].plot()
                
                current_time = time.time()
                
                # Cleanup expired track history (older than 5 minutes)
                expired_ids = [tid for tid, t in track_history_timestamps.items() if current_time - t > TRACK_MEMORY_TIMEOUT]
                for tid in expired_ids:
                    alerted_track_ids.discard(tid)
                    del track_history_timestamps[tid]

                if results[0].boxes is not None and results[0].boxes.id is not None:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    for box, track_id in zip(results[0].boxes, track_ids):
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf = float(box.conf[0])
                        
                        track_history_timestamps[track_id] = current_time

                        if class_name in ["no_helmet", "no-helmet", "Without Helmet"]:
                            # RoI Check (P2.1)
                            in_roi, (cx, cy) = is_center_in_roi(box, roi_polygon)
                            if not in_roi:
                                continue # Ignore detections outside RoI

                            if track_id not in alerted_track_ids and conf >= 0.4:
                                timestamp = int(current_time)
                                evidence_path = get_evidence_path(f"{timestamp}_id{track_id}")
                                
                                # Async image writing (P1.2)
                                image_writer_pool.submit(cv2.imwrite, evidence_path, annotated_frame.copy())

                                if conf > 0.8:
                                    print(f"High Confidence ({conf:.2f}) for Person ID #{track_id}: Logged as CONFIRMED_BY_YOLO")
                                    insert_detection(evidence_path, conf, "CONFIRMED_BY_YOLO")
                                else:
                                    print(f"Medium Confidence ({conf:.2f}) for Person ID #{track_id}: Sent to Gemini for verification")
                                    detection_id = insert_detection(evidence_path, conf, "PENDING_GEMINI")
                                    
                                    # Collect YOLO boxes for overlap checking in Gemini worker
                                    yolo_boxes = []
                                    if results[0].boxes is not None:
                                        for b in results[0].boxes:
                                            yolo_boxes.append(b.xyxy[0].cpu().tolist())

                                    gemini_task_queue.put({
                                        "detection_id": detection_id,
                                        "image_path": evidence_path,
                                        "yolo_boxes": yolo_boxes
                                    })
                                
                                alerted_track_ids.add(track_id)

            # Draw RoI Polygon on frame (P2.1 Visualization)
            if roi_polygon is not None:
                cv2.polylines(annotated_frame, [roi_polygon], isClosed=True, color=(0, 255, 255), thickness=2)
                cv2.putText(annotated_frame, "Monitoring Zone (RoI)", (roi_polygon[0][0] + 5, roi_polygon[0][1] + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # FPS calculation
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            try:
                cv2.imshow("CCTV Helmet Detection", annotated_frame)
            except cv2.error:
                # GUI not supported, ignore (e.g. headless env)
                pass

            try:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except cv2.error:
                # Fallback for headless environments
                time.sleep(0.03) # ~30 fps delay
                
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Cleaning up...")
        stream.stop()
        image_writer_pool.shutdown(wait=False)
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass
        stop_gemini_worker()
        print("Stream closed.")

if __name__ == '__main__':
    main()
