from django.contrib import admin
from .models import Author, Book, BookRental, Genre, BookRating
from django.contrib.auth.admin import UserAdmin

class BooksInline(admin.TabularInline):
    """ enables to add books when creating author model"""
    model = Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ''' displays fields in admin site and registers model'''
    list_display = ('title','author', 'display_genre', 'publisher')
class AuthorAdmin(admin.ModelAdmin):
    ''' registers the author model on admin site'''
    list_display = ('fullname','last_name', 'first_name')
    fields = ['fullname','first_name', 'last_name']
    inlines = [BooksInline]
admin.site.register(Author, AuthorAdmin)

@admin.register(BookRental)
class BookRentalAdmin(admin.ModelAdmin):
    list_display = ('book','status', 'due_date','loanee','id')
    list_filter = ('status', 'due_date')
    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_date', 'loanee')
        }),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)
    ordering = ('genre_name',)
    search_fields = ('genre_name',)

    fieldsets = (
        (None, {
            'fields': ('genre_name',)
        }),
    )

    readonly_fields = ('get_absolute_url',)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    get_absolute_url.short_description = 'Genre URL'
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'timestamp')
    list_filter = ('book', 'user', 'rating', 'timestamp')
    search_fields = ('book__title', 'user__email')
    ordering = ('-timestamp',)

admin.site.register(BookRating, BookRatingAdmin)