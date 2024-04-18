from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('generate_timetable', views.generate_timetable, name='generate_timetable'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('login_page', views.login_page, name='login_page'),
    path('SignOut', views.SignOut, name='SignOut'),
    path('edit_timetable/<int:pk>/', views.edit_timetable, name='edit_timetable'),
    path('delete_tt/<int:pk>/', views.delete_tt, name='delete_tt'),



]