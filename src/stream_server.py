#!/usr/bin/env python3
"""
Leaf Detection Streaming Server - Minimal Version
Process video stream with leaf detection and serve results over HTTP
"""

import cv2
import numpy as np
from ultralytics import YOLO
from flask import Flask, Response
import argparse
import time
import threading
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LeafDetectionStreamServer:
    def __init__(self, model_path, video_url, conf_threshold=0.25, host='0.0.0.0', port=5000):
        """
        Initialize the streaming server
        
        Args:
            model_path: Path to the trained YOLO model (relative to project root)
            video_url: URL of the input video stream
            conf_threshold: Confidence threshold for detections
            host: Server host address
            port: Server port
        """
        # Convert relative path to absolute path from project root
        if not os.path.isabs(model_path):
            model_path = os.path.join(PROJECT_ROOT, model_path)
        
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.video_url = video_url
        self.host = host
        self.port = port
        
        # Stream state
        self.output_frame = None
        self.lock = threading.Lock()
        self.is_running = False
        
        # Colors for bounding boxes (BGR format)
        self.colors = {
            'leaf': (0, 255, 0),      # Green for leaves
            'text': (255, 255, 255),  # White for text
            'background': (0, 0, 0)    # Black for text background
        }
        
        # Font settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.font_thickness = 1
        
    def draw_detection_box(self, frame, box, confidence, class_name="leaf"):
        """Draw bounding box with label"""
        x1, y1, x2, y2 = map(int, box)
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), self.colors['leaf'], 2)
        
        # Prepare label text
        label = f"{class_name}: {confidence:.2f}"
        
        # Get text size for background rectangle
        (text_width, text_height), baseline = cv2.getTextSize(
            label, self.font, self.font_scale, self.font_thickness
        )
        
        # Draw background rectangle for text
        cv2.rectangle(
            frame,
            (x1, y1 - text_height - baseline - 5),
            (x1 + text_width, y1),
            self.colors['background'],
            -1
        )
        
        # Draw text
        cv2.putText(
            frame,
            label,
            (x1, y1 - baseline - 5),
            self.font,
            self.font_scale,
            self.colors['text'],
            self.font_thickness
        )
        
        return frame
    
    def process_stream(self):
        """Process video stream with leaf detection"""
        print(f"Connecting to input stream: {self.video_url}")
        cap = cv2.VideoCapture(self.video_url)
        
        if not cap.isOpened():
            print(f"Error: Could not open video stream {self.video_url}")
            return
        
        print("Successfully connected to input stream!")
        print("Starting leaf detection processing...")
        
        # Connection retry parameters
        max_retries = 5
        retry_count = 0
        
        self.is_running = True
        
        while self.is_running:
            ret, frame = cap.read()
            
            if not ret:
                print("Warning: Could not read frame from stream")
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Error: Lost connection after {max_retries} retries")
                    break
                
                print(f"Attempting to reconnect... ({retry_count}/{max_retries})")
                cap.release()
                time.sleep(1)
                cap = cv2.VideoCapture(self.video_url)
                continue
            
            # Reset retry count on successful read
            retry_count = 0
            
            # Run detection
            results = self.model.predict(
                frame,
                conf=self.conf_threshold,
                verbose=False
            )
            
            # Process detections - draw bounding boxes
            for result in results:
                if result.boxes is not None:
                    for box, conf in zip(result.boxes.xyxy, result.boxes.conf):
                        frame = self.draw_detection_box(
                            frame, box.cpu().numpy(), conf.item()
                        )
            
            # Update output frame
            with self.lock:
                self.output_frame = frame.copy()
        
        cap.release()
        print("Stream processing stopped")
    
    def generate_frames(self):
        """Generate frames for streaming"""
        while True:
            with self.lock:
                if self.output_frame is None:
                    continue
                
                # Encode frame as JPEG
                (flag, encoded_image) = cv2.imencode(".jpg", self.output_frame)
                
                if not flag:
                    continue
            
            # Yield frame in byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                  bytearray(encoded_image) + b'\r\n')
    
    def start_server(self):
        """Start the Flask server"""
        app = Flask(__name__)
        
        @app.route('/')
        @app.route('/video')
        def video_feed():
            """Video streaming route"""
            return Response(
                self.generate_frames(),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )
        
        # Start processing thread
        processing_thread = threading.Thread(target=self.process_stream)
        processing_thread.daemon = True
        processing_thread.start()
        
        # Start Flask server
        print(f"\nLeaf Detection Stream Server Started")
        print(f"Stream URL: http://{self.host}:{self.port}/")
        print(f"Press Ctrl+C to stop\n")
        
        app.run(host=self.host, port=self.port, threaded=True, debug=False)

def main():
    parser = argparse.ArgumentParser(description='Leaf Detection Streaming Server')
    parser.add_argument('--model', 
                       default='leaf_detector/runs/leaf_detection/weights/best.pt',
                       help='Path to trained model (.pt file) relative to project root')
    parser.add_argument('--url', 
                       default='http://192.168.31.163:8000/video',
                       help='URL of the input video stream')
    parser.add_argument('--conf', type=float, default=0.5, 
                       help='Confidence threshold (default: 0.25)')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Server host (default: 0.0.0.0 for all interfaces)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Server port (default: 5000)')
    
    args = parser.parse_args()
    
    # Convert model path to absolute path
    model_path = args.model
    if not os.path.isabs(model_path):
        model_path = os.path.join(PROJECT_ROOT, model_path)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} not found")
        print(f"Looking in: {model_path}")
        print(f"Project root: {PROJECT_ROOT}")
        return
    
    # Create and start server
    server = LeafDetectionStreamServer(
        model_path=args.model,
        video_url=args.url,
        conf_threshold=args.conf,
        host=args.host,
        port=args.port
    )
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        server.is_running = False

if __name__ == "__main__":
    main()

