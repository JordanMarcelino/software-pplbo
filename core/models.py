from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import pytz

# Create your models here.

jenis_kelamin = (
    ('Laki-Laki', 'Laki-Laki'),
    ('Perempuan', 'Perempuan')
)
golongan_darah = (
    ('O', 'O'),
    ('A', 'A'),
    ('B', 'B'),
    ('AB', 'AB'),
)
agama = (
    ('Islam', 'Islam'),
    ('Kristen', 'Kristen'),
    ('Katolik', 'Katolik'),
    ('Budha', 'Budha'),
    ('Konghucu', 'Konghucu'),
)

class Users(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(_('avatar'), null=True, default="man.png")
    jenis_kelamin = models.CharField(_('gender'), max_length=255, choices=jenis_kelamin)
    nik = models.CharField(_('nik'), max_length=255, unique=True)
    no_telepon = models.CharField(max_length=255, unique=True)
    alamat = models.CharField(max_length=255)
    tanggal_lahir = models.DateTimeField()
    golongan_darah = models.CharField(max_length=10, choices=golongan_darah)
    agama = models.CharField(max_length=50, choices=agama)
    is_dokter = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class EmailConfirmation(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=255)
    confirmed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        tz = pytz.timezone('Asia/Jakarta')
        time_difference = timezone.now().astimezone(tz) - self.updated_at

        return time_difference.total_seconds() > 7200

    def __str__(self):
        return self.user.username
    
class ResetPassword(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        tz = pytz.timezone('Asia/Jakarta')
        time_difference = timezone.now().astimezone(tz) - self.updated_at

        return time_difference.total_seconds() > 300

    def __str__(self):
        return self.user.username
    
    
class Queue(models.Model):
    id = models.UUIDField(_('id'), default=uuid4, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    nomor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        tz = pytz.timezone('Asia/Jakarta')
        time_difference = timezone.now().astimezone(tz) - self.created_at

        return time_difference.total_seconds() > 600

    def __str__(self):
        return self.user.username
    
class RekamMedis(models.Model):
    id = models.UUIDField(_('id'), default=uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dokter = models.ForeignKey(Users, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    keluhan = models.TextField(blank=True, null=True)
    diagnosa = models.TextField(blank=True, null=True)
    obat = models.TextField(blank=True, null=True)
    riwayat_penyakit = models.TextField(blank=True, null=True)
    