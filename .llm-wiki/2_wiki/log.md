# Ingestion Log

[Updated: 2026-07-22]

## Chronological History

### 2026-07-22 - Added ByteTrack Object Tracking, Decoupled StreamReader, RoI Filtering, Gemini Bounding Box Grounding & Auto .env
- **Scope**: Ingested ByteTrack tracking pipeline, `VideoStreamReader`, async image file writing, RoI polygon filtering, Gemini JSON bounding box grounding with IoU non-overlap filtering, SQLite DB schema migration (`violation_count`), auto `.env` loading, and Next.js Dashboard stats updates.
- **Classification Tiering**:
  - **Tier A (System Architecture & Current Source)**: Extracted ByteTrack tracking (`model.track`), `VideoStreamReader` thread, `ThreadPoolExecutor` async writer, `is_center_in_roi` filter, Gemini JSON grounding (`boxes`, `violation_count`), IoU overlap filter (`compute_iou`), and SQLite auto-migration (`violation_count`).
  - **Tier B (Lessons Learned & Historical Bug Fixes)**: Logged fixes for Async File Writing race condition in Gemini worker (`os.path.exists` wait loop), LINE Notify unbatched flag bug, and Gemini 429 Rate Limit handling.
- **Root Context Sync**: Synchronized `CONTEXT.md`, `GEMINI.md`, `README.md`, `USER_GUIDE.md`, and `PRODUCT.md` with 100% fidelity to current source code.

### 2026-07-21 - Added Next.js Dashboard & AI Double-Check Verification
- **Scope**: Ingested new UI components, Next.js dashboard, SQLite database implementation, and Gemini API worker.
- **Classification Tiering**:
  - **Tier A (System Architecture & Current Source)**: Extracted Gemini 2.5 Flash validation, SQLite DB structure (`detections`), and Next.js App Router UI.
  - **Tier B (Lessons Learned & Historical Bug Fixes)**: Logged fixes for Next.js GET Route Caching, React `useEffect` Polling bugs, and Tailwind CSS cyclical recursion error.
- **Root Context Sync**: Synchronized `CONTEXT.md`, `GEMINI.md`, `README.md`, `USER_GUIDE.md`, and `PRODUCT.md` with Next.js dashboard, SQLite, and Gemini 2.5 Flash integrations.

### 2026-07-21 - Initial Knowledge Ingestion & Root Context Synchronization
- **Scope**: Ingested workspace source code (`run_cctv.py`, `train_helmet.py`, `export_model.py`, `run_images_as_video.py`, dataset `data.yaml`) and classified 83 raw files in `.llm-wiki/1_raw/`.
- **Classification Tiering**:
  - **Tier A (System Architecture & Current Source)**: Extracted YOLO11 + OpenVINO inference pipeline, RTSP stream handling, and LINE Notify integration into `2_wiki/architecture/` and `2_wiki/components/`.
  - **Tier B (Lessons Learned & Historical Bug Fixes)**: Compiled historical fix patterns and live code mismatch (`no-helmet` string check vs dataset `no_helmet` class) into `2_wiki/lessons-learned/bugs-and-fixes.md`.
  - **Tier C (General External Knowledge)**: Preserved 40+ external tutorials/framework docs in `1_raw/` without polluting Wiki (Lazy-loaded).
- **Conflict Note / Deprecated Context**: Marked legacy web application docs (QSMS, Next.js, Firebase, Google Apps Script) found in `1_raw/` as `[Conflict Note / Legacy Context]`.
- **Root Context Sync**: Synchronized `CONTEXT.md`, `GEMINI.md`, `README.md`, `USER_GUIDE.md`, and `PRODUCT.md` with 100% fidelity to active CCTV Helmet Detection codebase.
