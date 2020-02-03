from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('filter/<typ>/<key>/<page_no>', views.filt, name='filt'),
    path('sort/<key>/<order>/<page_no>', views.sort, name='sort'),
    path('book_info/<book_id>/', views.book_info, name='book_info'),
    path('<page_no>', views.books, name='books'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
