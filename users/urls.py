from django.urls import path
from . import views


urlpatterns = [
    path('user/login', views.login_user, name='login'),

    path('api/register', views.register_user, name='register_user'),
]