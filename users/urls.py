from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserListView, ProfileView, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),
    path('list/', UserListView.as_view(template_name="users/user_list.html"), name='user_list'),
    #path('user/<int:pk/', UserDetailView.as_view(template_name="users/user_detail.html"), name='user_detail'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='user_profile_update')
]
