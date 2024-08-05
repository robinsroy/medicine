from django.urls import path

from .import views 

urlpatterns = [
    path("Medicine_Func",views.Medicine_Func,name="Medicine_Func"),
    path("MedicineValidate/<int:pk>",views.MedicineValidate,name="MedicineValidate"),
    path("CustomerOrderes",views.CustomerOrderes,name="CustomerOrderes"),
    path("Deletemed/<int:pk>",views.Deletemed,name="Deletemed"),
    
]
