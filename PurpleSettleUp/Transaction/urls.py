from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('history', views.history, name='history'),
    path('history/<str:slug>', views.single_transaction, name='single_transaction'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('my_debt/', views.my_debt, name='my_debt'),
    path('cancel_debt/', views.cancel_debt, name='cancel_debt'),
    path('repay_debt/', views.repay_debt, name='repay_debt'),
    path('get_payment_method/<str:username>/', views.get_payment_method, name='get_payment_method'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
]
