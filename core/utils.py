from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import EmailConfirmation, ResetPassword

def send_email_confirmation(request, user):
    email_token = account_activation_token.make_token(user)
    email_confirmation = EmailConfirmation.objects.update_or_create(user=user, confirmation_code=email_token)
    email_confirmation_url = request.build_absolute_uri(
        f'/activate/{urlsafe_base64_encode(force_bytes(user.email))}/{email_token}/'
    )

    email_subject = 'Confirm your email address'
    email_body = render_to_string('core/email_confirmation.html', {'email_confirmation_url': email_confirmation_url, 'username': user.username})
    email_messages = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to=[user.email])
    email_messages.send()

def send_reset_password(request, user):
    email_token = account_activation_token.make_token(user)
    reset_password = ResetPassword.objects.update_or_create(user=user, confirmation_code=email_token)
    reset_password_url = request.build_absolute_uri(
        f'/reset/{urlsafe_base64_encode(force_bytes(user.email))}/{email_token}/'
    )

    email_subject = 'Reset password'
    email_body = render_to_string('core/reset_password.html', {'reset_password_url': reset_password_url, 'username': user.username})
    email_messages = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to=[user.email])
    email_messages.send()