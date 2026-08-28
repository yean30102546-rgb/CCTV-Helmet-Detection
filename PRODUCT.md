# Product Definition & Scope: CCTV Helmet Detection

[Updated: 2026-07-22]

## Product Vision
An intelligent, low-cost safety enforcement solution that automates helmet compliance monitoring across industrial sites, construction areas, and public roadways using existing CCTV infrastructure. It features ByteTrack Person ID tracking, Region of Interest (RoI) filtering, Gemini 2.5 Flash Bounding Box Grounding, and a real-time web dashboard for evidence review.

## Target Audience & Stakeholders
- **Industrial & Construction Safety Officers**: Require automated real-time monitoring, true violation counts, and evidence logging for safety compliance via a user-friendly dashboard.
- **Facility Security Managers**: Need instant mobile alerts when unauthorized / unhelmeted personnel enter restricted areas.
- **Operations Team**: Require low hardware overhead without requiring expensive multi-GPU servers.

## Product Capabilities & Scope
- **Scope Included**:
  - Fine-tuned YOLO11 object detection for safety helmets (`helmet`, `no_helmet`).
  - ByteTrack Person ID tracking & alert deduplication.
  - OpenVINO model compilation for Intel CPU execution.
  - Decoupled Video Stream Ingestion (`VideoStreamReader`) & Async Image File Writing.
  - Region of Interest (RoI) polygon zone filtering & overlay rendering.
  - Multi-source video input support (RTSP CCTV stream, USB Webcam, Dataset image folder simulation).
  - Cloud AI Verification & Grounding (Gemini 2.5 Flash JSON Bounding Boxes + Thai descriptions).
  - Snapshot evidence capturing, orange bounding box overlay, and SQLite local storage with schema auto-migration.
  - Next.js Web Dashboard for monitoring events and real-time statistics.
  - LINE Notify API integration with retry policies.
- **Out of Scope**:
  - Full cloud video recording storage (NVR features).
  - Facial recognition or license plate recognition.
