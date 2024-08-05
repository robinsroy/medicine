from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DoctorPrescription
from django.forms import ModelForm, Select, Textarea, TextInput

class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1","password2"]

class DocPriscriptionAddForm(ModelForm):
    class Meta:
        model  = DoctorPrescription
        fields = ["doctor","Disease"]

        widgets = {
            "doctor":Select(attrs={"class":"form-control"}),
            "Disease":TextInput(attrs={"class":"form-control"})
        }
