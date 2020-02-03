from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('search_order', views.search_order, name='search_order'),
    path('status', views.status, name='status'),
    path('staff_login', views.staff, name='staff'),
    path('update_status/<typ>/<rent_id>', views.update_status, name='update_status'),
    path('payment/<amt>', views.pay, name='pay'),
    path('update_deposite/<amt>', views.deposite, name='deposite'),
    path('books/', include('show_books.urls'), name='books'),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
