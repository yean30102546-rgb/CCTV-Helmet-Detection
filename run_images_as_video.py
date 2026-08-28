import cv2
import os
import glob
import time
from ultralytics import YOLO

def main():
    # 1. โหลดโมเดล OpenVINO ที่เพิ่งแปลงเสร็จ
    model_path = r"c:\Workplace\CCTV Helmet Detection\helmet_training_results\weights\best_openvino_model"
    
    if not os.path.exists(model_path):
        print(f"Error: OpenVINO model not found at {model_path}")
        print("Falling back to .pt model...")
        model_path = r"c:\Workplace\CCTV Helmet Detection\helmet_training_results\weights\best.pt"
        if not os.path.exists(model_path):
            print(f"Error: .pt model not found either. Please check paths.")
            return

    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # 2. ค้นหารูปภาพทดสอบใน dataset เพื่อนำมารันต่อกันเหมือนวิดีโอ
    test_dir = r"c:\Workplace\CCTV Helmet Detection\CCTV Helmet Detection.v3i.yolov11\test\images"
    image_paths = glob.glob(os.path.join(test_dir, "*.jpg"))
    image_paths.sort() # เรียงลำดับรูปภาพตามชื่อเฟรม

    if not image_paths:
        print(f"No images found in {test_dir}")
        return

    print(f"Found {len(image_paths)} images to play as video.")
    print("Press 'q' to stop the video.")

    # กำหนดความเร็วจำลอง (เช่น ต้องการแสดงผลที่ประมาณ 15 FPS)
    target_fps = 15
    delay = 1.0 / target_fps

    cv2.namedWindow("Real-time Labeling Simulation", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Real-time Labeling Simulation", 800, 600)

    for i, img_path in enumerate(image_paths):
        start_time = time.time()

        # อ่านรูปภาพ
        frame = cv2.imread(img_path)
        if frame is None:
            continue

        # รันโมเดลตรวจจับ
        # สามารถปรับ conf (Confidence threshold) ตามความเหมาะสม (เช่น 0.4 หรือ 0.5)
        results = model.predict(frame, conf=0.4, device="cpu", verbose=False)

        # วาด Bounding Box
        annotated_frame = results[0].plot()

        # คำนวณ FPS การประมวลผลจริง
        inference_time = time.time() - start_time
        actual_fps = 1.0 / inference_time if inference_time > 0 else target_fps

        # ใส่ข้อความบอกจำนวนเฟรมและ FPS
        cv2.putText(annotated_frame, f"Frame: {i+1}/{len(image_paths)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Actual FPS: {actual_fps:.1f}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # แสดงภาพ
        cv2.imshow("Real-time Labeling Simulation", annotated_frame)

        # คำนวณหา delay ที่เหลือเพื่อให้ได้ target FPS
        elapsed = time.time() - start_time
        sleep_time = max(1, int((delay - elapsed) * 1000))

        # รอรับการกดปุ่ม 'q' เพื่อหยุด
        if cv2.waitKey(sleep_time) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("Simulation stopped.")

if __name__ == "__main__":
    main()
