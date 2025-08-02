from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Use custom view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_password, name='add_password'),
    path('edit/<int:pk>/', views.edit_password, name='edit_password'),
    path('delete/<int:pk>/', views.delete_password, name='delete_password'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('get-password/<int:pk>/', views.get_password, name='get_password'),
]
