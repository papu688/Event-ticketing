
from django.contrib import admin
from django.urls import path
from eventapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('buy_tickets/<int:event_id>/', views.buy_ticket,name='buy_tickets'),
    path('my_tickets/', views.my_tickets,name='my_tickets'),
    path('personal_page/', views.personal_page, name='personal_page'),

]

