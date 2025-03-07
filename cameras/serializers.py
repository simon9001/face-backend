from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['name', 'location', 'stream_url', 'camera_type', 'face_recognition', 'motion_detection', 'night_vision', 'recording_mode']
    
    # Ensure 'stream_url' and 'camera_type' are required
    stream_url = serializers.CharField(required=True)
    camera_type = serializers.CharField(required=True)

