#!/usr/bin/env python3
"""
YOLOv8n Leaf Detection Inference Script
Test the trained model on new images
"""

import os
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import argparse

def detect_leaves(model_path, image_path, output_dir=None, conf_threshold=0.25):
    """
    Detect leaves in an image using the trained YOLOv8n model
    
    Args:
        model_path: Path to the trained model (.pt file)
        image_path: Path to the input image
        output_dir: Directory to save results (optional)
        conf_threshold: Confidence threshold for detections
    """
    # Load the trained model
    model = YOLO(model_path)
    
    # Run inference
    results = model.predict(
        image_path,
        conf=conf_threshold,
        save=output_dir is not None,
        project=output_dir,
        name='leaf_detection_results'
    )
    
    # Display results
    for result in results:
        # Get the image with detections
        annotated_img = result.plot()
        
        # Convert BGR to RGB for matplotlib
        annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        
        # Display the image
        plt.figure(figsize=(12, 8))
        plt.imshow(annotated_img)
        plt.axis('off')
        plt.title(f'Leaf Detection Results (Confidence ≥ {conf_threshold})')
        plt.show()
        
        # Print detection statistics
        print(f"Detected {len(result.boxes)} leaves")
        if len(result.boxes) > 0:
            print("Confidence scores:")
            for i, conf in enumerate(result.boxes.conf):
                print(f"  Leaf {i+1}: {conf:.3f}")
    
    return results

def batch_detect(model_path, image_dir, output_dir=None, conf_threshold=0.25):
    """
    Detect leaves in all images in a directory
    
    Args:
        model_path: Path to the trained model (.pt file)
        image_dir: Directory containing images
        output_dir: Directory to save results (optional)
        conf_threshold: Confidence threshold for detections
    """
    # Load the trained model
    model = YOLO(model_path)
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [f for f in os.listdir(image_dir) 
                   if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No image files found in {image_dir}")
        return
    
    print(f"Processing {len(image_files)} images...")
    
    # Run batch inference
    results = model.predict(
        image_dir,
        conf=conf_threshold,
        save=output_dir is not None,
        project=output_dir,
        name='batch_leaf_detection'
    )
    
    # Print summary
    total_detections = 0
    for result in results:
        total_detections += len(result.boxes)
    
    print(f"Total detections across all images: {total_detections}")
    print(f"Average detections per image: {total_detections/len(image_files):.1f}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='YOLOv8n Leaf Detection Inference')
    parser.add_argument('--model', required=True, help='Path to trained model (.pt file)')
    parser.add_argument('--image', help='Path to single image for detection')
    parser.add_argument('--image_dir', help='Directory containing images for batch detection')
    parser.add_argument('--output', help='Output directory for results')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold (default: 0.25)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model file {args.model} not found")
        return
    
    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file {args.image} not found")
            return
        print(f"Detecting leaves in: {args.image}")
        detect_leaves(args.model, args.image, args.output, args.conf)
    
    elif args.image_dir:
        if not os.path.exists(args.image_dir):
            print(f"Error: Image directory {args.image_dir} not found")
            return
        print(f"Detecting leaves in directory: {args.image_dir}")
        batch_detect(args.model, args.image_dir, args.output, args.conf)
    
    else:
        print("Error: Please specify either --image or --image_dir")
        parser.print_help()

if __name__ == "__main__":
    main()
