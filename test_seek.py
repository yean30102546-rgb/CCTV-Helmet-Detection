import av
import cv2
import time
import os

video_path = r"c:\Workplace\CCTV project\CCTV raw video\Demo AI CCTV 2.asf"
output_dir = r"c:\Workplace\CCTV project\dataset_frames"
os.makedirs(output_dir, exist_ok=True)

container = av.open(video_path)
stream = container.streams.video[0]
time_base_val = float(stream.time_base)

target_sec = 3600
pts_target = int(target_sec / time_base_val)

print(f"Seeking to {target_sec} seconds...")
container.seek(pts_target, stream=stream)

for frame in container.decode(stream):
    if frame.pts >= pts_target:
        # Convert frame to numpy array for OpenCV (BGR format)
        img = frame.to_ndarray(format='bgr24')
        output_path = os.path.join(output_dir, "test_seek_frame.jpg")
        cv2.imwrite(output_path, img)
        print(f"Successfully saved frame to {output_path}")
        break

container.close()
