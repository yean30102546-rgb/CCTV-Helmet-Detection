import cv2
import os
from roboflow import Roboflow
import glob

# --- CONFIGURATION ---
API_KEY = os.getenv("ROBOFLOW_API_KEY") 
MODEL_ID = "helmet-no-helmet/1" # Back to original model but specifying owner
SOURCE_DIR = "dataset_frames"
OUTPUT_DIR = "test_labels_output_v2"
NUM_IMAGES = 10
CONFIDENCE = 20
OVERLAP = 30

def test_auto_label():
    if not API_KEY:
        print("ERROR: Please set the 'ROBOFLOW_API_KEY' environment variable.")
        return

    # Initialize Roboflow
    rf = Roboflow(api_key=API_KEY)
    
    # Split MODEL_ID into project and version
    project_id, version = MODEL_ID.split("/")
    
    # Explicitly use 'gbc' workspace as it worked before
    project = rf.workspace("gbc").project(project_id)
    model = project.version(int(version)).model
    
    print(f"Model Classes: {model.classes}")

    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get first 10 images
    images = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.jpg")))[:NUM_IMAGES]

    print(f"Processing {len(images)} images for testing...")

    for img_path in images:
        filename = os.path.basename(img_path)
        print(f"Predicting: {filename}")
        
        # Perform inference
        prediction = model.predict(img_path, confidence=CONFIDENCE, overlap=OVERLAP)
        
        preds = prediction.json()['predictions']
        if preds:
            print(f"  Found: {[p['class'] for p in preds]}")
        else:
            print("  No objects detected.")
        
        # Load image for drawing
        img = cv2.imread(img_path)
        
        # Draw predictions
        for pred in prediction.json()['predictions']:
            x = int(pred['x'])
            y = int(pred['y'])
            w = int(pred['width'])
            h = int(pred['height'])
            label = pred['class']
            conf = pred['confidence']

            # Calculate coordinates for OpenCV (x,y are center points)
            x1 = int(x - w/2)
            y1 = int(y - h/2)
            x2 = int(x + w/2)
            y2 = int(y + h/2)

            # Pick color (Green for helmet, Red for no-helmet)
            color = (0, 255, 0) if "no" not in label.lower() else (0, 0, 255)
            
            # Draw box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            # Draw label
            cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save annotated image
        output_path = os.path.join(OUTPUT_DIR, f"annotated_{filename}")
        cv2.imwrite(output_path, img)
        print(f"Saved: {output_path}")

    print("\nDone! Please check the 'test_labels_output' folder to see the results.")

if __name__ == "__main__":
    test_auto_label()
