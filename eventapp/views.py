from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def register(request):
    if request.method == 'POST':
        form = CustumUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustumUserCreationForm()
    return render(request, 'register.html', {'form': form })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request,'logout.html')

@login_required
def home_view(request):
    events = Event.objects.filter(is_active= True)
    return render(request, 'home.html', {'events': events})

 def create_event(request):
    if not request.user.is_organizer:
        
