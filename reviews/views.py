import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review
from books.models import Book


@csrf_exempt
@permission_classes((permissions.AllowAny,))
def add_review(request):
    data = json.loads(request.body)
    print("data", data)
    id = data['id']
    stars = data['stars']
    review_text = data['review']
    print("________________________________")

    try:
        book = Book.objects.get(id=id)
        existing_review = Review.objects.filter(user=request.user, book=book).first()
        if existing_review:
            return JsonResponse({"status": "error", "message": "User has already posted a review"})

        new_review = Review(user=request.user, book=book, stars=stars, review=review_text)
        new_review.save()

        response_data = {
            "status": "success",
            "message": {
                "userId": {
                    "name": request.user.username,
                    "email": request.user.email,
                },
                "stars": stars,
                "review": review_text,
            }
        }
        return JsonResponse(response_data)

    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Book not found"})

@csrf_exempt
@permission_classes((permissions.AllowAny,))
def edit_review(request):
    data = json.loads(request.body)
    id = data.get('id')
    stars = data.get('stars')
    review_text = data.get('review')

    try:
        review = Review.objects.get(book_id=id, user=request.user)
        print(review)
        review.stars = stars or review.stars
        print(review.review)
        review.review = review_text or review.review
        review.save()
        print(review.review)

        response_data = {
            "status": "success",
            "message": {
                "userId": {
                    "name": request.user.username,
                    "email": request.user.email,
                },
                "stars": review.stars,
                "review": review.review,
            }
        }
        print(review.review)
        return JsonResponse(response_data)
    except Review.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Review not found or you don't have permission to edit it"})


@csrf_exempt
@permission_classes((permissions.AllowAny,))
def delete_review(request):
    data = json.loads(request.body)
    id = data.get('id')
    try:
        review = Review.objects.get(book_id=id, user=request.user)
        review.delete()
        return JsonResponse({"status": "success", "message": "Deleted successfully"})
    except Review.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Review not found or you don't have permission to delete it"})

