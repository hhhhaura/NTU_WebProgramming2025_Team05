from django.shortcuts import render, redirect, get_object_or_404
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
import json
from django.utils import timezone
from datetime import datetime
import pytz

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
    # Get all non-deleted notifications
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_deleted=False
    ).exclude(
        # Exclude verified payment notifications
        notification_type='payment',
        verification_id__isnull=False,
        title__icontains='verification',
        read=True
    ).order_by('-created_at')
    
    all_users = User.objects.exclude(id=request.user.id).order_by('username')
    
    # Get minimum date for datetime-local input (current time)
    min_date = timezone.now()
    
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'all_users': all_users,
        'min_date': min_date
    })

@login_required
def mark_as_read(request, notification_id):
    success = mark_notification_as_read(notification_id)
    return JsonResponse({'success': success})

@login_required
def get_notifications_count(request):
    count = get_unread_notifications_count(request.user)
    return JsonResponse({'count': count})

@login_required(login_url="/account_login")
@require_http_methods(["POST"])
@csrf_protect
def mark_notification_read(request, notification_id):
    try:
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        recipient_username = data.get('recipient')
        message = data.get('message')
        schedule_date = data.get('schedule_date')
        
        if not recipient_username or not message:
            return JsonResponse({
                'status': 'error',
                'message': 'Recipient and message are required'
            }, status=400)

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Recipient not found'
            }, status=404)

        # Parse schedule date if provided
        created_at = None
        if schedule_date:
            try:
                # Convert string to datetime
                created_at = datetime.fromisoformat(schedule_date.replace('Z', '+00:00'))
                # Make timezone-aware if it isn't already
                if created_at.tzinfo is None:
                    created_at = pytz.UTC.localize(created_at)
                
                # Check if date is in the past
                if created_at < timezone.now():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Cannot schedule message in the past'
                    }, status=400)
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid date format'
                }, status=400)

        # Create notification
        Notification.objects.create(
            recipient=recipient,
            sender=request.user,
            notification_type='message',
            title=f'Message from {request.user.username}',
            message=message,
            created_at=created_at or timezone.now()
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Message scheduled successfully' if created_at else 'Message sent successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def delete_notification(request, notification_id):
    try:
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )
        
        # Don't allow deletion of unread payment verification notifications
        if notification.notification_type == 'payment' and 'verification' in notification.title.lower() and not notification.read:
            return JsonResponse({
                'status': 'error',
                'message': 'Cannot delete unread verification notification'
            }, status=400)
        
        notification.is_deleted = True
        notification.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)