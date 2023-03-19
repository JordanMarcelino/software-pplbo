from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Users, Queue, RekamMedis
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField

class UserCreateForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = Users
        fields = ['nik', 'username', 'email', 'alamat', 'tanggal_lahir', 'golongan_darah', 'no_telepon', 'avatar', 'gender', 'agama', 'password1', 'password2']

    
class UserUpdateForm(ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'avatar', 'alamat', 'tanggal_lahir', 'golongan_darah', 'no_telepon', 'gender', 'agama']


class SetPasswordForm(SetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = Users
        fields = ['new_password1', 'new_password2']