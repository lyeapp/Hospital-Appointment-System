from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),
    path('department/', views.department, name='department'),
    path('signup/', views.signup, name='signup'),  # Custom sign-up view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('booking/edit/<int:id>/', views.edit_booking, name='edit_booking'),
    path('booking/delete/<int:id>/', views.delete_booking, name='delete_booking'),
]