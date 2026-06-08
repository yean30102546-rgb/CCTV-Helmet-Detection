import os
import av
import cv2
import time

def extract_frames_by_schedule(video_path, output_dir):
    """
    Extract frames from a video at specific hour intervals using fast PyAV seeking.
    
    Schedule:
    - Hour 1: Start at 0s, extract 500 frames, every 10s.
    - Hour 2: Start at 3600s (1h), extract 500 frames, every 10s.
    - Hour 3: Start at 7200s (2h), extract 500 frames, every 10s.
    - Hour 4: Start at 10800s (3h), extract 250 frames, every 10s.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(video_path):
        print(f"Error: Could not find video file at {video_path}")
        return

    print(f"Opening video file: {video_path}")
    container = av.open(video_path)
    stream = container.streams.video[0]
    time_base_val = float(stream.time_base)
    
    # Calculate video duration
    duration_sec = float(stream.duration * time_base_val) if stream.duration else 0.0
    print(f"Video Duration: {duration_sec:.2f} seconds ({duration_sec / 3600:.2f} hours)")
    print(f"Time Base: {stream.time_base}")
    
    # Extraction schedule
    schedule = [
        {"hour": 1, "start_sec": 0, "count": 500, "interval_sec": 10},
        {"hour": 2, "start_sec": 3600, "count": 500, "interval_sec": 10},
        {"hour": 3, "start_sec": 7200, "count": 500, "interval_sec": 10},
        {"hour": 4, "start_sec": 10800, "count": 250, "interval_sec": 10},
    ]
    
    total_expected_frames = sum(item["count"] for item in schedule)
    total_saved_count = 0
    start_time = time.time()
    
    print(f"Starting scheduled frame extraction. Target: {total_expected_frames} frames.\n")
    
    for config in schedule:
        hour = config["hour"]
        start_sec = config["start_sec"]
        count = config["count"]
        interval_sec = config["interval_sec"]
        
        print(f"--- Processing Hour {hour} (Start: {start_sec}s, Target: {count} frames, Every {interval_sec}s) ---")
        
        hour_saved_count = 0
        for i in range(count):
            target_sec = start_sec + (i * interval_sec)
            
            # Stop if target exceeds video duration
            if duration_sec > 0 and target_sec > duration_sec:
                print(f"Warning: Target time {target_sec}s exceeds video duration {duration_sec:.2f}s. Stopping Hour {hour} early.")
                break
                
            pts_target = int(target_sec / time_base_val)
            
            # Seek to keyframe before target_sec
            container.seek(pts_target, stream=stream)
            
            # Decode frames until we find the exact/nearest frame >= target_sec
            frame_found = False
            for frame in container.decode(stream):
                if frame.pts >= pts_target:
                    # Convert to BGR for OpenCV
                    img = frame.to_ndarray(format='bgr24')
                    
                    # Create clear filename containing hour, frame index, and actual timestamp
                    filename = f"hour{hour}_frame_{i:03d}_{target_sec:05d}s.jpg"
                    output_path = os.path.join(output_dir, filename)
                    
                    cv2.imwrite(output_path, img)
                    hour_saved_count += 1
                    total_saved_count += 1
                    frame_found = True
                    break
            
            if not frame_found:
                print(f"Warning: Could not decode frame at target time {target_sec}s")
                
            # Print progress every 50 frames within the hour
            if (i + 1) % 50 == 0 or (i + 1) == count:
                elapsed = time.time() - start_time
                avg_time_per_frame = elapsed / total_saved_count if total_saved_count > 0 else 0
                est_remaining = (total_expected_frames - total_saved_count) * avg_time_per_frame
                print(f"Progress: Hour {hour} -> {i + 1}/{count} frames processed. "
                      f"Total saved: {total_saved_count}. "
                      f"Elapsed: {elapsed:.1f}s. Est. remaining: {est_remaining:.1f}s.")
        
        print(f"Completed Hour {hour}: Saved {hour_saved_count} frames.\n")
        
    container.close()
    
    total_elapsed = time.time() - start_time
    print("=" * 50)
    print(f"Extraction Completed!")
    print(f"Total Frames Saved: {total_saved_count} / {total_expected_frames}")
    print(f"Total Time Taken: {total_elapsed:.2f} seconds ({total_elapsed / 60:.2f} minutes)")
    print(f"Average Speed: {total_elapsed / total_saved_count:.4f} seconds per frame")
    print(f"Frames saved in: {output_dir}")
    print("=" * 50)

if __name__ == "__main__":
    VIDEO_PATH = r"c:\Workplace\CCTV project\CCTV raw video\Demo AI CCTV 2.asf"
    OUTPUT_DIR = r"c:\Workplace\CCTV project\dataset_frames"
    
    extract_frames_by_schedule(VIDEO_PATH, OUTPUT_DIR)
