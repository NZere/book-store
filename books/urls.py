from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('popularnow', views.popular_books, name='popular_books'),
]