from django.db import models
from main.models import Book, Customer
from checkout.models import Order

# Create your models here.


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name=(
        "book_id"), on_delete=models.CASCADE, default=None, )
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=1)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)

    @staticmethod
    def add_to_cart(book_id, request):
        user = request.user
        book = Book.objects.get(id=book_id)
        if user in [cart.customer for cart in Cart.objects.all()]:
            if book in [cart.book for cart in Cart.objects.filter(customer=user, is_ordered=False)]:
                cart = Cart.objects.get(book=book, customer=user)
                cart.quantity = cart.quantity + 1
                cart.total = cart.book.price * cart.quantity
                cart.save()
            else:
                cart = Cart.objects.create(
                    customer=user, book=book, quantity=1, total=book.price)
                cart.save()
        else:
            cart = Cart.objects.create(
                customer=user, book=book, quantity=1, total=book.price)
            cart.save()
