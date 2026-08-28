# Component: RTSP CCTV Inference & Notification

[Updated: 2026-07-21]

## 1. Summary
Handles live stream decoding, inference execution, bounding box plotting, evidence image snapshot generation, and LINE Notify delivery.

## 2. Key Modules & Scripts

### Live CCTV Processing (`run_cctv.py`)
- **Model Fallback Logic**:
  1. `helmet_training_results/weights/best_openvino_model` (Primary)
  2. `helmet_training_results/weights/best.pt` (Fallback 1)
  3. `yolo11n.pt` (Fallback 2)
- **Stream URL**: RTSP string or device index `0` (webcam).
- **Inference Config**: `conf=0.5`, `device="cpu"`, `process_every_n_frames=2`.
- **Alert Logic**:
  - Checks if detected box class name matches `no-helmet` or `Without Helmet` (Note: See [[lessons-learned/bugs-and-fixes.md]] regarding `no_helmet` string discrepancy).
  - Enforces `alert_cooldown_seconds = 10`.
  - Saves frame to `evidence_<timestamp>.jpg`.
  - Calls `send_line_notify(message, image_path)`.

### Test Image Simulation (`run_images_as_video.py`)
- Simulates real-time stream using test dataset directory `CCTV Helmet Detection.v3i.yolov11/test/images/*.jpg`.
- Runs inference at target 15 FPS simulation rate with `conf=0.4`.

## 3. Knowledge Relationships
- Architecture: [[architecture/cctv-helmet-detection-system.md]]
- Model Provider: [[components/model-training-and-export.md]]
- Critical Bug Note: [[lessons-learned/bugs-and-fixes.md]]
