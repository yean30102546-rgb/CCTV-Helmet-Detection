# Architecture: CCTV Helmet Detection System

[Updated: 2026-07-21]

## 1. Summary
The CCTV Helmet Detection system is an edge-optimized computer vision application built to detect whether individuals captured by CCTV cameras are wearing safety helmets. The system utilizes YOLO11n optimized via Intel OpenVINO for high-speed inference on CPU hardware (e.g. Intel Core i5), paired with OpenCV for stream decoding/visualization and LINE Notify API for real-time alerting with image evidence.

## 2. System Architecture & Data Flow

```text
[ RTSP CCTV Stream / Webcam (cv2.VideoCapture) ]
                       │
                       ▼
         [ Frame Skipping (every 2nd frame) ]
                       │
                       ▼
       [ OpenVINO Inference Engine (YOLO11n) ]
                       │
                       ▼
   [ Class Check: 'helmet' vs 'no_helmet' (conf >= 0.5) ]
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
    [ Helmet Detected ]   [ No Helmet Detected ]
             │                   │
             │           [ Cooldown Check (> 10s) ]
             │                   │
             │                   ▼
             │         [ Save evidence image ]
             │                   │
             │                   ▼
             │       [ LINE Notify API Alert ]
             └─────────┬─────────┘
                       ▼
       [ OpenCV Window Display & FPS Counter ]
```

## 3. Core Subsystems

1. **Model Pipeline**:
   - Base weights trained on custom Roboflow dataset (`CCTV Helmet Detection.v3i.yolov11`).
   - Exported from PyTorch `.pt` to OpenVINO IR format (`best_openvino_model`) for CPU hardware acceleration.

2. **Inference & Stream Manager (`run_cctv.py`)**:
   - Captures RTSP video stream via `cv2.VideoCapture`.
   - Implements frame-skipping (`process_every_n_frames = 2`) to maintain high throughput on limited CPU resources.
   - Computes real-time FPS overlay on bounding-box-annotated frame (`results[0].plot()`).

3. **Notification & Evidence Handler**:
   - Triggers when `no_helmet` class is detected with confidence threshold.
   - Enforces a 10-second alert cooldown (`alert_cooldown_seconds = 10`) to prevent notification flooding.
   - Writes snapshot `evidence_<timestamp>.jpg` and posts payload via HTTP POST to `https://notify-api.line.me/api/notify`.

## 4. Knowledge Relationships
- Depends On: [[tech-stack/yolo11-openvino-opencv.md]], [[components/model-training-and-export.md]]
- Related Components: [[components/rtsp-cctv-inference-and-notification.md]]
- Known Bugs / Mismatches: [[lessons-learned/bugs-and-fixes.md]]
