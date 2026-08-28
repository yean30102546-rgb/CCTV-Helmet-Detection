# User Operational Guide: CCTV Helmet Detection

[Updated: 2026-07-22]

## Overview
This guide provides step-by-step instructions for operators deploying and monitoring the CCTV Helmet Detection system.

## Operational Steps

### 1. Setting Up Environment Variables (.env)
1. Open `.env` in the root directory.
2. Fill in your keys and configuration:
   ```env
   GEMINI_API_KEY="your_gemini_api_key"
   LINE_NOTIFY_TOKEN="your_line_notify_token"
   CCTV_SOURCE="path_to_video_or_rtsp_url"
   CCTV_ROI="0.1,0.1;0.9,0.1;0.9,0.9;0.1,0.9"
   ```

### 2. Setting Up the Web Dashboard
1. Ensure Node.js is installed.
2. Open a terminal and navigate to the `dashboard/` directory.
3. Run `npm install` followed by `npm run dev`.
4. Open `http://localhost:3000` in your browser. The dashboard will auto-refresh as new detections arrive with true violation counts.

### 3. Connecting to CCTV Cameras
1. Obtain the RTSP URL from your IP Camera administrator (e.g. `rtsp://admin:password@192.168.1.50:554/stream1`).
2. Alternatively, set a local video file (ASF/MP4) or set `0` for USB webcam in `CCTV_SOURCE`.

### 4. Monitoring & Controlling Live Stream
- Execute `python run_cctv.py` in your terminal.
- View the real-time window showing detected bounding boxes, Person IDs (`#1`, `#2`), RoI Monitoring Zone, and FPS.
- Monitor verified violations on the Web Dashboard at `http://localhost:3000`.
- Press key **`q`** on your keyboard while focusing on the video window to cleanly shut down the stream.

### 5. Adjusting Alert Frequency & Sensitivity
- **Confidence Threshold**: Change `conf=0.2` in `model.track(...)` higher or lower.
- **Tracking Memory Timeout**: Change `TRACK_MEMORY_TIMEOUT = 300` in `run_cctv.py` to adjust how long Person IDs are remembered before clearing memory.
