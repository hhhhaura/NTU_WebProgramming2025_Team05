from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('history/<slug:slug>/', views.single_transaction, name="page"),
    path('history/', views.history),
    path('add_transaction/', views.add_transaction),
]
