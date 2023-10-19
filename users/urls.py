from django.urls import path
from . import views


urlpatterns = [
    path('user/login', views.login_user, name='login'),
    path('user/logout', views.logout_view, name='logout'),
    path('api/register', views.register_user, name='register_user'),
]