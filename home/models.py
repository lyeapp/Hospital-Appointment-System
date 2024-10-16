from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Departments model
class Departments(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()

    def __str__(self):
        return self.dep_name


# Doctors model
class Doctors(models.Model):
    doc_name = models.CharField(max_length=255)
    doc_spec = models.CharField(max_length=255)
    dep_name = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors')

    def __str__(self):
        return 'Dr ' + self.doc_name + ' - (' + self.doc_spec + ')'


# Booking model
class Booking(models.Model):
    p_name = models.ForeignKey('PatientProfile', on_delete=models.CASCADE)  # Use string reference
    p_phone = models.CharField(max_length=10)
    p_email = models.EmailField()
    doc_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)


# PatientProfile model
class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# Signal to create or save PatientProfile
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile only if the user is created
        PatientProfile.objects.get_or_create(user=instance)
    else:
        # Save the profile if it already exists when the user is updated
        instance.patientprofile.save()




