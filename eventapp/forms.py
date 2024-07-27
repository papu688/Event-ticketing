from django import forms
from .models import Event, Profile, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustumUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'is_organizer', 'is_attendee']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_organizer', 'is_attendee']
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'price', 'location', 'max_tickets']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']