from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('namelist/', views.namelist, name='namelist'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_notification_as_read'),
    path('notifications/count/', views.get_notifications_count, name='get_notifications_count'),
]