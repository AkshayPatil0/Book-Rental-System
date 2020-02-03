from django.db import models
from main.models import Customer, Address

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, default=None, null=True)
    is_ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    total_cost = models.IntegerField(default=0)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, default=None, null=True)


class Rent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    is_received = models.BooleanField(default=False)
    received_date = models.DateField(null=True)
    return_requested = models.BooleanField(default=False)
    request_date = models.DateField(null=True)
    is_returned = models.BooleanField(default=False)
    return_date = models.DateField(null=True)
    cost = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
