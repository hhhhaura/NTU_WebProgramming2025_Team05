from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('namelist/', views.namelist),
]