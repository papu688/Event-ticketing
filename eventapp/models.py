from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=False)

    def clean(self):
        if self.is_organizer and self.is_attendee:
            raise ValidationError('A user cannot be both an organizer and an attendee.')

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    price = models.FloatField()
    max_tickets = models.PositiveIntegerField()
    tickets_sold = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def available_tickets(self):
        return self.max_tickets - self.tickets_sold
    
    def is_active_event(self):
        return self.date > timezone.now()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class  Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.event.title} by {self.attendee.username}'
    


