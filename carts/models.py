from django.db import models
from users.models import User
from books.models import Book


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_total_item_price(self):
        return self.quantity * self.book.price

    def get_final_price(self):
        return self.get_total_item_price()

    def __unicode__(self):
        return "Cart item for product " + self.book.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True,
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.book.price * order_item.quantity
        return total
