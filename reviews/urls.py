from django.urls import path
from . import views


urlpatterns = [
    path('add', views.add_review, name='add'),
    path('edit', views.edit_review, name='edit'),
    path('delete', views.delete_review, name='delete'),
]