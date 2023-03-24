import requests
from itertools import zip_longest
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
from .models import Users, Proxy, Orders, EmailConfirmation, ResetPassword
from .forms import UserCreateForm, UserUpdateForm, ProxyCreateForm, SetPasswordForm
from .utils import send_email_confirmation, send_reset_password
from .decorators import user_authenticated
# Create your views here.

@user_authenticated(redirect_url='proxies')
def index(request):
    return render(request, 'core/home.html')

@user_authenticated
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower() if request.POST.get('email') else ""
        password = request.POST.get('password') if request.POST.get('password') else ""
        recaptcha_response = request.POST.get('g-recaptcha-response') if request.POST.get('g-recaptcha-response') else ""
        resend = request.POST.get('resend')
        
        if resend:
            send_email_confirmation(request, Users.objects.get(email=email))
            messages.success('Email confirmation has been sended')
            return redirect('login')
        else:
            if recaptcha_response:
                data = {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY, 
                    'response': recaptcha_response
                }
                response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                if response.json()['success']:
                    user = authenticate(request, email=email, password=password)     
                    if user is not None:
                        if not user.is_active:
                            return render(request, 'core/check_email.html', {'email':email})
                        else:
                            login(request, user)
                            return redirect('proxies')
                    else:
                        messages.error(request, "Email or Password is wrong!")
            else:
                messages.error(request, "You must pass the reCAPTCHA test!")
        
    context = {'page': 'login', 'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'core/authentication.html', context=context)

@user_authenticated
def register_page(request):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            if user.gender == "Perempuan":
                user.avatar = "woman.png"
            
            user.save()
            send_email_confirmation(request, user)
            # redirect to a page to notify the user to check their email
            return render(request, 'core/check_email.html', {'email':user.email})
            

    return render(request, 'core/authentication.html', {'form':form})


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
    if request.method == 'POST':
        email = request.POST.get('email').lower() if request.POST.get('email') else ""
        recaptcha_response = request.POST.get('g-recaptcha-response') if request.POST.get('g-recaptcha-response') else ""
        
        if recaptcha_response:
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY, 
                'response': recaptcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            if response.json()['success']:
                user = Users.objects.get(email=email)
                send_reset_password(request, user)
                messages.success(request, "We've emailed you a link to reset your password")
                return redirect('login')
        else:
            messages.error(request, "You must pass the reCAPTCHA test!")
    
    context = {'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'core/forgot_password.html', context=context)

@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('home')

@user_authenticated(redirect_url='proxies')
def products(request, type):
    type = " ".join(type.split("-"))
    
    product_list = ["HTTP Proxy", "HTTPS Proxy", "Dedicated Proxy", "SOCKS5 Proxy", "Shared Proxy", "Shared SOCKS5 Proxy"]
    
    proxy = None
    for product in product_list:
        if type == product.lower():
            proxy = product
    
    if proxy is None:
        raise Http404()
    
    context = {'proxy':proxy}
    return render(request, 'core/products.html', context=context)

@login_required(login_url='login')
def proxies(request):
    page = 1
    proxy = Proxy.objects.all()
    total_proxy = proxy.count()
    proxy_zip = list(zip_longest(*([iter(proxy)] * 20), fillvalue=None))
    orders = Orders.objects.filter(user=request.user).count()
    if request.method == 'POST':
        page = request.POST.get('page')
        if int(page) > len(proxy_zip):
            page = len(proxy_zip)
    context = {'proxies':proxy, 'orders':orders, 'total': total_proxy, 'p_zip':len(proxy_zip), 'page': page}
    return render(request, 'core/proxies.html', context=context)


@login_required(login_url='login')
def add_proxies(request):
    form = ProxyCreateForm()
    
    if not request.user.is_staff:
        redirect('home')
    
    
    if request.method == 'POST':
        form = ProxyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proxies')
    
    
    context = {'form':form}
    return render(request, 'core/add_proxies.html', context=context)

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