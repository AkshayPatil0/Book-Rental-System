from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('update', views.update, name='update'),
    path('<book_id>', views.cart, name='cart'),
    path('remove/<item_id>', views.remove, name='remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
