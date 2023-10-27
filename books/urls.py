from django.urls import path
from . import views
from .views import BookDetailView

urlpatterns = [
    path('', views.index),
    path('<int:book_id>', BookDetailView.as_view(), name='book-detail'),
    path('popularnow', views.popular_books, name='popular_books'),
    path('category/<str:category_name>', views.categories, name='categories'),
]