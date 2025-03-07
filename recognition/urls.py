from django.urls import path
from .views import (
    get_csrf_token, switch_user, user_login, user_logout, check_session,
    add_user, get_users, update_user, delete_user, get_user_distribution
)

urlpatterns = [
    #CSRF Token
    path('csrf/', get_csrf_token, name='csrf-token'),
    path('users/add/', add_user, name='add-user'),
    path('users/', get_users, name='get-users'),
    path('users/update/<int:user_id>/', update_user, name='update-user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete-user'),
    path('users/distribution/', get_user_distribution, name='user-distribution'),
    path('switch-user/', switch_user, name='switch-user'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('check-session/', check_session, name='check-session'),
]
