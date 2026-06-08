# Title: CCTV Helmet Detection System Architecture
[Updated: 2026-06-05]

## 1. Summary & Current Implementation
ระบบตรวจจับบุคลากรไม่สวมหมวกนิรภัย (Helmet Detection) ผ่านกล้อง CCTV ของโรงงาน เริ่มต้นด้วยการสกัดภาพจากวิดีโอดิบยาว 2 ชม. (Time-based Sampling ทุกๆ 2 วินาที) เพื่อใช้สร้าง Dataset สำหรับนำไปตีกรอบ (Annotate) บน Roboflow ด้วย Class `helmet` และ `no_helmet` จากนั้นนำไปเทรนโมเดล YOLO (v8/v11) 

สถาปัตยกรรมระบบจริงในโรงงานจะเป็น Local Server/Edge Device ที่ประมวลผลสตรีมวิดีโอสดผ่านโปรโตคอล RTSP และแจ้งเตือนทาง LINE Notify พร้อมแนบภาพถ่ายพนักงานที่ทำผิดกฎ โดยใช้ระบบ Cooldown Timer (1-2 นาที) ป้องกันสแปมส่งข้อความซ้ำซ้อน

## 2. Technical Code Snippet (Best Practice)
### สคริปต์สกัดภาพจากวิดีโอ (.asf / HEVC) แบบสุ่มวินาทีข้ามเฟรมอย่างรวดเร็ว (Seeking)
การอ่านวิดีโอเรียงเฟรม (Sequential Reader) บนไฟล์ H.265 ขนาดใหญ่จะช้ามากเนื่องจากต้องดีโค้ดทุกเฟรม วิธีที่ดีที่สุดคือการนำ PyAV (`av`) มา Seek ไปยังตำแหน่งเป้าหมายแบบสุ่มวินาที แล้วดีโค้ดเฉพาะช่วงเฟรมที่ต้องการ จากนั้นใช้ OpenCV (`cv2`) เพื่อบันทึกภาพ:

```python
import os
import av
import cv2

def extract_frames_by_seek(video_path, output_dir, target_seconds):
    os.makedirs(output_dir, exist_ok=True)
    container = av.open(video_path)
    stream = container.streams.video[0]
    time_base_val = float(stream.time_base)
    
    for i, sec in enumerate(target_seconds):
        pts_target = int(sec / time_base_val)
        container.seek(pts_target, stream=stream)
        
        for frame in container.decode(stream):
            if frame.pts >= pts_target:
                # แปลงเป็น BGR สำหรับ OpenCV
                img = frame.to_ndarray(format='bgr24')
                output_path = os.path.join(output_dir, f"frame_{i:04d}_{sec}s.jpg")
                cv2.imwrite(output_path, img)
                break
    container.close()
```

## 3. Knowledge Relationships
- Depends On (must read): [[../index.md]]
- Related Project Context: [[../../CONTEXT.md]]
