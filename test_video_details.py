import os
import imageio.v3 as iio

video_path = r"c:\Workplace\CCTV project\CCTV raw video\Demo AI CCTV 2.asf"

if not os.path.exists(video_path):
    print(f"Error: Video file not found at {video_path}")
    exit(1)

try:
    print("Reading metadata using imageio with pyav plugin...")
    meta_data = iio.immeta(video_path, plugin="pyav")
    print("Metadata keys:", list(meta_data.keys()))
    fps = meta_data.get('fps', 30.0)
    duration = meta_data.get('duration', 0.0)
    size = meta_data.get('size', (0, 0))
    print(f"FPS: {fps}")
    print(f"Duration: {duration} seconds ({duration / 3600:.2f} hours)")
    print(f"Size: {size}")
except Exception as e:
    print(f"Error reading with imageio (pyav): {e}")

try:
    print("\nTrying to import av directly and read packet info...")
    import av
    container = av.open(video_path)
    print(f"Container format: {container.format}")
    stream = container.streams.video[0]
    print(f"Stream info: codec_context={stream.codec_context.name}, rate={stream.average_rate}, duration={stream.duration}, time_base={stream.time_base}")
    print(f"Stream duration in seconds: {float(stream.duration * stream.time_base) if stream.duration else 'Unknown'}")
except Exception as e:
    print(f"Error using av directly: {e}")
