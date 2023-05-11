from django import forms
from .models import BookRating, Genre

class BookRatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(str(i), i) for i in range(1, 6)])

    class Meta:
        model = BookRating
        fields = ['rating']



class GenreForm(forms.ModelForm):
    genre_name = forms.ModelChoiceField(queryset=Genre.objects.all())
    class Meta:
        model = Genre
        fields = ['genre_name']

