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
    print(f"Using EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"Using EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"Using EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_USE_TLS is set to: {settings.EMAIL_USE_TLS}")
    
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
        print("Attempting to create SMTP connection...")
        # Create SMTP connection
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            print("SMTP connection created successfully")
            print("Attempting to start TLS...")
            server.starttls()  # Enable TLS
            print("TLS started successfully")
            print("Attempting to login...")
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print("Login successful")
            print("Attempting to send message...")
            server.send_message(msg)
            print("Message sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email via SMTP: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def create_notification(user, notification_type, title, message, send_email=False, verification_id=None):
    """
    Create a notification for a user.
    
    Args:
        user: User object - the recipient of the notification
        notification_type: str - type of notification (debt, payment, reminder, system)
        title: str - notification title
        message: str - notification message
        send_email: bool - whether to send an email notification
        verification_id: int - optional ID for payment verifications
    """
    notification = Notification.objects.create(
        recipient=user,
        notification_type=notification_type,
        title=title,
        message=message,
        email_sent=False,
        verification_id=verification_id
    )

    if send_email:
        try:
            # Send email logic here
            subject = title
            body = message
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            # Create plain text and HTML versions
            text = body
            html = f"""
            <html>
              <body>
                <h2>{title}</h2>
                <p>{message}</p>
              </body>
            </html>
            """

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
            notification.email_sent = True
            notification.save()
        except Exception as e:
            print(f"Failed to send email notification: {e}")

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