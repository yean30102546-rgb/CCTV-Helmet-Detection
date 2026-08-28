# CCTV Helmet Detection System

Automated real-time safety helmet detection system for CCTV streams with OpenVINO CPU acceleration, ByteTrack object tracking, Gemini 2.5 Flash Bounding Box Grounding, Next.js web dashboard, and LINE Notify integration.

## Features
- **YOLO11 Powered**: State-of-the-art object detection model tuned for safety helmet detection.
- **ByteTrack Object Tracking**: Assigns Person IDs to track individuals and eliminate duplicate alert spam.
- **Decoupled Stream Reader**: `VideoStreamReader` runs stream ingestion on a separate thread for fluid 30 FPS playback.
- **Region of Interest (RoI)**: Filter detections within designated polygon zones (`CCTV_ROI`).
- **Gemini AI Grounding & Double-Check**: Verifies unhelmeted detections using Gemini 2.5 Flash, draws non-overlapping orange bounding boxes (`Gemini Verified`), and returns Thai descriptions.
- **Intel OpenVINO Acceleration**: Optimized for high FPS performance on standard CPU hardware.
- **Next.js Web Dashboard**: Real-time web dashboard (`dashboard/`) with true violation counting and evidence gallery.
- **LINE Instant Alerts**: Sends high-priority notification messages with snapshot evidence via background workers with retry policies.
- **Auto Configuration**: Automatic loading of environment variables from `.env`.

## Requirements
- Python 3.9+
- Node.js (for Next.js Dashboard)
- Packages: `ultralytics`, `opencv-python`, `requests`, `openvino`, `google-genai`, `python-dotenv`

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Configure Environment Variables
Edit `.env` in the root directory:
```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
LINE_NOTIFY_TOKEN=YOUR_LINE_NOTIFY_TOKEN
CCTV_SOURCE=0
CCTV_ROI=0.1,0.1;0.9,0.1;0.9,0.9;0.1,0.9
```

### 2. Running Live CCTV Detection
```bash
python run_cctv.py
```

### 3. Running the Next.js Dashboard
Open a new terminal, navigate to `dashboard/`, install Node modules, and start the development server:
```bash
cd dashboard
npm install
npm run dev
```
The dashboard will be available at `http://localhost:3000`.

## Dataset Structure
- `CCTV Helmet Detection.v3i.yolov11/data.yaml`
- Classes: `helmet`, `no_helmet`
