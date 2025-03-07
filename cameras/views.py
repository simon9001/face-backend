from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import CameraSerializer
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
import json


@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([AllowAny]) 
def check_session(request):
    if request.user.is_authenticated:
        return Response({"status": "Session valid"})
    return Response({"status": "Session invalid"}, status=403)


@api_view(['POST'])
@permission_classes([AllowAny])  
def add_camera(request):
    """API to add a new camera"""
    serializer = CameraSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Validation errors:", serializer.errors)  # Print validation errors
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
