from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Users, Queue, RekamMedis
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from django.utils.translation import gettext_lazy as _

class UserCreateForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    tanggal_lahir = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'min':'1900-01-01'}))
    class Meta:
        model = Users
        fields = ['nik', 'username', 'email', 'alamat', 'tanggal_lahir', 'golongan_darah', 'no_telepon', 'avatar', 'jenis_kelamin', 'agama', 'password1', 'password2']

    
class UserUpdateForm(ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'avatar', 'alamat', 'tanggal_lahir', 'golongan_darah', 'no_telepon', 'jenis_kelamin', 'agama']


class SetPasswordForm(SetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = Users
        fields = ['new_password1', 'new_password2']