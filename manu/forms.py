from django.forms import ModelForm,TextInput
from .models import Medicine

class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ["name","description","manufacturer","batch_number","expiry_date","date_of_manufacture","image","distributer_price","MRP","image"]
        
        widgets = {
            "expiry_date":TextInput(attrs={"type":'date'}),
            "date_of_manufacture":TextInput(attrs={"type":"date"}),
            
        }
