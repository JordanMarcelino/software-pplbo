from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import Users
from django.db.models import Q

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Q(username__iexact=email) | Q(email__iexact=email) | Q(nik=email))
        except Users.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
