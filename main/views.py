from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Book, Customer, Address, Payment
from cart.models import Cart
from checkout.models import Rent, Order
from datetime import datetime, date
from django.http import Http404
import re
# Create your views here.

def cart_items(request):
    user = request.user
    try:
        items = Cart.objects.filter(customer=user, is_ordered=False)
    except Exception:
        items = list()
    return items

def main(request):
    books = Book.objects.all()
    categories = list()
    authors = list()
    for book in books:
        categories.append(book.category)

    for book in books:
        if not book.category == 'autobiography':
            authors.append(book.author)

    categories = list(set(categories))
    authors = list(set(authors))
    return render(request, "index.html", {'books': books, 'categories': categories, 'authors': authors,
                                          'page': 'index', 'item_count': len(cart_items(request))})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'page': 'login'})

    else:

        email = request.POST.get('c_email')
        pas = request.POST.get('c_password')

        if not email:
            messages.error(request, "E-mail required!!", extra_tags='log')
            return redirect('/login')

        if not pas:
            messages.error(request, "Password required!!", extra_tags='log')
            return redirect('/login')

        user = auth.authenticate(username=email, password=pas)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.error(request, 'Invalid credentials !!', extra_tags='log')
            return redirect('/login')

    return redirect('/')


def register(request):

    fname = request.POST['c_fname']
    lname = request.POST['c_lname']
    email = request.POST['c_email']
    phone = request.POST['c_phone']
    pass1 = request.POST['c_password']
    pass2 = request.POST['c_password1']

    if not email:
        messages.error(request, "User must have an E-mail !!")
        return redirect('/login')

    if not phone:
        messages.error(request, "User must have a phone no !!")
        return redirect('/login')

    if not pass1:
        messages.error(request, "User must provide password !!")
        return redirect('/login')

    if not pass2:
        messages.error(request, "User must confirm password !!")
        return redirect('/login')

    if pass1 == pass2:
        if Customer.objects.filter(email=email):
            messages.error(request, "E-mail already exists !!")
            return redirect('/login')

        else:
            user = Customer.objects.create_user(
                username=email, password=pass1, email=email, first_name=fname, last_name=lname, phone=phone)
            user.save()
            messages.info(request, 'User created !!')
            return redirect('/login')

    else:
        messages.error(request, 'Password not matching')
        return redirect('/login')


def logout(request):
    auth.logout(request)
    return redirect("/")


def search(request):
    key = request.GET['search']
    user = request.user
    try:
        cart_items = Cart.objects.filter(customer=user)
    except Exception:
        cart_items = list()
    books = list(Book.objects.all())
    items = list()
    for book in books:
        if re.search(key.lower(), book.title.lower()):
            items.append(book)

    return render(request, 'search.html', {'books': items, 'page': 'books', 'item_count': len(cart_items)})


def contact(request):
    return render(request, 'contact.html', {'item_count': len(cart_items(request))})


def profile(request):
    addresses = Address.objects.filter(customer=request.user)
    order_objs = Order.objects.filter(customer=request.user, is_ordered=True)
    orders = dict()
    for order in order_objs:
        items = Cart.objects.filter(order=order, is_ordered=True)
        orders[order.id] = items
    return render(request, 'profile.html', {'addresses': addresses, 'orders': orders, 'item_count': len(cart_items(request))})


def deposite(request, amt):
    user = request.user
    user.deposite = user.deposite + int(amt)
    user.save()
    return redirect("/profile")


def pay(request, amt):
    return render(request, 'payment.html', {'amt': amt})


def staff(request):
    if request.method == 'GET':
        return render(request, 'staff_log.html')

    else:
        email = request.POST.get('c_email')
        pas = request.POST.get('c_password')

        if not email:
            messages.error(request, "E-mail required!!", extra_tags='log')
            return redirect('/staff_login')

        if not pas:
            messages.error(request, "Password required!!", extra_tags='log')
            return redirect('/staff_login')

        user = auth.authenticate(username=email, password=pas)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('/status')

            else:
                messages.error(
                    request, 'Not staff member !!', extra_tags='log')
                return redirect('/staff_login')

        else:
            messages.error(request, 'Invalid credentials !!', extra_tags='log')
            return redirect('/staff_login')


def status(request):
    rent_objs = Rent.objects.all()
    return render(request, 'status.html', {'rents': rent_objs})


def update_status(request, typ, rent_id):

    rent = Rent.objects.get(id=rent_id)

    if typ == 'del':
        rent.is_received = True
        rent.received_date = date.today()
        
    elif typ == 'ret':
        if rent.return_requested:
            rent.is_returned = True
            rent.return_date = date.today()
        else:
            messages.error(request, 'Return is not requested !!')
            return redirect("/status")

    else:
        rent.return_requested = True
        rent.request_date = date.today()
        days = (rent.request_date - rent.received_date).days+1
        rent.cost = days*(5*rent.order.total_cost/100)+50
        rent.save()
        return redirect('/profile')

    rent.save()
    return redirect("/status")

def search_order(request):
    order_id = None
    try:
        order_id = request.GET['order_id']
    except:
        messages.error(request, 'No record found !!')
        return render(request, 'status.html')
    
    rent_objs = Rent.objects.filter(order_id=order_id)

    if len(rent_objs) > 0:
        return render(request, 'status.html', {'rents': rent_objs})

    else:
        messages.error(request, 'No record found !!')
        return render(request, 'status.html')