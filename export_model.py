import os
from ultralytics import YOLO

def main():
    model_path = r"c:\Workplace\CCTV Helmet Detection\helmet_training_results\weights\best.pt"
    
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading trained model: {model_path}")
    model = YOLO(model_path)

    print("Exporting model to OpenVINO format to maximize CPU (i5) performance...")
    # This will create a folder named 'best_openvino_model' next to best.pt
    exported_path = model.export(format="openvino")
    
    print(f"Export successful! OpenVINO model is located at: {exported_path}")

if __name__ == "__main__":
    main()
