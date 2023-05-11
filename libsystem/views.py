from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookRental, Author, Genre, BookRating
from django.views import generic
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, Http404
from .forms import BookRatingForm, GenreForm
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from django.urls import reverse


# Create your views here.
def index(request):
    ''' view function for home page of site.'''
    # counts books and rental status of books
    books_count = Book.objects.all().count()
    #rental_count = BookRental.objects.all().count()

    books_availability = BookRental.objects.filter(status__exact='a').count()

    authors_count = Author.objects.count()
    popular_books = Book.objects.order_by('-ratings_count', '-ratings')[:3]

    genres_count = Genre.objects.all().count()
    context = {
        'books_count': books_count,
        'authors_count': authors_count,
        'genres_count': genres_count,
        'popular_books': popular_books
    }

    return render(request, 'index.html', context=context)



class BookListView(generic.ListView):

    model = Book
    paginate_by = 8

class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = BookRatingForm()
        context['related_books'] = self.object.related_books()
        return context

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 8
class AuthorDetailView(generic.DetailView):
    model = Author

class GenreListView(generic.ListView):
    model = Genre


@login_required
@require_POST # user must be logged in, method must be post
def loan_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copy = book.bookrental_set.filter(status='a').first()

    if available_copy:
        available_copy.loanee = request.user
        available_copy.status = 'u'
        #set due date for 2 weeks after todays date
        available_copy.save()


    return redirect('book-detail', pk=book.pk)




@login_required
def return_book(request, pk):
    rental = get_object_or_404(BookRental, id=pk)
    if rental.loanee != request.user:
        messages.error(request, 'You are not the current loanee of this book.')
    else:
        rental.status = 'a'  # set book status as available
        rental.save()
        messages.success(request, f'Thank you for returning {rental.book.title}.')

    return redirect('book-detail', pk=rental.book.id)

@login_required # user must be logged in, method must be post
@require_POST
def book_rate(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookRatingForm(request.POST)
    if form.is_valid():
        rating = int(form.cleaned_data['rating'])
        BookRating.objects.create(book=book, user=request.user, rating=rating)
        book.ratings_count += 1
        book.ratings = (book.ratings * (book.ratings_count - 1) + rating) / book.ratings_count
        book.save()
        messages.success(request, 'Book rated successfully!')
    else:
        messages.error(request, 'Invalid rating')
    return redirect('book-detail', pk=book.pk)



def recommend_books(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            selected_genre = form.cleaned_data['genre_name'].genre_name # cleans data
            genre_books = Book.objects.filter(genre__genre_name=selected_genre) # filters book by genre
            if len(genre_books) == 0:
                context = {'message': f"No books found for the genre {selected_genre}."}
            else:
                book_titles = [book.title for book in genre_books]
                count_vectorizer = CountVectorizer()
                count_matrix = count_vectorizer.fit_transform(book_titles) # transfrom titles into matrix
                cosine_sim = cosine_similarity(count_matrix, count_matrix) # calculates cosine between each pairs of books
                sim_scores = list(enumerate(cosine_sim[-1]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #sorts sim scores in desc order
                book_indices = [i[0] for i in sim_scores[1:6]] #selects top 5 similar books
                recommended_books = Book.objects.filter(title__in=[book_titles[i] for i in book_indices])
                context = {'recommended_books': recommended_books, 'form': GenreForm()}
    else:
        form = GenreForm()
        context = {'form': form}
    return render(request, 'libsystem/recommend.html', context=context)