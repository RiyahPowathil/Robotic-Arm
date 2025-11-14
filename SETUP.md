# Quick Setup Guide

## Overview
The streaming server (`src/stream_server.py`) processes the camera feed with leaf detection and serves it to the React app. All paths are now relative to the project root.

## File Structure
```
Robotic Arm/
├── src/
│   ├── stream_server.py    ← Flask server (leaf detection)
│   ├── App.js              ← React component
│   ├── App.css             ← Styling
│   └── index.js            ← React entry
├── leaf_detector/
│   └── runs/leaf_detection/weights/best.pt  ← Trained model
├── package.json            ← npm config (includes "npm run stream")
└── README.md               ← Full documentation
```

## Run the System

### Terminal 1 - Start Detection Server
```bash
cd "/home/shuttle_01/Desktop/Learning/Robotic Arm"
python src/stream_server.py
```
Or use npm:
```bash
npm run stream
```

This will:
- Connect to camera at `http://192.168.31.163:8000/video`
- Process frames with YOLOv8 leaf detection
- Serve results at `http://localhost:5000/video`

### Terminal 2 - Start React App
```bash
npm start
```

Then open: **http://localhost:8080**

## What Changed

✅ Moved `stream_server.py` from `leaf_detector/` to `src/`
✅ Updated all paths to be relative to project root
✅ Model path now: `leaf_detector/runs/leaf_detection/weights/best.pt`
✅ React app now displays stream from `http://localhost:5000/video`
✅ Added `npm run stream` script to package.json
✅ Updated README with full documentation

## Server Options

```bash
# Higher confidence (fewer detections)
python src/stream_server.py --conf 0.5

# Different port
python src/stream_server.py --port 8080

# Different camera
python src/stream_server.py --url http://OTHER_IP:PORT/video
```

## Architecture

```
Camera (192.168.31.163:8000)
    ↓
stream_server.py (processes with YOLO)
    ↓
Flask Server (localhost:5000)
    ↓
React App (localhost:8080)
```

## Quick Test

1. `python src/stream_server.py` (wait for "Stream Server Started")
2. `npm start` (in another terminal)
3. Open http://localhost:8080
4. You should see video with green bounding boxes around leaves!

