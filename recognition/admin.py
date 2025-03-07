from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, CustomUser, User, AuthorizedUser, Visitor

# ✅ Register CustomUser (Admin & Gatekeeper Roles)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# ✅ Register UserProfile (Monitored Users)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'blacklisted', 'watchlisted')
    search_fields = ('name', 'role')
    list_filter = ('role', 'blacklisted', 'watchlisted')

# ✅ Register User (Monitored System Users)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'blacklisted', 'watchlisted')
    search_fields = ('name', 'role')
    list_filter = ('role', 'blacklisted', 'watchlisted')

# ✅ Register AuthorizedUser (Users with images, blacklist & watchlist status)
@admin.register(AuthorizedUser)
class AuthorizedUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'blacklisted', 'watchlisted')
    search_fields = ('name', 'role')
    list_filter = ('role', 'blacklisted', 'watchlisted')

# ✅ Register Visitor (Tracking Visitors & Visit Reasons)
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'visit_reason', 'visit_date')
    search_fields = ('name', 'visit_reason')
    list_filter = ('visit_date',)
