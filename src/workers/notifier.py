import os
import time
import requests
import threading
from datetime import datetime
from src.db.database import get_unbatched_detections, mark_as_batched

# Use env var or default for testing
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN", "YOUR_LINE_NOTIFY_TOKEN_HERE")

def send_line_notify(message, image_path=None):
    if not LINE_NOTIFY_TOKEN or LINE_NOTIFY_TOKEN == "YOUR_LINE_NOTIFY_TOKEN_HERE":
        print("LINE Notify Token is not set. Skipping notification.")
        return False

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    payload = {"message": message}
    
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as file:
                files = {"imageFile": file}
                response = requests.post(url, headers=headers, data=payload, files=files)
        else:
            response = requests.post(url, headers=headers, data=payload)
            
        if response.status_code == 200:
            print("LINE notification sent successfully.")
            return True
        else:
            print(f"Failed to send LINE notification. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending LINE Notify: {e}")
        return False

def notifier_loop():
    print("LINE Batch Notifier started.")
    # Check every 5 minutes (300 seconds)
    check_interval = 300 
    
    while True:
        try:
            # Fetch unbatched detections that are confirmed (by YOLO or Gemini)
            unbatched_records = get_unbatched_detections()
            
            if unbatched_records:
                count = len(unbatched_records)
                
                # Create a summary message
                now_str = datetime.now().strftime("%H:%M")
                message = f"\n⚠️ [สรุปยอดล่าสุดเวลา {now_str}]\nตรวจพบพนักงานไม่สวมหมวกนิรภัยจำนวน {count} รายการ"
                
                # Pick the image from the record with the highest confidence as a representative image
                best_record = max(unbatched_records, key=lambda x: x['confidence'])
                representative_image = best_record['image_path']
                
                # Send the notification
                sent_success = send_line_notify(message, image_path=representative_image)
                
                if sent_success:
                    # Mark these records as batched only on successful send
                    record_ids = [r['id'] for r in unbatched_records]
                    mark_as_batched(record_ids)
                    print(f"Batched {count} detections for LINE notification.")
                else:
                    print(f"LINE notification failed. Will retry batch of {count} detections on next check.")
                
        except Exception as e:
            print(f"Error in LINE notifier worker: {e}")
            
        # Wait for next batch interval
        time.sleep(check_interval)

def start_notifier():
    worker_thread = threading.Thread(target=notifier_loop, daemon=True)
    worker_thread.start()
    return worker_thread
