from django.urls import path
from . import views
from django.views import generic


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('loan_book/<int:pk>', views.loan_book, name='loan_book'),
    path('book/<uuid:pk>/return', views.return_book, name='return_book'),
    path('book/<int:pk>/rate/', views.book_rate, name='book_rate'),
    path('recommendation/', views.recommend_books, name='recommend'),

]
