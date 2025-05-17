from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('namelist/', views.namelist, name='namelist'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/count/', views.get_notifications_count, name='get_notifications_count'),
    path('send-message/', views.send_message, name='send_message'),
]