from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("login/", views.login_page, name='login'),
    path("register/", views.register_page, name='register'),
    path("logout/", views.logout_page, name='logout'),
    path("activate/<str:uidb64>/<str:token>/", views.activate_account, name='activate'),
    path("forgot/", views.forgot_password, name='forgot'),
    path("reset/<str:uidb64>/<str:token>/", views.reset_password, name='reset'),
    path("dokter/", views.daftar_dokter, name='daftar_dokter'),
]