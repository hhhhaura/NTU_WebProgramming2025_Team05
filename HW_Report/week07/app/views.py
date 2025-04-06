from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(
        request, username=data['username'], password=data['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'success': True, 'username': user.username})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


def me(request):
    if request.user.is_authenticated:
        return JsonResponse({'loggedIn': True, 'username': request.user.username})
    return JsonResponse({'loggedIn': False})
