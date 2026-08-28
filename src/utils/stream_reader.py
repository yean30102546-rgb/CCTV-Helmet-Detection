import cv2
import time
import threading

class VideoStreamReader:
    """
    Decoupled video stream reader running on a separate thread to prevent RTSP/Webcam
    network spikes or latency from blocking the main AI inference loop.
    """
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        thread = threading.Thread(target=self.update, args=(), daemon=True)
        thread.start()
        return self

    def update(self):
        while not self.stopped:
            if not self.cap.isOpened():
                time.sleep(0.5)
                self.cap = cv2.VideoCapture(self.src)
                continue

            grabbed, frame = self.cap.read()
            if not grabbed:
                time.sleep(0.01)
                continue

            with self.lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return self.grabbed, self.frame.copy()

    def is_opened(self):
        return self.cap.isOpened()

    def stop(self):
        self.stopped = True
        if self.cap:
            self.cap.release()
