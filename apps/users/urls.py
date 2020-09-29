from django.contrib.auth.views import PasswordResetView
from django.urls import path
from django.views.generic import TemplateView

from apps.users.views import LoginView, LogoutView, ProfileView, RegisterView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset/', PasswordResetView.as_view(
        template_name='users/reset.html',
        success_url='/users/reset/done/'
    ), name='pw_reset'),
    path('reset/done/', TemplateView.as_view(
        template_name='users/reset_done.html'
    ), name='pw_reset_done'),

]
