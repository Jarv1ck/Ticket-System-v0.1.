from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Your First Name')
    last_name = forms.CharField(max_length=30, help_text='Your Last Name')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email',
                  'password1', 'password2', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('job', 'company', )