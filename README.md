# Robotic Arm - Leaf Detection System

Real-time leaf detection system with bounding boxes using YOLOv8 and React interface.

## Project Structure

```
.
├── src/
│   ├── App.js              # React app main component
│   ├── App.css             # Styling
│   ├── index.js            # React entry point
│   └── stream_server.py    # Flask server for leaf detection streaming
├── leaf_detector/          # Training data and model
│   └── runs/
│       └── leaf_detection/
│           └── weights/
│               └── best.pt # Trained YOLOv8 model
├── public/
│   └── index.html          # HTML template
└── package.json            # npm configuration
```

## Setup

### 1. Install Node.js Dependencies
```bash
npm install
```

### 2. Install Python Dependencies
```bash
cd leaf_detector
pip install -r requirements.txt
```

## Running the Application

### Option 1: Run Everything Separately

**Terminal 1 - Start the detection stream server:**
```bash
python src/stream_server.py
```

**Terminal 2 - Start the React app:**
```bash
npm start
```

Access the app at: http://localhost:8080

### Option 2: Using npm scripts

**Terminal 1:**
```bash
npm run stream
```

**Terminal 2:**
```bash
npm start
```

## Stream Server Options

```bash
# Default (uses camera at 192.168.31.163:8000)
python src/stream_server.py

# Custom camera URL
python src/stream_server.py --url http://YOUR_IP:PORT/video

# Custom confidence threshold
python src/stream_server.py --conf 0.4

# Custom port
python src/stream_server.py --port 8080
```

## How It Works

1. **Stream Server** (`src/stream_server.py`):
   - Connects to the camera stream at `http://192.168.31.163:8000/video`
   - Processes each frame with YOLOv8 leaf detection model
   - Draws bounding boxes on detected leaves
   - Serves the processed video on `http://localhost:5000/video`

2. **React App** (`src/App.js`):
   - Displays the processed video stream from the Flask server
   - Shows instructions and stream status
   - Provides a clean interface for viewing results

## Features

✅ Real-time leaf detection with bounding boxes
✅ Green boxes with confidence scores
✅ Automatic reconnection on stream loss
✅ All paths relative to project root
✅ Clean, minimal interface

## Troubleshooting

### Stream not showing:
1. Make sure `stream_server.py` is running
2. Check that the camera is accessible at `http://192.168.31.163:8000/video`
3. Verify the model exists at `leaf_detector/runs/leaf_detection/weights/best.pt`

### Port already in use:
```bash
python src/stream_server.py --port 5001
```
Then update `STREAM_URL` in `src/App.js` to `http://localhost:5001/video`

## Model Information

- **Model**: YOLOv8n (Nano)
- **Task**: Leaf Detection
- **Location**: `leaf_detector/runs/leaf_detection/weights/best.pt`
- **Classes**: leaf (single class)

## Development

The project uses:
- **Frontend**: React with Webpack
- **Backend**: Flask (Python)
- **ML**: Ultralytics YOLOv8
- **Video Processing**: OpenCV
