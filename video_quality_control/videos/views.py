import os
import numpy as np
import cv2
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.conf import settings
from .models import Video
from django.core.files.storage import FileSystemStorage
from bson import ObjectId
from pymongo import MongoClient
from skimage.metrics import structural_similarity as ssim
from tensorflow.keras.models import load_model

# Load the pre-trained model
model = load_model('vqeg_video_quality_model.h5')

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['video_db']
videos_collection = db['videos']

def extract_frames(video_path, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def compute_ssim(img1, img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(gray_img1, gray_img2)

class UploadVideo(View):
    def post(self, request):
        if 'video' not in request.FILES:
            return JsonResponse({"error": "No video file provided"}, status=400)

        video_file = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Insert video info into MongoDB
        video_info = {"filename": filename, "path": file_path}
        inserted_id = videos_collection.insert_one(video_info).inserted_id

        return JsonResponse({"message": "Video uploaded successfully", "video_id": str(inserted_id)}, status=200)

class GetVideoIDs(View):
    def get(self, request):
        video_ids = [str(video['_id']) for video in videos_collection.find({}, {"_id": 1})]
        return JsonResponse({"video_ids": video_ids}, status=200)

class CheckVideoQuality(View):
    def get(self, request, video_id):
        try:
            video_info = videos_collection.find_one({"_id": ObjectId(video_id)})
            if not video_info:
                return JsonResponse({"error": "Video not found"}, status=404)
        except:
            return JsonResponse({"error": "Invalid video ID format"}, status=400)

        video_path = video_info['path']
        frames = extract_frames(video_path)

        ssim_scores = []
        for i in range(len(frames) - 1):
            ssim_value = compute_ssim(frames[i], frames[i + 1])
            ssim_scores.append(ssim_value)

        avg_ssim = np.mean(ssim_scores)
        predicted_quality = model.predict(np.array([avg_ssim]))

        return JsonResponse({"average_ssim": avg_ssim, "predicted_quality": predicted_quality[0][0]}, status=200)

class PlayVideo(View):
    def get(self, request, video_id):
        try:
            video_info = videos_collection.find_one({"_id": ObjectId(video_id)})
            if not video_info:
                return JsonResponse({"error": "Video not found"}, status=404)
        except:
            return JsonResponse({"error": "Invalid video ID format"}, status=400)

        video_path = video_info['path']
        if not os.path.exists(video_path):
            return JsonResponse({"error": "Video file not found"}, status=404)

        with open(video_path, 'rb') as video:
            response = HttpResponse(video.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'inline; filename={video_info["filename"]}'
            return response
