from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('worker', 'Worker'),
        ('security', 'Security'),
        ('visitor', 'Visitor'),
    ]

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    blacklisted = models.BooleanField(default=False)
    watchlisted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('gatekeeper', 'Gatekeeper'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='gatekeeper')

    def __str__(self):
        return f"{self.username} ({self.role})"

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('worker', 'Worker'),
        ('security', 'Security'),
        ('visitor', 'Visitor'),
    ]

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    blacklisted = models.BooleanField(default=False)
    watchlisted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    from django.db import models

class AuthorizedUser(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    blacklisted = models.BooleanField(default=False)
    watchlisted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Visitor(models.Model):
    name = models.CharField(max_length=255)
    visit_reason = models.TextField(blank=True, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AccessLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    action = models.CharField(max_length=10, choices=[('entry', 'Entry'), ('exit', 'Exit')])
    timestamp = models.DateTimeField(auto_now_add=True)
    authorized = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.action} - {self.timestamp}"
    
class SecurityAlert(models.Model):
    ALERT_TYPES = [
        ('intrusion', 'Intrusion Attempt'),
        ('blacklist', 'Blacklisted Entry'),
        ('watchlist', 'Watchlisted Entry'),
        ('overstay', 'Visitor Overstay'),
        ('visitor_registered', 'New Visitor Registered'),
    ]   

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, verbose_name="Alert Type")  # ✅ Improved Admin Display
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.timestamp}"