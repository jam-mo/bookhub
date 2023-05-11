from django.db import models
from django.urls import reverse
from users.models import CustomUser #django marks as error, though apparently works
from datetime import date
from django.db.models import Q
import uuid
# Create your models here.

class Genre(models.Model):
    ''' model rperesents book genres'''
    genre_name = models.CharField(max_length=200)
    #define an absolute url for genres

    def __str__(self):

        return self.genre_name

    def get_absolute_url(self):
        return reverse('genre_detail', args=[self.genre_name])

class Book(models.Model):
    ''' model representing the books,'''
    #no need for id column as django will create a column automatically
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    ratings = models.DecimalField(max_digits=3, decimal_places=1)
    genre = models.ManyToManyField(Genre)
    publisher = models.CharField(max_length=200)
    ratings_count = models.IntegerField()
    book_copies = models.IntegerField()



    def __str__(self):
        """returns."""
        return self.title

    def get_absolute_url(self):
        """returns url to get record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):

        return ', '.join(genre.genre_name for genre in self.genre.all()[:3])

    def related_books(self):
        # get all books with the same genre(s) as this book, excluding this book
        related_by_genre = Book.objects.filter(genre__in=self.genre.all()).exclude(id=self.id)
        # get all books with similar titles, excluding this book
        related_by_title = Book.objects.filter(
            Q(title__icontains=self.title) | Q(title__icontains=self.title.split()[0]),
            ~Q(id=self.id)
        )
        # combine the two sets of related books and order by rating (descending)
        related_books = related_by_genre.union(related_by_title).order_by('-ratings')[:5]
        return related_books

    display_genre.short_description = 'Genre'


class BookRental(models.Model):
    ''' representing a copy of a book that can be taken out on loan'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    due_date = models.DateField(null=True, blank=True) # use instead of dateRented, dateReturned as waste of space
    # book status moves to here as more apr
    loanee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    book_status = (
        ('a', 'Available'),
        ('r', 'Reserved'),
        ('u', 'Unavailable'),
    )
    status = models.CharField(
        max_length=1,
        choices=book_status,
        blank=True,
        default='u',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_date']
    @property
    def is_due(self):
        ''' determines if the book is overdue'''
        return bool(self.due_date and date.today() > self.due_date)

    def __str__(self):

        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    ''' model representing author'''
    fullname = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """returns url."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return f'{self.fullname}'

class BookRating(models.Model):
    ''' model for book ratings,'''
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

