# Leaf Detection - Video Stream Usage Guide

## Overview
This script runs the trained leaf detection model on a video stream from a network camera/server and visualizes bounding boxes in real-time.

## Quick Start

### Basic Usage (with default settings)
```bash
cd /home/shuttle_01/Desktop/Learning/Robotic\ Arm/leaf_detector
python video_stream_detection.py
```

This will connect to `http://192.168.31.163:8000/video` by default.

### Custom Video URL
```bash
python video_stream_detection.py --url http://YOUR_IP:PORT/video
```

### Custom Confidence Threshold
```bash
python video_stream_detection.py --conf 0.4
```

### Custom Model
```bash
python video_stream_detection.py --model /path/to/your/model.pt
```

### All Options Combined
```bash
python video_stream_detection.py \
  --url http://192.168.31.163:8000/video \
  --model runs/leaf_detection/weights/best.pt \
  --conf 0.25
```

## Keyboard Controls

While the detection window is active:

- **`q`** - Quit the application
- **`c`** - Capture current frame to image file
- **`+`** or **`=`** - Increase confidence threshold
- **`-`** - Decrease confidence threshold

## Features

✅ Real-time leaf detection with bounding boxes  
✅ Green boxes around detected leaves  
✅ Confidence scores displayed on each detection  
✅ Live FPS counter  
✅ Current detection count  
✅ Adjustable confidence threshold on-the-fly  
✅ Image capture functionality  
✅ Automatic reconnection on stream loss  

## Requirements

Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

Key packages:
- ultralytics (YOLOv8)
- opencv-python
- torch
- numpy

## Troubleshooting

### Can't Connect to Stream
1. Check if the stream URL is correct
2. Verify the stream server is running
3. Test the URL in a browser or with curl: `curl http://192.168.31.163:8000/video`
4. Ensure you're on the same network (or have proper routing)

### Low FPS
- Try reducing the resolution of your stream
- Use a lower confidence threshold
- Ensure your GPU drivers are properly installed for faster inference

### Model Not Found
The script looks for the model at:
`/home/shuttle_01/Desktop/Learning/Robotic Arm/leaf_detector/runs/leaf_detection/weights/best.pt`

If it's elsewhere, specify with `--model` flag.

## Example Output

```
Connecting to video stream: http://192.168.31.163:8000/video
Successfully connected to video stream!
Starting leaf detection...
Press 'q' to quit, 'c' to capture image
Press '+' or '-' to adjust confidence threshold
```

The detection window will show:
- Leaves Detected: X
- FPS: XX.X
- Confidence: 0.XX
- Stream URL
- Control instructions

## Notes

- The script will attempt to reconnect automatically if the stream is lost
- Captured images are saved with timestamps in the current directory
- The info panel at the top shows real-time statistics

