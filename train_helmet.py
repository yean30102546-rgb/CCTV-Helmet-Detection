import os
from ultralytics import YOLO

def main():
    # 1. Path setup
    project_dir = r"c:\Workplace\CCTV Helmet Detection"
    dataset_yaml = os.path.join(project_dir, "CCTV Helmet Detection.v3i.yolov11", "data.yaml")
    
    # 2. Load the lightweight Nano model
    print("Loading YOLO11n model...")
    model = YOLO("yolo11n.pt")  # It will download automatically if not found locally
    
    # 3. Start training on CPU
    print(f"Starting training process using data: {dataset_yaml}")
    print("WARNING: Training on CPU will take significant time.")
    
    results = model.train(
        data=dataset_yaml,
        epochs=50,          # Set to 50 initially to get results faster on CPU
        imgsz=640,          # Standard image size for YOLO
        batch=8,            # Lower batch size to prevent memory issues on laptop
        device="cpu",       # Force CPU training
        project=project_dir,
        name="helmet_training_results",
        exist_ok=True       # Overwrite if folder exists
    )
    
    print("==================================================")
    print("Training Completed!")
    print(f"Best model weights saved to: {os.path.join(project_dir, 'helmet_training_results', 'weights', 'best.pt')}")
    print("==================================================")

if __name__ == '__main__':
    main()
