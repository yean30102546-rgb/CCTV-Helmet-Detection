# Project Context: CCTV Helmet Detection

[Updated: 2026-07-22]

## Core Features
1. **Real-time Helmet Detection & ByteTrack**: Identifies individuals wearing helmets (`helmet`) versus those without helmets (`no_helmet`) with ByteTrack Person ID tracking to deduplicate alerts.
2. **CPU Acceleration & Decoupled Ingestion**: Uses Intel OpenVINO model compilation on CPU and a threaded `VideoStreamReader` for non-blocking 30 FPS stream processing.
3. **Region of Interest (RoI) Zone Filtering**: Filters detections using polygon coordinates (`CCTV_ROI`) and renders yellow monitoring boundaries on screen.
4. **AI Double-Check & Bounding Box Grounding**: Uses Google Gemini 2.5 Flash with JSON structured outputs to verify detections, return Thai descriptions, and draw non-overlapping orange bounding boxes (`Gemini Verified`).
5. **Local Database & Web Dashboard**: Stores events in SQLite (with `violation_count` schema auto-migration) and provides a real-time Next.js web dashboard (`dashboard/`) with true violation analytics.
6. **LINE Notifications & Worker Resilience**: Sends instant/batched alert messages with snapshot evidence via LINE Notify worker with retry policies and startup queue recovery.

## Agent Guardrails & Guidelines
- **System Persona**: Oak (Engineering Copilot) & Oil (Knowledge Librarian).
- **No Vibe Coding**: Always verify dataset class names (`no_helmet`) against source code checks.
- **R0/R1 Gates**: Do not commit secrets (e.g., LINE Notify Tokens or Gemini API keys) or break RTSP streaming loops.
- **Verification Rule**: Verify code changes against active Python scripts and Next.js frontend code.
