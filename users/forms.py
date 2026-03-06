from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("email", "avatar", "phone", "country")


class UserModeratorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("is_active",)
