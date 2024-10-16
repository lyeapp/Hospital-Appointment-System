from django import forms
from django.contrib.auth.models import User
from .models import PatientProfile, Booking
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'booking_date': DateInput(),
        }
        labels = {
            'p_name': "Patient Name: ",
            'p_phone': "Phone Number: ",
            'p_email': "Email: ",
            'doc_name': "Consulting Doctor: ",
            'booking_date': "Booking Date: ",
        }

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['phone_number', 'address']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    tc = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'TC Number', 'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'tc', 'phone_number', 'address']
