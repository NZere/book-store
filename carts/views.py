from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User  # Import your User model
from books.models import Book  # Import your Book model
from carts.models import CartItem, Cart
from django.utils import timezone

def index():
    pass

@csrf_exempt  # For simplicity, you can use @csrf_exempt for this example
def add_to_cart(request, book_id):
    user = request.user  # Assuming you're using Django's built-in authentication
    book = get_object_or_404(Book, id=int(book_id))

    # Check if the book is already in the user's cart
    order_item, created = CartItem.objects.get_or_create(
        book=book,
        user=request.user,
        is_ordered=False,
        price=0,
        quantity=0,
    )
    order_qs = Cart.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(cart__items__book_id=book_id).exists():
            order_item.quantity += 1
            order_item.price += book.price
            order_item.save()
            return JsonResponse({'status': 'success', 'message': 'Item added to cart successfully'})
        else:
            order_item.price = book.price
            order.items.add(order_item)
            return JsonResponse({'status': 'success', 'message': 'Item added to cart successfully'})
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

    return JsonResponse({'status': 'failed', 'message': 'Item not added to cart'})








@csrf_exempt
def remove_from_cart(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)

    order_qs = Cart.objects.filter(
        user=user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(cart__items__book_id=book_id).exists():
            try:
                order_item = CartItem.objects.filter(
                    book=book,
                    user=user,
                    is_ordered=False
                ).first()
                order.items.remove(order_item)
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Item removed from cart successfully'})
            except Exception as e:
                print("error", e)
        else:
            return JsonResponse({'status': 'failed', 'message': 'his item was not in your cary'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'his item was not in your cary'})
