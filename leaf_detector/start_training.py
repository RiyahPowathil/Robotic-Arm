#!/usr/bin/env python3
"""
Simple script to start YOLOv8n training
Run this when you're ready to train the model
"""

import os
import subprocess
import sys

def start_training():
    """Start the YOLOv8n training process"""
    print("Starting YOLOv8n Leaf Detection Training")
    print("=" * 50)
    
    # Check if virtual environment exists
    venv_python = "/home/shuttle_01/Desktop/leaf_detector/.env/bin/python"
    if not os.path.exists(venv_python):
        print("Error: Virtual environment not found. Please run setup first.")
        return False
    
    # Check if training script exists
    train_script = "/home/shuttle_01/Desktop/leaf_detector/train_yolov8.py"
    if not os.path.exists(train_script):
        print("Error: Training script not found.")
        return False
    
    print("Training configuration:")
    print("- Model: YOLOv8n (nano)")
    print("- Epochs: 60")
    print("- Image size: 1024x1024")
    print("- Batch size: 8")
    print("- Dataset: 1130 images (904 train, 113 val, 113 test)")
    print()
    
    # Ask for confirmation
    response = input("Do you want to start training? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Training cancelled.")
        return False
    
    print("\nStarting training...")
    print("This may take several hours depending on your hardware.")
    print("Training progress will be displayed below.")
    print("-" * 50)
    
    try:
        # Run the training script
        result = subprocess.run([venv_python, train_script], check=True)
        print("\n" + "=" * 50)
        print("Training completed successfully!")
        print("Check the 'runs/leaf_detection' directory for results.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nTraining failed with error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nTraining interrupted by user.")
        return False

if __name__ == "__main__":
    start_training()
