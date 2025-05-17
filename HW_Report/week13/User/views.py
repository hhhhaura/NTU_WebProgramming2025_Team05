from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import UserForm, ProfileForm
from django.db import transaction
from .models import Notification
from .utils import mark_notification_as_read, get_unread_notifications_count, create_notification
from allauth.account.decorators import verified_email_required
from django.contrib.auth.models import User

@login_required
def namelist(request):
    users = User.objects.all().order_by('username')
    return render(request, 'namelist.html', {'users': users})

@verified_email_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })

@login_required
def mark_as_read(request, notification_id):
    success = mark_notification_as_read(notification_id)
    return JsonResponse({'success': success})

@login_required
def get_notifications_count(request):
    count = get_unread_notifications_count(request.user)
    return JsonResponse({'count': count})