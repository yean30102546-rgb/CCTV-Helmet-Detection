# Glossary

- **Inference Server**: A local edge device or server within the factory responsible for real-time processing of camera feeds to trigger alarms.
- **Video Source**: IP Cameras providing real-time RTSP streams for the Inference Server in production.
- **Raw Video**: Pre-recorded video files used for extracting training data.
- **Frame Extraction**: The process of generating dataset images from Raw Video. Settled on **Time-based Sampling** due to continuous foot traffic in the footage.
- **Annotation Classes**: Defined as exactly 2 classes: `helmet` (head with hard hat) and `no_helmet` (bare head). This ensures faster annotation and direct alarm triggers upon detecting `no_helmet`.
- **Model Architecture**: **YOLO** (e.g., YOLOv8 or YOLO11) chosen for high inference speed to enable real-time detection without requiring expensive GPU hardware.
- **Alarm System**: **Message Notification via LINE Notify**. When the `no_helmet` class is detected, the system will capture a snapshot and send an immediate alert with the image to a designated LINE group.
- **Alert Throttling**: **Cooldown Timer**. To prevent spamming the LINE group, the system will implement a cooldown period (e.g., 1-2 minutes) after each alert, during which no new alerts will be sent even if the violation persists.
