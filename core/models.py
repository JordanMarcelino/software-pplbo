from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import pytz
from datetime import date

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
    nama = models.CharField(_('nama lengkap'), max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(_('avatar'), null=True, default="man.png")
    jenis_kelamin = models.CharField(_('jenis kelamin'), max_length=255, choices=jenis_kelamin)
    nik = models.CharField(_('NIK'), max_length=255, unique=True)
    no_telepon = models.CharField(_('no telepon'), max_length=255, unique=True)
    alamat = models.TextField(_('alamat'), blank=True, null=True)
    tanggal_lahir = models.DateField()
    golongan_darah = models.CharField(_('golongan darah'), max_length=10, choices=golongan_darah)
    agama = models.CharField(_('agama'), max_length=50, choices=agama)
    is_dokter = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.tanggal_lahir.year - ((today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day))
    
    @property
    def first_name(self):
        return self.nama.split(" ")[0]
    
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
    COUNTER = 1
    
    id = models.UUIDField(_('id'), default=uuid4, primary_key=True)
    pasien = models.ForeignKey(Users, on_delete=models.CASCADE)
    dokter = models.IntegerField()
    nomor = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-nomor']

    def is_expired(self):
        tz = pytz.timezone('Asia/Jakarta')
        time_difference = timezone.now().astimezone(tz) - self.created_at

        return time_difference.total_seconds() > 900

        
    def increment_counter():
        Queue.COUNTER += 1
        
    def reset_counter():
        Queue.COUNTER = 1

    @property
    def doctor(self):
        doc = Users.objects.get(id=self.dokter)
        
        return doc.username
    
class RekamMedis(models.Model):
    id = models.UUIDField(_('id'), default=uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pasien = models.ForeignKey(Users, on_delete=models.CASCADE)
    dokter = models.IntegerField()
    keluhan = models.TextField(_('keluhan'), blank=True, null=True)
    diagnosa = models.TextField(_('diagnosa'), blank=True, null=True)
    obat = models.TextField(_('obat'), blank=True, null=True)
    riwayat_penyakit = models.TextField(_('riwayat penyakit'), blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    @property
    def doctor(self):
        doc = Users.objects.get(id=self.dokter)
        
        return doc.username
    