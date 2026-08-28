# Tech Stack: YOLO11, OpenVINO & OpenCV

[Updated: 2026-07-21]

## 1. Summary
The technology stack is tailored for real-time computer vision inference on CPU edge devices without requiring dedicated Nvidia GPUs.

## 2. Component Breakdown

| Component | Library / Tool | Version / Spec | Primary Role |
| :--- | :--- | :--- | :--- |
| **Object Detection Model** | Ultralytics YOLO | YOLO11n (`yolo11n.pt`) | Light weight object detection architecture tuned for speed & accuracy |
| **CPU Acceleration Engine** | Intel OpenVINO | OpenVINO IR (`best_openvino_model`) | Optimizes PyTorch graphs for Intel i5/i7 x86 CPU instructions |
| **Stream Processing & Display** | OpenCV | `opencv-python` (`cv2`) | Video stream ingestion (RTSP/Webcam), image IO, FPS computation, GUI rendering |
| **HTTP Notifications** | Requests | `requests` | Multipart form-data upload of evidence snapshots to LINE Notify API |
| **Dataset & Annotations** | Roboflow Format | YOLOv11 Format (`data.yaml`) | 2 classes: `helmet`, `no_helmet` |

## 3. Dependencies (`requirements.txt`)
- `ultralytics`
- `opencv-python`
- `requests`
- `openvino` (for OpenVINO export & runtime)

## 4. Knowledge Relationships
- Related Architecture: [[architecture/cctv-helmet-detection-system.md]]
- Training & Export: [[components/model-training-and-export.md]]
