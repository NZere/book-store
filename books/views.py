# views.py
import json
import urllib.parse

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from users.models import User
from users.serilaizers import UserSerializer
from .models import Book
from .serializers import BookSerializer

@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def index(request):
    return Response({'message': "hi"})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def popular_books(request):
    print("hey books")
    popular_books = Book.objects.all().order_by('-popularity')[:10]

    print("====================================")
    serializer = BookSerializer(popular_books, many=True)
    for data in serializer.data:
        print(data["price"])
        print(data["image"])
        data["authors"] = json.loads(data["authors"])
        data["_id"] = data["id"]
        image = urllib.parse.unquote(data["image"])
        data["image"] = image[1:] if image[0] == '/' else image
        print(data["image"])
    return Response({'message': serializer.data})


class BookDetailView(View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            # reviews = book.reviews.select_related('userId').only('userId__name', 'userId__email')
            # serialized_reviews = [{"name": review.userId.name, "email": review.userId.email} for review in reviews]
            serializer = BookSerializer(book)
            data = serializer.data
            data["authors"] = json.loads(data["authors"])
            data["_id"] = data["id"]
            image = urllib.parse.unquote(data["image"])
            data["image"] = image[1:] if image[0] == '/' else image
            reviews = Review.objects.filter(book_id=book.id)
            data["reviews"] = []
            for review in reviews:
                ser_review = ReviewSerializer(review).data
                ser_review["_id"] = ser_review["id"]
                data["reviews"].append(ser_review)
                user = User.objects.get(id=ser_review["user"])
                ser_review["userId"] = UserSerializer(user).data
                ser_review["userId"]["_id"]=ser_review["userId"]["id"]

            print(data["image"])
            print(data)
            return JsonResponse({"status": "success", "message": data})
        except Book.DoesNotExist:
            raise Http404("Book does not exist")


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def categories(request, category_name):
    print(category_name.lower())
    books = Book.objects.filter(category=category_name.lower()).order_by('-popularity')[:10]

    print("====================================")
    serializer = BookSerializer(books, many=True)
    for data in serializer.data:
        print(data["price"])
        print(data["image"])
        data["authors"] = json.loads(data["authors"])
        data["_id"] = data["id"]
        image = urllib.parse.unquote(data["image"])
        data["image"] = image[1:] if image[0] == '/' else image
        print(data["image"])
    return Response({'message': serializer.data})