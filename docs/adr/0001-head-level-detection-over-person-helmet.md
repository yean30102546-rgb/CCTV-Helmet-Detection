# 1. Use Head-Level Detection Instead of Person+Helmet for PPE

Date: 2026-06-06

## Status

Accepted

## Context

We are building a CCTV-based AI system to detect workers not wearing helmets and send LINE Notify alerts. 
To speed up dataset creation, we tried using pre-trained auto-labeling models from Roboflow Universe. However, these models struggle to accurately detect `no_helmet` (bare heads) due to high visual variance.

An alternative was proposed: use highly accurate off-the-shelf models to detect `Person` (full body) and `Helmet`. If a `Person` bounding box does not contain a `Helmet` bounding box inside it, we trigger a "no helmet" alarm.

This alternative presents a trade-off:
- **Pros:** Extremely easy to auto-label the dataset today because `Person` and `Helmet` models are ubiquitous and highly accurate.
- **Cons:** CCTV cameras are often mounted high up, causing people to overlap (occlusion) in the frame. Mapping which helmet belongs to which person using Intersection-over-Union (IoU) logic in post-processing is complex, error-prone, and adds computational overhead on edge devices.

## Decision

We will use **Head-Level Detection** with exactly two classes: `helmet` (head with hard hat) and `no_helmet` (bare head). We reject the `Person` + `Helmet` intersection approach.

## Consequences

- **Short-term pain:** We must manually annotate the `no_helmet` class for the initial dataset batch (e.g., 500-1,000 images) since auto-labeling models cannot reliably do it for us.
- **Long-term stability:** The final YOLO model will directly output the actionable class (`no_helmet`). The application logic on the Inference Server will be drastically simpler, faster, and much less prone to false positives caused by crowded scenes.
