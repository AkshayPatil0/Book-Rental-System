from django.contrib import admin
from .models import Book, Customer, Address

# Register your models here.
admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Address)
