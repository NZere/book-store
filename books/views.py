# views.py
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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
    # Implement your logic to fetch popular books. For example, you could order them by popularity.
    popular_books = Book.objects.all().order_by('-popularity')[:10]  # Adjust as needed.

    serializer = BookSerializer(popular_books, many=True)
    return Response({'message': serializer.data})
