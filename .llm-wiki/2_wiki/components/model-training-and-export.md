# Component: Model Training & OpenVINO Export

[Updated: 2026-07-21]

## 1. Summary
This component covers model training from raw dataset annotations (`train_helmet.py`) and subsequent model graph compilation to Intel OpenVINO format (`export_model.py`).

## 2. Scripts Specification

### Training (`train_helmet.py`)
- **Base Model**: `yolo11n.pt`
- **Dataset Configuration**: `CCTV Helmet Detection.v3i.yolov11/data.yaml`
- **Hyperparameters**:
  - `epochs`: 50
  - `imgsz`: 640
  - `batch`: 8
  - `device`: `"cpu"`
  - `exist_ok`: `True`
- **Output Artifact**: `helmet_training_results/weights/best.pt`

### OpenVINO Model Export (`export_model.py`)
- **Source Artifact**: `helmet_training_results/weights/best.pt`
- **Target Format**: `openvino`
- **Export Method**: `model.export(format="openvino")`
- **Output Directory**: `helmet_training_results/weights/best_openvino_model/`
- **Benefit**: Provides up to 2-3x inference speedup on Intel CPUs compared to native PyTorch `.pt`.

## 3. Operations Workflow
```bash
# Step 1: Run Training
python train_helmet.py

# Step 2: Export to OpenVINO
python export_model.py
```

## 4. Knowledge Relationships
- Depends On: [[tech-stack/yolo11-openvino-opencv.md]]
- Impacted By: Dataset class changes in `data.yaml`
- Runtime Consumer: [[components/rtsp-cctv-inference-and-notification.md]]
