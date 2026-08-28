import os
import time
import threading
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
EVIDENCE_DIR = os.path.join(DATA_DIR, "evidence")

# Ensure evidence directory exists
if not os.path.exists(EVIDENCE_DIR):
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

def cleanup_old_evidence(days_to_keep=30):
    """
    Deletes evidence images older than specified days to free up disk space.
    """
    print(f"Running evidence cleanup (keeping {days_to_keep} days)...")
    now = time.time()
    cutoff_time = now - (days_to_keep * 86400)
    
    deleted_count = 0
    try:
        for filename in os.listdir(EVIDENCE_DIR):
            if filename.endswith(".jpg"):
                filepath = os.path.join(EVIDENCE_DIR, filename)
                file_mtime = os.path.getmtime(filepath)
                
                if file_mtime < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
                    
        if deleted_count > 0:
            print(f"Cleanup complete. Removed {deleted_count} old evidence files.")
    except Exception as e:
        print(f"Error during evidence cleanup: {e}")

def storage_manager_loop():
    while True:
        # Run cleanup once a day
        cleanup_old_evidence(days_to_keep=30)
        # Sleep for 24 hours
        time.sleep(86400)

def start_storage_manager():
    worker_thread = threading.Thread(target=storage_manager_loop, daemon=True)
    worker_thread.start()
    return worker_thread

def get_evidence_path(timestamp):
    return os.path.join(EVIDENCE_DIR, f"evidence_{timestamp}.jpg")
