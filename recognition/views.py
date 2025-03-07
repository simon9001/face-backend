from datetime import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AccessLog, SecurityAlert, User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
import json
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserProfileSerializer

@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['POST'])
def switch_user(request):
    """Simulates switching between Admin & Gatekeeper roles"""
    role = request.data.get('role')

    if role not in ['admin', 'gatekeeper']:
        return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.role = role
    user.save()

    return Response({'message': f'Switched to {role}', 'user': UserProfileSerializer(user).data})


@api_view(['POST'])
@permission_classes([AllowAny]) 
@parser_classes([MultiPartParser, FormParser])  
def add_user(request):
    """API to add a new user"""
    serializer = UserProfileSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

@csrf_exempt  # ✅ Disable CSRF for login
@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ Allow all users to call this API
def user_login(request):
    """Login API using username & password"""
    
    try:
        data = json.loads(request.body.decode("utf-8"))  # ✅ Ensure request body is parsed correctly
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Log in user
            return Response({'message': 'Login successful', 'user': {'username': user.username, 'role': user.role}})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def user_logout(request):
    """Logout API"""
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_session(request):
    """Check if a user is already logged in"""
    if request.user.is_authenticated:
        return Response({'user': UserProfileSerializer(request.user).data})
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])  # ✅ Allow access without authentication
def get_user_distribution(request):
    """Retrieve user role distribution"""
    user_roles = User.objects.values_list('role', flat=True)
    role_distribution = {}

    for role in user_roles:
        role_distribution[role] = role_distribution.get(role, 0) + 1

    return Response(role_distribution)

@api_view(['GET'])
@permission_classes([AllowAny])  # ✅ Make this API publicly accessible
def get_users(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    serializer = UserProfileSerializer(user, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a user
@api_view(['DELETE'])
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_dashboard_stats(request):
    today = timezone.now().date()
    
    total_users = User.objects.count()
    today_entries = AccessLog.objects.filter(timestamp__date=today, action='entry').count()
    unread_alerts = SecurityAlert.objects.filter(alert_type='intrusion').count()
    unauthorized_attempts = AccessLog.objects.filter(authorized=False).count()

    return Response({
        "total_users": total_users,
        "today_entries": today_entries,
        "unread_alerts": unread_alerts,
        "unauthorized_attempts": unauthorized_attempts
    })

# 🚀 Fetch User Distribution
@api_view(['GET'])
def get_user_distribution(request):
    user_roles = User.objects.values_list('role', flat=True)
    role_distribution = {}

    for role in user_roles:
        role_distribution[role] = role_distribution.get(role, 0) + 1

    return Response(role_distribution)

# 🚀 Fetch Security Alerts Distribution
@api_view(['GET'])
def get_alert_distribution(request):
    alert_types = SecurityAlert.objects.values_list('alert_type', flat=True)
    alert_distribution = {}

    for alert in alert_types:
        alert_distribution[alert] = alert_distribution.get(alert, 0) + 1

    return Response(alert_distribution)

# 🚀 Fetch Recent Activity Logs
@api_view(['GET'])
def get_recent_activity_logs(request):
    logs = AccessLog.objects.all().order_by('-timestamp')[:5]

    log_data = [{
        "id": log.id,
        "userName": log.user_name,
        "userRole": log.user_role,
        "action": log.action,
        "location": "Main Gate",  # Placeholder, can be updated dynamically
        "timestamp": log.timestamp.isoformat(),
        "authorized": log.authorized
    } for log in logs]

    return Response(log_data)