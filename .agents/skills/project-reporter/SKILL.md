---
name: project-reporter
description: Generates a comprehensive project report and thesis/presentation outline from the codebase.
disable-model-invocation: true
---

# Project Reporter Skill

This skill allows the agent to analyze the current codebase, database schema, and LLM Wiki, and generate structured academic reports or thesis outlines.

## Objective
To synthesize the current implementation state, database design, and key architectural choices into a clean, presentation-ready report (e.g., for thesis chapters or slide outlines).

---

## 1. Thesis/Report Structure Guide

When generating a project report, structure it into the following 5 academic chapters:

### Chapter 1: Introduction (บทนำ)
- **Problem Statement:** What problem does QSMS Rework Management solve? (E.g., tracking rework items, preventing data input errors, maintaining transaction integrity).
- **Project Objectives:** Define the main goals (e.g., automating OCR metadata extraction, enforcing business rules like non-zero amounts, roles boundaries).
- **Scope of Work:** The system boundaries (Next.js serverless architecture, Supabase real-time operational database, Cloudinary media storage, Gemini AI integration).

### Chapter 2: Literature Review & Technologies (ทฤษฎีและเทคโนโลยีที่เกี่ยวข้อง)
- **FSD (Feature-Driven Development):** Explain why the project uses FSD migration/modular breakdown.
- **Supabase & PostgreSQL:** Highlight real-time sync, pgvector, and relational integrity.
- **Gemini AI Vision & OCR:** How multimodal models analyze PDF drawings/masters.
- **RAG (Retrieval-Augmented Generation):** The RAG pipeline using Supabase vector search (`jina-embeddings-v5-text-small` and Gemini vision).

### Chapter 3: System Design & Architecture (การออกแบบระบบ)
- **Database Schema:** Provide tables, columns, relations (specifically `engineering_drawings`, `rework_cases`, `rework_items`).
- **Software Architecture:** Explain client-server boundaries (Next.js serverless routes API proxying and SPA Client Shell).
- **Workflow State Lifecycles:**
  - Case initiation (`Pending` -> `In-Progress` -> `Awaiting Valuation` -> `Completed`).
  - Item verification (`Idle` -> `Checking` -> `Verified` / `New` / `Conflict`).

### Chapter 4: Implementation & Execution (การพัฒนาระบบ)
- **Codebase Walkthrough:** Detailed explanation of key modules:
  - `src/modules/storage`: Drawing and Master specs.
  - `src/modules/rework`: Case and Item management.
  - `src/modules/guide`: DocAI RAG system.
- **OCR Ingestion Flow:** How upload modal processes PDFs base64 and sequentially calls Gemini API.
- **Custom Business Constraints:** Explain specific rules (e.g., zero-value validation, PTT OR document validation badges, oil group mapping constraint to GEAR OIL/ENGINE OIL).

### Chapter 5: Testing & Conclusion (การทดสอบและบทสรุป)
- **Testing Methodology:** E2E tests using Playwright (`/e2e`) and Unit tests using Vitest.
- **Conclusion & Future Recommendations:** Key takeaways from the QSMS project and potential future expansions.

---

## 2. Step-by-Step Reporting Instructions

1. **Information Gathering:**
   - Scan the codebase structure to report on active features.
   - Read `.llm-wiki/2_wiki/index.md` to review current architecture records.
   - Inspect `.llm-wiki/1_raw/presentation_and_report_guide.md` for writing and slide design principles.

2. **Report Generation:**
   - Generate output using Markdown.
   - Maintain professional, objective, academic language.
   - Include code snippet examples for critical business rules (e.g. `getPackageSizeGroup` sorting, `normalizeOilGroup` validation).

3. **Presentation/Slide Blueprint:**
   - Map report chapters to a **20-slide presentation blueprint**.
   - Keep text on slides minimal (follow the "less is more" rule).
   - Propose layout ideas (e.g., Mermaid diagrams, side-by-side tables).
