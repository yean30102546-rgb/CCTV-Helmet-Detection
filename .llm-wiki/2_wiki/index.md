# Second Brain Knowledge Index

[Updated: 2026-07-22]

Welcome to the centralized knowledge index for the **CCTV Helmet Detection Project**.

## Core Architecture & System Design
- [[architecture/cctv-helmet-detection-system.md]]: High-level architecture, RTSP ingestion, OpenVINO CPU acceleration, and notification pipeline.
- [[tech-stack/yolo11-openvino-opencv.md]]: Technology stack specification covering YOLO11n, OpenVINO runtime, OpenCV, Python 3, and LINE Notify.

## System Components
- [[components/model-training-and-export.md]]: YOLO11 model training pipeline (`train_helmet.py`) and OpenVINO conversion script (`export_model.py`).
- [[components/rtsp-cctv-inference-and-notification.md]]: Real-time CCTV stream reader, frame skip optimization, detection logic, and LINE Notify alert mechanism (`run_cctv.py`, `run_images_as_video.py`).

## Lessons Learned & Quality Assurance
- [[lessons-learned/bugs-and-fixes.md]]: Identified bugs, class name mismatch warnings (`no_helmet` vs `no-helmet`), cooldown configuration, and historical fix patterns.

## Audit & Raw Knowledge Management
- `1_raw/` Tier Classification:
  - **Tier A (Active Architecture)**: Synthesized into Wiki structure above.
  - **Tier B (Bug Fixes & Postmortems)**: Recorded in lessons-learned.
  - **Tier C (General Reading & External Docs)**: Retained in `1_raw/` for lazy loading (Mantine, Next.js, UI Glossary, etc.).
  - **[Conflict Note]**: Legacy web app notes in `1_raw/` tagged as deprecated relative to the current Python Computer Vision system.
