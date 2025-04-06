from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'success': True, 'username': user.username})
    else:
        return Response({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "註冊成功！"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def me(request):
    if request.user.is_authenticated:
        return JsonResponse({'loggedIn': True, 'username': request.user.username})
    return JsonResponse({'loggedIn': False})
