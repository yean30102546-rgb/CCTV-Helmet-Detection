# Lessons Learned: Bugs & Fixes

[Updated: 2026-07-22]

## 1. Active Code Mismatches & Critical Audit Findings

### [CRITICAL BUG / CONFLICT NOTE] Class Name Mismatch in Notification Trigger
- **Symptom**: `run_cctv.py` may fail to trigger LINE Notify alerts even when someone without a helmet is detected.
- **Root Cause**: `run_cctv.py` (lines 96-97) explicitly checks:
  ```python
  if class_name == "no-helmet" or class_name == "Without Helmet":
  ```
  However, `CCTV Helmet Detection.v3i.yolov11/data.yaml` defines classes as:
  ```yaml
  names: ['helmet', 'no_helmet']
  ```
  Note the underscore (`no_helmet`) in `data.yaml` vs hyphen (`no-helmet`) in `run_cctv.py`.
- **Fix**: Updated `run_cctv.py` condition to check `class_name == "no_helmet" or class_name == "no-helmet" or class_name == "Without Helmet"`.

---

### Hardcoded Model Absolute Paths
- **Symptom**: Model paths in `run_cctv.py` and `run_images_as_video.py` use hardcoded absolute path `c:\Workplace\CCTV Helmet Detection\...` which differs from workspace path `c:\Workplace\Mytask\Projects\CCTV Helmet Detection\...`.
- **Status**: System currently falls back to `yolo11n.pt` or resolves dynamically using `Path(__file__).resolve().parent`.
- **Fix**: Use `os.path.join(os.path.dirname(__file__), ...)` for relative resolution.

---

## 2. Async Worker & API Rate Limit Fixes

### Async Image File Writing Race Condition
- **Symptom**: Gemini Worker reports `Error: Image ... not found for Gemini verification.` and rejects valid detection tasks.
- **Root Cause**: `run_cctv.py` offloaded `cv2.imwrite` to a `ThreadPoolExecutor` (P1.2 Async Write), but immediately pushed the task to `gemini_task_queue`. Gemini Worker popped the item and checked `os.path.exists(image_path)` before the background thread finished writing the file to disk.
- **Fix**: Added a polling wait loop in `gemini_worker.py` (`while not os.path.exists(image_path) and wait_count < 20: time.sleep(0.1)`) allowing up to 2 seconds for the image file to flush to disk before checking.

### LINE Notifier Unbatched Flag False Clearance
- **Symptom**: Unbatched detections were marked as `is_batched = 1` even when LINE Notify HTTP request failed due to network disconnection or invalid token.
- **Root Cause**: `notifier_loop()` called `mark_as_batched(record_ids)` unconditionally after `send_line_notify()`, regardless of HTTP status code.
- **Fix**: Updated `send_line_notify()` to return a boolean `True` only on HTTP 200 success, and wrapped `mark_as_batched()` in `if sent_success:`.

### Gemini 429 Rate Limit & Pending State
- **Symptom**: Detections stay in `Verifying...` (`PENDING_GEMINI` status) on Dashboard indefinitely.
- **Root Cause**: Google Gemini API Free Tier returned `429 RESOURCE_EXHAUSTED` due to exceeding requests per minute/day when processing dense detection frames.
- **Fix**: Implemented exponential backoff retries (3 attempts) in `gemini_worker.py`, startup recovery loop (`get_pending_gemini_detections`), and IoU non-overlap filtering to reduce unnecessary API calls.

---

## 3. Next.js Web Dashboard & UI Fixes

### Next.js App Router GET Cache Trap
- **Symptom**: `/api/detections` returns an empty array `[]` on the dashboard, even when the SQLite database has data.
- **Root Cause**: Next.js 14/15 aggressively caches `GET` route handlers during build/dev if they aren't explicitly opted out of caching.
- **Fix**: Added `export const dynamic = 'force-dynamic';` to the top of `route.ts`.

### React `useEffect` Missing Polling
- **Symptom**: The Next.js dashboard does not automatically update when new detections arrive; requires a manual page reload.
- **Root Cause**: The `useEffect` fetching the API was configured with an empty dependency array `[]` and no timer.
- **Fix**: Replaced single `fetch` with `setInterval(fetchData, 3000)` inside `useEffect` and cleaned up the interval on unmount.

### Tailwind CSS Cyclical Variables
- **Symptom**: Next.js fails to compile CSS or crash during development with `Expected '</', got '<eof>'` or similar AST parsing errors.
- **Root Cause**: In `globals.css` using Tailwind v4, a variable was defined recursively: `--font-sans: var(--font-sans);`.
- **Fix**: Replaced cyclical reference with the actual base token (e.g., `--font-sans: var(--font-geist-sans);`).
