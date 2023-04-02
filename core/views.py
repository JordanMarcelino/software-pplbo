import requests
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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
from .forms import UserCreateForm, UserUpdateForm, SetPasswordForm, RekamMedisForm
from .utils import send_email_confirmation, send_reset_password
from .decorators import user_authenticated
# Create your views here.

def index(request):
    return render(request, 'core/home.html')


@user_authenticated
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') if request.POST.get('password') else ""
        recaptcha_response = request.POST.get('g-recaptcha-response') if request.POST.get('g-recaptcha-response') else ""
        resend = request.POST.get('resend')
        
        if resend:
            send_email_confirmation(request, Users.objects.get(Q(username__iexact=email) | Q(email__iexact=email) | Q(nik=email)))
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
                            return redirect('home')
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
            
            if user.jenis_kelamin == "Perempuan":
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

@login_required(login_url='login')
def edit_profile(request):
    form = UserUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'core/profile.html', context=context)

def daftar_dokter(request):
    dokter = Users.objects.filter(is_dokter=True)
    
    context = {'dokter':dokter}
    return render(request, 'core/daftar_dokter.html', context=context)

@login_required(login_url='login')
def daftar_pasien(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    pasien = Users.objects.filter((Q(nik__contains=q) | Q(nama__icontains=q) | Q(email__icontains=q)), is_dokter=False, is_staff=False)
    
    if not request.user.is_dokter and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        page = request.POST.get('page')
    else:
        page = 1
    
    paginator = Paginator(pasien, 10)
    obj = paginator.get_page(page)
    context = {'pasiens': obj , 'page': obj.number, 'next': obj.has_next, 'prev': obj.has_previous, 'total_page': obj.paginator.num_pages}
    
    return render(request, 'core/daftar_pasien.html', context=context)

def faq(request):
    return render(request, 'core/faq.html')

@login_required(login_url='login')
def input_dokter(request):
    dokter = Users.objects.filter(is_dokter=True)
    
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        id = request.POST.get('dokter')
        page = request.POST.get('page')
        
        print(id)
        if id != None:
            print(Users.objects.get(id=id))
    else:
        page = 1
    
    paginator = Paginator(dokter, 5)
    obj = paginator.get_page(page)
    context = {'dokters': obj , 'page': obj.number, 'next': obj.has_next, 'prev': obj.has_previous, 'total_page': obj.paginator.num_pages}
    return render(request, 'core/input_dokter.html', context=context)

@login_required(login_url='login')
def add_dokter(request):
    form = UserCreateForm()
    if not request.user.is_staff:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_dokter = True
            
            if user.jenis_kelamin == "Perempuan":
                user.avatar = "woman.png"
            
            user.save()
            return redirect('input_dokter')
        
    context = {'form': form}
    return render(request, 'core/add_dokter.html', context=context)


@login_required(login_url='login')
def delete_dokter(request, id):
    dokter = Users.objects.get(id=id)
    if not request.user.is_staff:
        return redirect('home')
        
    if request.method == 'POST':
        dokter.delete()
        return redirect('input_dokter')
        
    context = {'dokter':dokter}
    return render(request, 'core/delete_confirmation.html', context=context)

@login_required(login_url='login')
def edit_dokter(request, id):
    dokter = Users.objects.get(id=id)
    form = UserUpdateForm(instance=dokter)
    
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=dokter)
        if form.is_valid():
            form.save()
            return redirect('input_dokter')
    
    
    context = {'form':form, 'page':'edit'}
    return render(request, 'core/add_dokter.html', context=context)


@login_required(login_url='login')
def edit_pasien(request, id):
    pasien = Users.objects.get(id=id)
    form = UserUpdateForm(instance=pasien)
    
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=pasien)
        if form.is_valid():
            form.save()
            return redirect('daftar_pasien')
    
    
    context = {'form':form}
    return render(request, 'core/edit_pasien.html', context=context)


@login_required(login_url='login')
def rekam_medis(request, id):
    user = Users.objects.get(id=id)
    rekam_medis = RekamMedis.objects.filter(pasien=user)
    context = {'rekam_medis':rekam_medis}
    return render(request, 'core/rekam_medis.html', context=context)


@login_required(login_url='login')
def add_rekam_medis(request, id):
    pasien = Users.objects.get(id=id)
    form = RekamMedisForm()
    
    if not request.user.is_dokter:
        return redirect('home')
    
    if request.method == 'POST':
        form = RekamMedisForm(request.POST)
        if form.is_valid():
            rekam_medis = form.save(commit=False)
            rekam_medis.pasien = pasien
            rekam_medis.dokter = request.user.id
            
            rekam_medis.save()
            return redirect('daftar_pasien')
    
    
    context = {'form':form}
    return render(request, 'core/add_rekam_medis.html', context=context)
    

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
