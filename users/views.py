import json

# from django.contrib.auth.models import User
from users.models import User

from django.core.exceptions import ValidationError
import bcrypt

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

# @xframe_options_exempt
@csrf_exempt
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def my_authenticated_view(request, is_superuser=False):
    print(request.path)

    print("hi")

    if request.user.is_authenticated:
        print("is_authenticated", request.user.is_authenticated)
        if is_superuser:
            if not request.user.is_superuser:
                response_data = {
                    "status": "error",
                    "message": "You are not logged in.(admin)",
                }
        user_data = {
            "cartItems": [],  # Replace with actual user data as needed
            "email": request.user.email,
            "isUser": request.user.is_active,  # Adjust based on your user model
            "name": request.user.first_name,
            "_id": request.user.id,
        }

        response_data = {
            "status": "success",
            "message": "You are logged in.",
            "user": user_data,
        }
    else:
        response_data = {
            "status": "error",
            "message": "You are not logged in.",
        }

    return JsonResponse(response_data)

@csrf_exempt
def my_authenticated_admin_view(request):
    return my_authenticated_view(request, is_superuser=True)



@csrf_exempt  # Remove this decorator in production; it's used to disable CSRF protection for simplicity.
def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        plain_password = request.POST.get('password')

        # Validation
        if not name or not email or not plain_password:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        if User.objects.filter(username=email).exists():
            return JsonResponse({'status': 'error', 'message': 'User has already been registered.'}, status=400)

        if len(plain_password) < 6:
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 6 characters.'}, status=400)

        # Hash the password
        password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User registered.'}, status=200)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': e.messages}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def login_user(request):
    print("hh")
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        email = request_data.get('email')
        plain_password = request_data.get('password')
        temp_user = User.objects.all()
        user = authenticate(request, username=temp_user[0].username, password=plain_password)
        if user is not None:
            login(request, user)
            user_data = {
                'cartItems': [],  # Replace with user-specific data
                'email': user.email,
                'isUser': user.is_active,  # Adjust based on your user model
                'name': user.first_name,
                '_id': user.id,
            }

            return JsonResponse({
                'status': 'success',
                'message': f'You have been logged in as {user.first_name}',
                'user': user_data,
            }, status=200)

        return JsonResponse({'status': 'error', 'message': 'Invalid login credentials.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

