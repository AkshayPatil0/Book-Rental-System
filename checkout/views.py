from django.shortcuts import render, redirect
from main.models import Book, Customer, Address
from cart.models import Cart
from .models import Order, Rent
import datetime
from django.contrib import messages

# Create your views here.


def checkout(request):
    cart_objs = Cart.objects.filter(customer=request.user)
    items=[]
    for item in cart_objs:
        if not item.is_ordered:
            items.append(item)
    
    if len(items) == 0:
        return redirect('/cart/0')
    order = None
    for item in items:
        if item.order and not item.is_ordered:
            order = item.order
            break

    if order:
        pass
    else:
        order = Order.objects.create()

    for item in items:
        item.order = order
        item.save()

    order.customer = request.user
    order.total_cost = sum([item.total for item in items])
    order.save()
    addresses = Address.objects.filter(customer=request.user)
    items = Cart.objects.filter(customer=request.user, order=order)
    total = sum([item.total for item in items])

    return render(request, 'checkout.html', {'addresses': addresses, 'items': items, 'total': total, 'order_id': order.id})


def place(request, order_id):
    try:
        address_choice = request.GET['address']
        address_id = request.GET.get('c_address')
    except:
        messages.error(request, 'Select address to proceed !!',
                       extra_tags='address')
        return redirect('/checkout')

    if address_choice == '1':
        if address_id == None:
            messages.error(request, 'Select address to proceed !!',
                        extra_tags='address')
            return redirect('/checkout')

    fname = request.GET['c_fname']
    lname = request.GET['c_lname']
    add_ln1 = request.GET['c_add_ln1']
    add_ln2 = request.GET['c_add_ln2']
    pin = request.GET['c_pin']
    city = request.GET['c_city']
    phone = request.GET['c_phone']

    if fname==None or lname==None or add_ln1==None or pin==None or phone==None or city==None:
        messages.error(
            request, 'Must fill the required fields marked as *', extra_tags='field')
        return redirect('/checkout')

    order = Order.objects.get(id=order_id)
    
    if request.user.deposite < order.total_cost:
        messages.error(request, 'You should have deposited amount more than order amount in your account to place the order',
                        extra_tags='deposite')
        return redirect('/checkout')

    if address_choice == '1':
        address = Address.objects.get(id=address_id)

    else:
        address = Address.objects.create(first_name=fname, last_name=lname, add_ln1=add_ln1, add_ln2=add_ln2, city=city,
                                         pincode=pin, phone=phone, customer=request.user)

    order.address = address
    order.is_ordered = True
    order.date_ordered = datetime.datetime.now()
    order.save()
    items = Cart.objects.filter(customer=request.user)
    for item in items:
        item.is_ordered = True
        item.save()
    rent = Rent.objects.create(order=order)
    rent.save()
    return render(request, 'thankyou.html')
