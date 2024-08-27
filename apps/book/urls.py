from django.urls import path
from . import views

app_name = 'book-urls'
urlpatterns = [
    path('author/', views.list_authors, name='list-author'),
    path('tag/', views.list_tags, name='list-tag'),
    path('list/', views.list_books, name='list-book'),
    path('create/', views.create_book, name='create-book'),
]