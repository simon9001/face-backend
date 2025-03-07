from django.db import models

# Camera Model
class Camera(models.Model):
    NIGHT_VISION_CHOICES = [
        ('auto', 'Auto'),
        ('on', 'Always On'),
        ('off', 'Always Off'),
    ]
    RECORDING_MODE_CHOICES = [
        ('continuous', 'Continuous'),
        ('motion-based', 'Motion-based'),
        ('manual', 'Manual'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    stream_url = models.URLField()
    camera_type = models.CharField(max_length=50, choices=[('IP Camera', 'IP Camera'), ('Webcam', 'Webcam'), ('CCTV', 'CCTV')])
    face_recognition = models.BooleanField(default=False)
    motion_detection = models.BooleanField(default=False)
    night_vision = models.CharField(max_length=10, choices=NIGHT_VISION_CHOICES, default='auto')
    recording_mode = models.CharField(max_length=20, choices=RECORDING_MODE_CHOICES, default='motion-based')
    storage = models.CharField(max_length=50, default='local')

    def __str__(self):
        return self.name

