from rest_framework import serializers
from django.conf import settings
from .models import Visitor
from .models import UserProfile
from .models import AuthorizedUser

class UserProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'role', 'image', 'image_url', 'blacklisted', 'watchlisted', 'notes']

    def get_image_url(self, obj):
        """
        Returns the full URL of the user's profile image.
        """
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
   

class AuthorizedUserSerializer(serializers.ModelSerializer):
    color_code = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()  # New field for full image URL

    class Meta:
        model = AuthorizedUser
        fields = ['id', 'name', 'role', 'color_code', 'image', 'image_url']  # Include image_url

    def get_color_code(self, obj):
        return obj.get_color_code()

    def get_image_url(self, obj):
        """
        Returns the absolute URL of the user's image.
        If no image is available, returns None.
        """
        if obj.image:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.image.url) if request else f"{settings.MEDIA_URL}{obj.image.url}"
        return None

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['id', 'name', 'granted_by', 'expiration_time']


