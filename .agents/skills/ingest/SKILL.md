---
name: ingest
description: Incremental ingestion of recent work, bugs, knowledge, and system updates into Second Brain Wiki (.llm-wiki/2_wiki/) and mandatory synchronization of root project context files (CONTEXT.md, GEMINI.md, README.md, USER_GUIDE.md, PRODUCT.md).
disable-model-invocation: true
---

Execute a comprehensive Knowledge Ingestion and Project Context Synchronization session following these systematic steps:

## 1. Delta Identification (ตรวจจับงานและความเปลี่ยนแปลงล่าสุด)
- Inspect `.llm-wiki/2_wiki/log.md` to identify the timestamp/date of the last recorded ingestion.
- Review recent Git commit logs, task history, and file changes since the last ingestion date.
- Identify all new features, bug fixes, refactoring operations, architectural shifts, and role/permission modifications performed during this timeframe.

## 2. Source Code Verification (ตรวจสอบเทียบสเตตจริงของโค้ด)
- Cross-reference all findings against active source code in `src/`, `app/api/`, `supabase/`, etc.
- Verify API contracts, DB schema changes, active UI features, and configuration settings.
- If any legacy documentation or raw files contradict active code, tag them with `[Deprecated]` or `[Conflict Note]` along with the date and reason.

## 3. Second Brain Ingestion (ย่อยและบันทึกเข้าสู่ .llm-wiki/2_wiki/)
- Update `.llm-wiki/2_wiki/log.md` with a new chronological entry covering the ingested period.
- If new bugs were discovered and fixed, append them to `.llm-wiki/2_wiki/lessons-learned/bugs-and-fixes.md`.
- If new architectural patterns or modules were added/modified, update the corresponding files under `.llm-wiki/2_wiki/architecture/` or `.llm-wiki/2_wiki/nextjs-frontend/`.
- Update `.llm-wiki/2_wiki/index.md` to reflect any new or modified wiki entries.

## 4. Mandatory Root Context Synchronization (อัปเดตไฟล์บริบทหลักของโปรเจกต์)
Must update all root context files to match current source code implementation:
- **`CONTEXT.md`**: Update technical architecture, API signatures, state models, data flow, and terminology glossary. Remove obsolete roles/fields.
- **`GEMINI.md`**: Update project context, core features, model specifications, workflow steps, tech stack, and agent guardrails.
- **`README.md`**: Update feature list, tech stack description, database models, and mock account credentials.
- **`USER_GUIDE.md`**: Update user roles, capabilities, and operational steps for users.
- **`PRODUCT.md`**: Update target users, product purpose, and scope.

## 5. Ingestion Summary (สรุปผลการทำงาน)
Provide a clear, structured summary detailing:
- The timeframe/delta ingested.
- Wiki files created or updated in `.llm-wiki/2_wiki/`.
- Root context files synchronized (`CONTEXT.md`, `GEMINI.md`, etc.).
- Any conflicts or deprecated patterns identified during verification.
