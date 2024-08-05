from django.contrib import admin
from .models import DoctorPrescription, DoctorProfile, UserProfile

# Register your models here.
admin.site.register(DoctorPrescription)
admin.site.register(DoctorProfile)
admin.site.register(UserProfile)

