from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from main.models import Book, Customer
from cart.models import Cart
from django.http import Http404
import re
from main.views import cart_items

# Create your views here.


def books(request, page_no):
    books = list(Book.objects.all())
    categories = list()
    authors = list()

    for book in books:
        categories.append(book.category)

    for book in books:
        if not book.category == 'autobiography':
            authors.append(book.author)

    categories = list(set(categories))
    authors = list(set(authors))

    items = dict()
    page_count = int(len(books)/6 + 2)
    pages = [i for i in range(1, page_count)]
    for i in pages:
        l = []
        for j in range(6):
            try:
                book = books.pop(0)
            except Exception:
                break
            l.append(book)
        items[i] = l
    p = int(page_no)
    if p >= page_count:
        raise Http404
    if p <= 0:
        raise Http404
    return render(request, 'books.html', {'books': items, 'categories': categories, 'authors': authors,
                                          'page': 'books', 'pages': pages, 'page_no': p, 'page_count': page_count,
                                          'item_count': len(cart_items(request))})


def filt(request, typ, key, page_no):
    books = list(Book.objects.all())
    categories = list()
    authors = list()

    for book in books:
        categories.append(book.category)

    for book in books:
        if not book.category == 'autobiography':
            authors.append(book.author)

    categories = list(set(categories))
    authors = list(set(authors))

    if typ == 'category':
        books = list(Book.objects.filter(category=key))

    if typ == 'author':
        books = list(Book.objects.filter(author=key))

    items = dict()
    page_count = int(len(books)/6 + 2)
    pages = [i for i in range(1, page_count)]
    for i in pages:
        l = []
        for j in range(6):
            try:
                book = books.pop(0)
            except Exception:
                break
            l.append(book)
        items[i] = l
    p = int(page_no)
    if p >= page_count:
        raise Http404
    if p <= 0:
        raise Http404

    return render(request, 'books.html', {'books': items, 'categories': categories, 'authors': authors,
                                          'page': 'books', 'pages': pages, 'page_no': p, 'page_count': page_count,
                                          'item_count': len(cart_items(request)), 'type': typ, 'key': key})


def sort(request, key, order, page_no):
    books = list(Book.objects.all())
    categories = list()
    authors = list()

    for book in books:
        categories.append(book.category)

    for book in books:
        if not book.category == 'autobiography':
            authors.append(book.author)

    categories = list(set(categories))
    authors = list(set(authors))

    if key == 'name':
        if order == 'asc':
            books.sort(key=lambda x: x.title)
        else:
            books.sort(key=lambda x: x.title, reverse=True)
    elif key == 'price':
        if order == 'asc':
            books.sort(key=lambda x: x.price)
        else:
            books.sort(key=lambda x: x.price, reverse=True)

    items = dict()
    page_count = int(len(books)/6 + 2)
    pages = [i for i in range(1, page_count)]
    for i in pages:
        l = []
        for j in range(6):
            try:
                book = books.pop(0)
            except Exception:
                break
            l.append(book)
        items[i] = l
    p = int(page_no)
    if p >= page_count:
        raise Http404
    if p <= 0:
        raise Http404
    return render(request, 'books.html', {'books': items, 'categories': categories, 'authors': authors,
                                          'page': 'books', 'pages': pages, 'page_no': p, 'page_count': page_count,
                                          'item_count': len(cart_items(request))})


def book_info(request, book_id):
    books = Book.objects.all()
    item = Book.objects.filter(id=book_id)
    return render(request, 'item.html', {'books': books, 'item': item[0], 'act': 'add', 
                                            'page': 'books', 'item_count': len(cart_items(request))})
