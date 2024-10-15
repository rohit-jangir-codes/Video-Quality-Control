from django.urls import path
from .views import UploadVideo, GetVideoIDs, CheckVideoQuality, PlayVideo

urlpatterns = [
    path('upload_video/', UploadVideo.as_view(), name='upload_video'),
    path('get_video_ids/', GetVideoIDs.as_view(), name='get_video_ids'),
    path('check_quality/<str:video_id>/', CheckVideoQuality.as_view(), name='check_video_quality'),
    path('play_video/<str:video_id>/', PlayVideo.as_view(), name='play_video'),
]
