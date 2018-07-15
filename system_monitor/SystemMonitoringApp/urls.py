from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/', views.signup, name='app_signup'),
    path('login/', LoginView.as_view(template_name = 'SystemMonitoringApp/login.html'), name = 'app_login'),
    path('logout/', auth_views.logout, name = 'app_logout'),
    path('details/', views.details, name = 'app_details'),
    path('validate/', views.custom_login, name = 'app_custom_validate'),
    path('poll/', views.poll, name = 'app_poll')
]