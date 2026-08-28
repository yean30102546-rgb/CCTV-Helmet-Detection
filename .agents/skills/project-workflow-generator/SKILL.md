---
name: project-workflow-generator
description: Generates visual Mermaid diagrams and workflow documentation for the project.
disable-model-invocation: true
---

# Project Workflow Generator Skill

This skill allows the agent to extract the system's runtime flows and map them into visual flowcharts or sequence diagrams using **Mermaid.js** syntax.

## Objective
To provide visual workflow documentation that can be easily pasted into thesis reports or presentation slides to explain the application's runtime logic.

---

## 1. Key System Workflows

When generating workflows, focus on these five core operations:

### Workflow A: Drawing & Master PDF Ingestion (AI OCR)
Shows how a user uploads a PDF and the system parses metadata.
- **Trigger:** User uploads file in `UploadModal.tsx`.
- **Parsing:** Frontend converts PDF to Base64, splits headers, and sends to `/api/drawings` with the action `parse_drawing`.
- **Gemini Process:** Server calls Gemini API (`gemini-3.5-flash` or `gemini-3.1-flash-lite` fallback).
- **Result:** Returns structured metadata to frontend, allows editing, and saves to database (`is_active` updates for duplicates).

### Workflow B: Rework Case Initiation & Item Verification
Shows how a rework case is initiated and checked against Item Master.
- **Trigger:** Operator initializes case, system assigns Case ID (`RW...` or `RT...`).
- **Autofill & Verification:** User enters `Item Number` / `Item Code`. Trigger lookup in database.
- **State Transition:** Status transitions from `Idle` -> `Checking` -> `Verified` (found) / `New` (not found) / `Conflict` (mismatch).
- **Enforcements:** Prevent `amount` = 0 or `boxNumber` = 0. Link sources if product is dirty/leaking.

### Workflow C: Rework Rounting & Valuation Flow
Shows the lifecycle transitions and financial review.
- **Status Lifecycle:** `Pending` -> `In-Progress` -> `Awaiting Valuation` -> `Completed`.
- **Operator Role:** Logs labor hours, materials, resolution methods.
- **Finance Role:** Receives case in `Awaiting Valuation`, enters actual costs and labor rates, and completes case.

### Workflow D: Cloudinary Image Integrity Transaction
Shows how evidence images are processed to prevent database orphans.
- **Action:** User uploads image.
- **Client Processing:** Frontend compresses image to target ~300KB.
- **Upload Transaction:** Direct unsigned upload to Cloudinary.
- **DB Write:** If successful, save URL to Supabase. If save fails, roll back or delete the uploaded Cloudinary asset to maintain media integrity.

### Workflow E: DocAI RAG Manual Ingestion & Deletion Pipeline
Shows how technical manuals are chunked, embedded, and deleted.
- **Ingestion:** PDF upload -> Convert to JPEG -> OCR text via Gemini Vision -> embed text via Jina AI -> save vector to Supabase.
- **RAG Bulk Deletion:** Bulk delete documents triggers deletion of PDF file, chunks database entries, and vector embeddings in Supabase (`bulk_delete_documents`).

---

## 2. Mermaid.js Coding Guidelines

- **Always use correct Mermaid syntax** (flowchart TD/LR, sequenceDiagram, stateDiagram-v2).
- **Avoid HTML tags** inside node labels.
- **Always wrap text with quotes** if it contains special characters like brackets or parentheses.
- **Provide clear step-by-step explanations** underneath every diagram.
