import requests
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.http import Http404
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Users, EmailConfirmation, ResetPassword, Queue, RekamMedis
from .forms import UserCreateForm, UserUpdateForm, SetPasswordForm
from .utils import send_email_confirmation, send_reset_password
from .decorators import user_authenticated
# Create your views here.

def index(request):
    return render(request, 'core/home.html')


@user_authenticated
def login_page(request):
    return render(request, 'core/authentication.html')


@user_authenticated
def register_page(request):
    return render(request, 'core/authentication.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(email=uid)
        email_confirmation = EmailConfirmation.objects.get(user=user)
    except:
        user = None

    if user is not None and token == email_confirmation.confirmation_code and not email_confirmation.is_expired():
        user.is_active = True
        email_confirmation.confirmed = True
        user.save()
        email_confirmation.save()
        
        messages.success(request, "Your account has been activated, now you can login your account!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
        
    return redirect('login')
        
        
@user_authenticated    
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(email=uid)
        reset_password = ResetPassword.objects.get(user=user)
    except:
        user = None

    if user is not None and token == reset_password.confirmation_code and not reset_password.is_expired():
        form = SetPasswordForm(user)
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)    
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You can login to your account")
                return redirect('login')
            else:
                return render(request, "core/change_password.html", {'form':form})
        else:
            return render(request, "core/change_password.html", {'form':form})
    else:
        messages.error(request, "Reset password link is invalid!")
        
    return redirect('login')


@user_authenticated
def forgot_password(request):
    return render(request, 'core/forgot_password.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('home')


def error_handler(request, exception=None, status_code=None):
    if status_code == 400:
        error_message = "Bad Request"
    elif status_code == 403:
        error_message = "Forbidden"
    elif status_code == 404:
        error_message = "Page not found"
    else:
        error_message = "Server Error"
        
    context = {'status_code':status_code, 'error_message':error_message}
    return render(request, "core/error.html", status=status_code, context=context)
