from django.urls import path
from .views import add_camera
from .views import check_session

urlpatterns = [
    path('cameras/', add_camera, name='add-camera'), 
    path('cameraslst/', check_session , name='camera-list'),
]
