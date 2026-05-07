#!/usr/bin/env python3
"""
Vision detection bridge: camera → SSD MobileNet v2 → /boomy/detections_json
Runs on the Pi. Publishes COCO-class detections as JSON on ROS topic.
"""
import json, os, sys, time
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

MODEL_DIR = "/detection_model"
CAMERA_SOURCE = "http://192.168.1.11:6001/video_feed"  # Use demo MJPEG to avoid /dev/video0 contention
CONFIDENCE_THRESHOLD = 0.45
FRAME_INTERVAL = 2.0

import urllib.request

COCO_CLASSES = [
    "background", "person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
    "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
    "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
]


class DetectionBridge(Node):
    def __init__(self):
        super().__init__("detection_bridge")
        self.pub = self.create_publisher(String, "/boomy/detections_json", 10)
        self.get_logger().info("Loading SSD MobileNet v2...")
        cfg = os.path.join(MODEL_DIR, "pipeline.config")
        weights = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
        if not os.path.exists(weights):
            self.get_logger().error("Model not found at %s", weights)
            self.net = None
            return
        self.net = cv2.dnn.readNetFromTensorflow(weights, cfg)
        self.get_logger().info("Model loaded. Opening MJPEG stream from demo...")
        self.stream_url = os.environ.get("DETECTION_CAM_URL", CAMERA_SOURCE)
        self.stream = None
        self.bytes_buf = b""
        self._open_stream()
        self.last_infer = 0.0
        self.timer = self.create_timer(0.5, self._loop)
        self.get_logger().info("Detection bridge ready (MJPEG stream). Publishing on /boomy/detections_json")

    def _open_stream(self):
        try:
            self.stream = urllib.request.urlopen(self.stream_url, timeout=5)
        except Exception as e:
            self.get_logger().error("Cannot open MJPEG stream: %s", e)
            self.stream = None

    def _read_mjpeg_frame(self):
        if self.stream is None:
            self._open_stream()
            if self.stream is None:
                return None
        try:
            while True:
                self.bytes_buf += self.stream.read(4096)
                a = self.bytes_buf.find(b"\xff\xd8")
                b = self.bytes_buf.find(b"\xff\xd9")
                if a != -1 and b != -1 and b > a:
                    jpg = self.bytes_buf[a:b+2]
                    self.bytes_buf = self.bytes_buf[b+2:]
                    return cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
        except Exception:
            self.stream = None
            return None

    def _loop(self):
        if self.net is None:
            return
        now = time.time()
        if now - self.last_infer < FRAME_INTERVAL:
            return
        self.last_infer = now
        frame = self._read_mjpeg_frame()
        if frame is None:
            return
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
        self.net.setInput(blob)
        detections = self.net.forward()
        results = []
        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf < CONFIDENCE_THRESHOLD:
                continue
            cls_id = int(detections[0, 0, i, 1])
            label = COCO_CLASSES[cls_id] if cls_id < len(COCO_CLASSES) else "unknown"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            results.append({
                "label": label,
                "confidence": round(conf, 3),
                "box": [round(float(b), 1) for b in box],
            })
        if results:
            msg = String(data=json.dumps({"detections": results, "ts": now}))
            self.pub.publish(msg)
            labels = [r["label"] for r in results]
            self.get_logger().info("Detected: %s", labels)


def main():
    rclpy.init()
    node = DetectionBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.stream:
            node.stream.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
