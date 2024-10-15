import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
from skimage.metrics import structural_similarity as ssim

def compute_ssim(img1, img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(gray_img1, gray_img2)

def load_data(video_folder):
    frame_pairs = []
    labels = []  # Placeholder for actual MOS scores

    for video_file in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_file)
        frames = extract_frames(video_path)

        for i in range(len(frames) - 1):
            img1 = cv2.imread(frames[i])
            img2 = cv2.imread(frames[i + 1])
            ssim_value = compute_ssim(img1, img2)
            frame_pairs.append(ssim_value)

        labels.append(1.0)  # Placeholder for actual labels

    return np.array(frame_pairs), np.array(labels)

def create_model():
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(1,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)  # Output quality score
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == '__main__':
    video_folder = 'dataset/train/videos/'
    X_train, y_train = load_data(video_folder)
    model = create_model()
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
    model.save('vqeg_video_quality_model.h5')
