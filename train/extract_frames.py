import cv2
import os

def extract_frames(video_path, output_folder='frames', frame_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    frame_paths = []
    count = 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frame_path = f'{output_folder}/frame_{count}.jpg'
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
        count += 1

    cap.release()
    return frame_paths
