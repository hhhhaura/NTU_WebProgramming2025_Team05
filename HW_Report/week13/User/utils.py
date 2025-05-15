from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Notification
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_smtp_email(to_email, subject, html_content):
    """
    Send email using SMTP directly.
    """
    print(f"Attempting to send SMTP email to {to_email} with subject: {subject}")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email

    # Create both plain text and HTML versions
    text_content = strip_tags(html_content)
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        # Create SMTP connection
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email via SMTP: {str(e)}")
        return False

def create_notification(user, notification_type, title, message, send_email=True):
    """
    Create a notification and optionally send an email.
    """
    # Create notification object
    notification = Notification.objects.create(
        recipient=user,
        notification_type=notification_type,
        title=title,
        message=message
    )

    if send_email and user.email:  # Only send if user has an email address
        # Prepare email content
        html_message = render_to_string('notification_email.html', {
            'user': user,
            'title': title,
            'message': message,
            'notification_type': notification.get_notification_type_display()
        })

        # Send email using SMTP
        subject = f'Roommate Accounting System - {title}'
        email_sent = send_smtp_email(user.email, subject, html_message)
        
        if email_sent:
            print(f"Successfully sent email notification to {user.email}")
            notification.email_sent = True
            notification.save()

    return notification

def mark_notification_as_read(notification_id):
    """
    Mark a notification as read.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.read = True
        notification.save()
        return True
    except Notification.DoesNotExist:
        return False

def get_unread_notifications_count(user):
    """
    Get the count of unread notifications for a user.
    """
    return Notification.objects.filter(recipient=user, read=False).count() 