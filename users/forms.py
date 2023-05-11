from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Valid email address, please', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ChallengeProgressForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['challenges', 'progress']
        labels = {'challenges': 'Challenges',
                  'progress': 'Progress',}



