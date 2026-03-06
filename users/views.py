import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
)

from users.forms import UserRegisterForm, UserProfileForm, UserModeratorForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserListView(ListView, LoginRequiredMixin):
    model = User
    template_name = "users/user_list.html"  # Укажите ваш шаблон
    context_object_name = "users"  # Имя переменной в шаблоне


# class UserDetailView(DetailView, LoginRequiredMixin):
#     model = User
#     template_name = 'users/user_detail.html'
#     context_object_name = 'user_object'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("mailing:dispatch_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object:
            return UserProfileForm
        if user.has_perm("mailing.can_stop_dispatch"):
            return UserModeratorForm
        raise PermissionDenied
