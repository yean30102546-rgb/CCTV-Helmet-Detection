# Technical Context: CCTV Helmet Detection Project

[Updated: 2026-07-22]

## 1. Executive Summary
The **CCTV Helmet Detection System** is an automated computer vision solution designed to detect non-compliance with safety helmet regulations from real-time CCTV camera streams (RTSP / webcam). It incorporates Edge AI (YOLO11 + ByteTrack) for fast inference and person tracking, OpenVINO CPU acceleration, Region of Interest (RoI) filtering, and Cloud AI (Gemini 2.5 Flash) for secondary JSON bounding box verification. Verified violations are logged into an SQLite database, accessible via a Next.js web dashboard with true violation counting, and instant alerts are pushed to LINE Notify.

## 2. Technical Architecture & Tech Stack
- **Language**: Python 3.x (Backend), TypeScript (Frontend)
- **Computer Vision & Inference**:
  - **Ultralytics YOLO11**: Nano architecture (`yolo11n.pt`) fine-tuned on helmet dataset.
  - **ByteTrack**: Object tracking algorithm (`model.track`) for assigning Person IDs and deduplicating alerts.
  - **Intel OpenVINO IR**: Graph-optimized model format for CPU hardware acceleration.
  - **`VideoStreamReader` (`src/utils/stream_reader.py`)**: Decoupled non-blocking video stream ingestion on a separate thread.
  - **`ThreadPoolExecutor`**: Async image file writing to prevent disk I/O latency in main AI loop.
  - **Region of Interest (RoI)**: Polygon zone filtering (`is_center_in_roi`) and yellow overlay drawing (`cv2.polylines`).
- **Verification & Data Management**:
  - **Google Gemini API**: `gemini-2.5-flash` for multi-modal double-checking, returning JSON bounding boxes (`[ymin, xmin, ymax, xmax]`), violation count, and Thai descriptions.
  - **IoU Overlap Filter**: Calculates IoU between Gemini boxes and YOLO boxes (`compute_iou > 0.3`) to draw orange bounding boxes (`Gemini Verified #N`) only on unhelmeted persons missed by YOLO.
  - **SQLite3**: Local database (`cctv_helmet_data.db`) storing detection metadata, `violation_count`, and AI responses with auto-migration.
  - **Auto Configuration**: Uses `python-dotenv` to load `.env` settings automatically.
  - **Next.js 15 (App Router)**: Tailwind v4 frontend web dashboard to monitor violations, view true violation counts, and track verification states.
- **Alert System**:
  - **LINE Notify API**: HTTP POST with image attachments.
  - **Retry & Recovery**: Exponential backoff for Gemini worker, unbatched status persistence check for LINE worker.

## 3. Data & Class Models
- Dataset Format: Roboflow YOLOv11 Format
- Classes (`data.yaml`): Index 0: `helmet`, Index 1: `no_helmet`
- **Database Schema (`detections` table)**:
  - `id`, `timestamp`, `image_path`, `confidence`, `status` (`CONFIRMED_BY_YOLO`, `CONFIRMED_BY_GEMINI`, `PENDING_GEMINI`, `REJECTED`), `gemini_description`, `is_batched`, `violation_count`.

## 4. Key Scripts & Execution Entry Points
1. `run_cctv.py`: Main backend service initiating background workers (Database, Storage, Gemini, LINE Notifier), `VideoStreamReader`, and OpenVINO ByteTrack inference.
2. `dashboard/`: Next.js web interface (run via `npm run dev`) providing real-time UI.
3. `train_helmet.py` / `export_model.py`: Model training and optimization.

## 5. Technical Glossary
- **RTSP**: Real-Time Streaming Protocol for CCTV cameras.
- **OpenVINO**: Intel Open Visual Inference optimization toolkit.
- **ByteTrack**: Low-latency multi-object tracking algorithm.
- **IoU**: Intersection over Union metric for bounding box overlap calculation.
- **RoI**: Region of Interest polygon zone filtering.
