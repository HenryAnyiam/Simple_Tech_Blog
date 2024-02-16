from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .models import User

class CustomUserAuth(ModelBackend):
    """Build a custom user authentication"""

    def authenticate(self, request: HttpRequest,
                     username: str, password: str, **kwargs) -> User:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None