from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import BookingForm, SignUpForm
from .models import Departments, Doctors, PatientProfile, Booking
from django.contrib.auth import login
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Create a PatientProfile for the new user with phone number and address
            PatientProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            
            # Automatically log the user in after signup
            login(request, user)
            return redirect('profile')  # Redirect to the profile page after signup
            
        else:
            print(form.errors)  # Print any form validation errors for debugging
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # Associate the booking with the patient's profile
            booking.p_name = PatientProfile.objects.get(user=request.user)  # Ensure the booking is associated with the logged-in user
            booking.save()
            return render(request, 'confirmation.html')
    else:
        form = BookingForm()
    
    dict_form = {
        'form': form
    }
    return render(request, 'booking.html', dict_form)

def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, 'doctors.html', dict_docs)

def contact(request):
    return render(request, 'contact.html')

def department(request):
    dict_dept = {
        'dept': Departments.objects.all()
    }
    return render(request, 'department.html', dict_dept)

@login_required
def profile(request):
    try:
        # Get the PatientProfile for the logged-in user
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        # If no profile exists, redirect to a page where the user can create one or show an error
        return render(request, 'profile.html', {'error': 'Profile does not exist. Please contact support.'})

    # Check if phone_number and address are populated, handle if not
    if not patient_profile.phone_number or not patient_profile.address:
        error_message = "Your profile is missing some information. Please update your phone number and address."
    else:
        error_message = None

    # Retrieve the bookings for this patient profile
    bookings = Booking.objects.filter(p_name=patient_profile)
    
    context = {
        'profile': patient_profile,  # Pass the patient profile to the context
        'bookings': bookings,
        'error_message': error_message  # Pass the error message if profile is incomplete
    }

    return render(request, 'profile.html', context)

def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to profile or booking list page
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    
    if request.method == 'POST':
        booking.delete()
        return redirect('profile')  # Redirect back to profile or booking list page
    
    return render(request, 'confirm_delete.html', {'booking': booking})