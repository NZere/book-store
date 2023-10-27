from django.urls import path
from . import views


urlpatterns = [
    path('user/login', views.login_user, name='login'),
    path('admin/login', views.login_admin, name='login_admin'),
    path('admin/login/verify-otp', views.login_admin, name='verify_otp'),
    path('user/logout', views.logout_view, name='logout'),
    path('api/register', views.register_user, name='register_user'),
]