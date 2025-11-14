#!/usr/bin/env python3
"""
YOLOv8n Leaf Detection Training Script
Based on the reference notebook for leaf detection using Ultralytics YOLOv8
"""

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import random
import shutil
import cv2
import seaborn as sns
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
import yaml

# Set random seed for reproducibility
random_seed = 42
random.seed(random_seed)

def csv_to_dataframe(csv_filepath, columns_name):    
    """Convert CSV file to pandas DataFrame"""
    df = pd.read_csv(csv_filepath, names=columns_name, header=0)
    return df

def calc_percentage(df_total, df_part, file_id_column):
    """Calculate percentage of data in subset"""
    part = len(df_part[file_id_column].unique())
    total = len(df_total[file_id_column].unique())
    return (part / total) * 100

def convert_bbox_to_yolo(x, y, width, height, img_width, img_height):
    """Convert bounding box format to YOLO format"""
    x_center = (x + width / 2) / img_width
    y_center = (y + height / 2) / img_height
    width /= img_width
    height /= img_height
    return x_center, y_center, width, height

def dataframe_yolofiles(df, output_dir):
    """Convert DataFrame to YOLO format text files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)    
    data = {}    
    for index, row in df.iterrows():
        image_id = row['image_id']
        img_width = int(row['width'])
        img_height = int(row['height'])
        bbox = eval(row['bbox'])
        x, y, width, height = bbox
        x_center, y_center, norm_width, norm_height = convert_bbox_to_yolo(x, y, width, height, img_width, img_height)        
        if image_id not in data:
            data[image_id] = []        
        data[image_id].append(f"0 {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")    
    for image_id, bboxes in data.items():
        output_file_path = os.path.join(output_dir, os.path.splitext(image_id)[0] + ".txt")
        with open(output_file_path, 'w') as f:
            for bbox in bboxes:
                f.write(bbox + "\n")
    print(f'Total text files created in: {output_dir}')

def move_images_to_directory(df, root_dir, target_dir):
    """Move images to target directory"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)    
    unique_image_ids = df['image_id'].unique()    
    for image_id in unique_image_ids:
        source_path = os.path.join(root_dir, image_id)
        target_path = os.path.join(target_dir, image_id)        
        if os.path.exists(source_path):
            shutil.copy(source_path, target_path)
        else:
            print(f"Warning: Image {image_id} not found on path {source_path}")
    print(f'Total images moved to: {target_dir}')

def create_yaml_config(output_dir):
    """Create YAML configuration file for YOLO training"""
    yaml_data = {
        'train': f'{output_dir}/train/images',
        'val': f'{output_dir}/valid/images',
        'test': f'{output_dir}/test/images',
        'nc': 1,
        'names': ['leaf']
    }
    
    yaml_path = os.path.join(output_dir, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False)
    
    print(f'YAML file created successfully at: {yaml_path}')
    return yaml_path

def plot_training_results(csv_path):
    """Plot training results from CSV file"""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    
    fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(15, 15))
    
    # Plot training metrics
    sns.lineplot(x='epoch', y='train/box_loss', data=df, ax=axs[0,0])
    sns.lineplot(x='epoch', y='train/cls_loss', data=df, ax=axs[0,1])
    sns.lineplot(x='epoch', y='train/dfl_loss', data=df, ax=axs[1,0])
    sns.lineplot(x='epoch', y='metrics/precision(B)', data=df, ax=axs[1,1])
    sns.lineplot(x='epoch', y='metrics/recall(B)', data=df, ax=axs[2,0])
    sns.lineplot(x='epoch', y='metrics/mAP50(B)', data=df, ax=axs[2,1])
    sns.lineplot(x='epoch', y='metrics/mAP50-95(B)', data=df, ax=axs[3,0])
    sns.lineplot(x='epoch', y='val/box_loss', data=df, ax=axs[3,1])
    sns.lineplot(x='epoch', y='val/cls_loss', data=df, ax=axs[4,0])
    sns.lineplot(x='epoch', y='val/dfl_loss', data=df, ax=axs[4,1])
    
    # Set titles
    axs[0,0].set(title='Train Box Loss')
    axs[0,1].set(title='Train Class Loss')
    axs[1,0].set(title='Train DFL Loss')
    axs[1,1].set(title='Metrics Precision (B)')
    axs[2,0].set(title='Metrics Recall (B)')
    axs[2,1].set(title='Metrics mAP50 (B)')
    axs[3,0].set(title='Metrics mAP50-95 (B)')
    axs[3,1].set(title='Validation Box Loss')
    axs[4,0].set(title='Validation Class Loss')
    axs[4,1].set(title='Validation DFL Loss')
    
    plt.suptitle('Training Metrics and Loss', fontsize=24)
    plt.subplots_adjust(top=0.8)
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main training pipeline"""
    print("Starting YOLOv8n Leaf Detection Training Pipeline")
    print("=" * 50)
    
    # Define paths
    base_dir = "/home/shuttle_01/Desktop/leaf_detector"
    csv_filepath = os.path.join(base_dir, "train.csv")
    train_images_dir = os.path.join(base_dir, "train")
    test_images_dir = os.path.join(base_dir, "test/leaf")
    output_dir = os.path.join(base_dir, "yolo_dataset")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and process data
    print("1. Loading and processing dataset...")
    columns_name = ['image_id', 'width', 'height', 'bbox']
    annotations = csv_to_dataframe(csv_filepath, columns_name)
    df = pd.DataFrame(annotations)
    
    print(f"Total annotations: {len(df)}")
    print(f"Unique images: {len(df['image_id'].unique())}")
    
    # Split dataset
    print("2. Splitting dataset...")
    unique_filenames = df['image_id'].unique()
    train_filenames, val_test_filenames = train_test_split(
        unique_filenames, test_size=0.2, random_state=random_seed
    )
    train_df = df[df['image_id'].isin(train_filenames)]
    
    # 10% for validation and 10% for test
    val_filenames, test_filenames = train_test_split(
        val_test_filenames, test_size=0.5, random_state=random_seed
    )
    val_df = df[df['image_id'].isin(val_filenames)]
    test_df = df[df['image_id'].isin(test_filenames)]
    
    # Print dataset statistics
    train_percentage = calc_percentage(df, train_df, 'image_id')
    val_percentage = calc_percentage(df, val_df, 'image_id')
    test_percentage = calc_percentage(df, test_df, 'image_id')
    
    print(f"Train: {len(train_df['image_id'].unique())} images ({train_percentage:.1f}%)")
    print(f"Validation: {len(val_df['image_id'].unique())} images ({val_percentage:.1f}%)")
    print(f"Test: {len(test_df['image_id'].unique())} images ({test_percentage:.1f}%)")
    
    # Create YOLO dataset structure
    print("3. Creating YOLO dataset structure...")
    
    # Create directories
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)
    
    # Process training data
    train_img_dir = os.path.join(output_dir, 'train', 'images')
    train_label_dir = os.path.join(output_dir, 'train', 'labels')
    move_images_to_directory(train_df, train_images_dir, train_img_dir)
    dataframe_yolofiles(train_df, train_label_dir)
    
    # Process validation data
    val_img_dir = os.path.join(output_dir, 'valid', 'images')
    val_label_dir = os.path.join(output_dir, 'valid', 'labels')
    move_images_to_directory(val_df, train_images_dir, val_img_dir)
    dataframe_yolofiles(val_df, val_label_dir)
    
    # Process test data
    test_img_dir = os.path.join(output_dir, 'test', 'images')
    test_label_dir = os.path.join(output_dir, 'test', 'labels')
    move_images_to_directory(test_df, train_images_dir, test_img_dir)
    dataframe_yolofiles(test_df, test_label_dir)
    
    # Create YAML configuration
    print("4. Creating YAML configuration...")
    yaml_path = create_yaml_config(output_dir)
    
    # Load and train model
    print("5. Loading YOLOv8n model...")
    model = YOLO('yolov8n.pt')
    
    print("6. Starting training...")
    results = model.train(
        data=yaml_path,
        epochs=60,
        imgsz=1024,
        seed=random_seed,
        batch=8,
        workers=4,
        project=os.path.join(base_dir, 'runs'),
        name='leaf_detection'
    )
    
    print("7. Training completed!")
    print(f"Results saved to: {results.save_dir}")
    
    # Plot training results
    print("8. Plotting training results...")
    results_csv = os.path.join(results.save_dir, 'results.csv')
    if os.path.exists(results_csv):
        plot_training_results(results_csv)
    
    # Evaluate model
    print("9. Evaluating model...")
    best_model_path = os.path.join(results.save_dir, 'weights', 'best.pt')
    model = YOLO(best_model_path)
    
    # Evaluate on test set
    metrics = model.val(conf=0.25, split='test')
    print(f"Test mAP50: {metrics.box.map50:.3f}")
    print(f"Test mAP50-95: {metrics.box.map:.3f}")
    
    # Test predictions on sample images
    print("10. Testing predictions on sample images...")
    test_results = model.predict(
        test_images_dir, 
        save=True, 
        imgsz=1024, 
        conf=0.25,
        project=os.path.join(base_dir, 'runs'),
        name='test_predictions'
    )
    
    print("Training pipeline completed successfully!")
    print(f"Best model saved at: {best_model_path}")
    print(f"Test predictions saved to: {os.path.join(base_dir, 'runs', 'test_predictions')}")

if __name__ == "__main__":
    main()
