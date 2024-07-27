
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

]
