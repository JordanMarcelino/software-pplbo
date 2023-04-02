from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("login/", views.login_page, name='login'),
    path("register/", views.register_page, name='register'),
    path("logout/", views.logout_page, name='logout'),
    path("profile/", views.edit_profile, name='profile'),
    path("faq/", views.faq, name='faq'),
    path("activate/<str:uidb64>/<str:token>/", views.activate_account, name='activate'),
    path("forgot/", views.forgot_password, name='forgot'),
    path("reset/<str:uidb64>/<str:token>/", views.reset_password, name='reset'),
    path("dokter/", views.daftar_dokter, name='daftar_dokter'),
    path("dokter/list/", views.input_dokter, name='input_dokter'),
    path("dokter/edit/<str:id>/", views.edit_dokter, name='edit_dokter'),
    path("dokter/delete/<str:id>/", views.delete_dokter, name='delete_dokter'),
    path("dokter/add/", views.add_dokter, name='add_dokter'),
    path("pasien/list/", views.daftar_pasien, name='daftar_pasien'),
    path("pasien/edit/<str:id>/", views.edit_pasien, name='edit_pasien'),
    path("pasien/history/<str:id>/", views.rekam_medis, name='rekam_medis'),
    path("pasien/history/add/<str:id>/", views.add_rekam_medis, name='add_rekam_medis'),
]