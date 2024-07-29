from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .decorators import instructor_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
 
from django.db.models import Q


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
    is_organizer = request.user.is_organizer
    return render(request, 'home.html', {'events': events, 'is_organizer': is_organizer})

@login_required
@instructor_required
def create_event(request):
    
    
    if request.method == 'POST':
        
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
        
@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_tickets() <= 0:
        return HttpResponse('No Tickets available!')
    
    if request.method == 'POST':
        if event.available_tickets() > 0:
            Ticket.objects.create(event=event, attendee=request.user)
            event.tickets_sold += 1
            event.save()
            return redirect('home')
        
    return render(request, 'buy_tickets.html', {'event': event})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(attendee=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})


@login_required
def personal_page(request):
    tickets = Ticket.objects.filter(attendee=request.user)
    
    if request.method == 'POST':
        if 'change_username' in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                return redirect('personal_page')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) #um sicherzustellen, dass der Benutzer nach der Passwortänderung angemeldet bleibt
                return redirect('personal_page')
    else:
        username_form = UsernameChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'personal_page.html', {
        'tickets': tickets,
        'username_form': username_form,
        'password_form': password_form,
    })



