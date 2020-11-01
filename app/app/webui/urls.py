from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.StatusView.as_view(), name='status'),
    path('zoom/', views.ZoomView.as_view(), name='zoom'),
    path('first-run/', views.FirstRunView.as_view(), name='first_run'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('login/', auth_views.LoginView.as_view(
        extra_context={'hide_nav': True, 'title': 'Login', 'submit_text': 'Login'}, redirect_authenticated_user=True,
        template_name='webui/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.PasswordChangeView.as_view(), name='password_change'),
    re_path('^(?P<module>logs|websockify|sshwifty|sse)', views.nginx_protected, name='nginx_protected'),
]
