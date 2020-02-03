from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('place/<order_id>', views.place, name='place'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
