from django.shortcuts import render, redirect
from main.models import Book
from .models import Cart
from django.contrib import messages
from main.views import cart_items
# Create your views here.


def cart(request, book_id):
    user = request.user
    if user.is_authenticated:

        if book_id == '0':
            cart_objs = Cart.objects.filter(customer=user)
            items = list()
            for cart in cart_objs:
                if not cart.is_ordered:
                    items.append(cart)
            total = sum([item.total for item in items])
            return render(request, 'cart.html', {'items': items, 'total': total, 'item_count': len(cart_items(request))})

        else:
            Cart.add_to_cart(book_id, request)

        books = Book.objects.all()
        item = Book.objects.filter(id=book_id)
        return render(request, 'item.html', {'books': books, 'item': item[0], 'act': 'go', 
                                                'page': 'books', 'item_count': len(cart_items(request))})

    else:
        messages.error(request, 'You need to log in first !!',
                       extra_tags='log')
        return render(request, 'login.html', {'page': 'login'})


def remove(request, item_id):
    item = Cart.objects.get(id=item_id)
    item.delete()
    return redirect('/cart/0')


def update(request):
    user = request.user
    items = Cart.objects.filter(customer=user, is_ordered=False)

    for item in items:
        item.quantity = int(request.GET['n'+str(item.id)])
        item.total = item.book.price * item.quantity
        item.save()

    total = sum([item.total for item in items])
    return render(request, 'cart.html', {'items': items, 'total': total, 'item_count': len(cart_items(request))})
