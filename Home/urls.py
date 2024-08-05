from django.urls import path 
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.Index,name="Index"),
    path('SignIn',views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("MakerIndex",views.MakerIndex,name="MakerIndex"),
    path("ViewMed/<int:pk>",views.ViewMed,name="ViewMed"),
    path("ValidateMedicine/<int:pk>",views.ValidateMedicine,name="ValidateMedicine"),
    path("Userprofile",views.Userprofile,name="Userprofile"),
    path("AllMedicines",views.AllMedicines,name="AllMedicines"),
    path("Search",views.Search,name="Search"),
    path("UploadPrescription",views.UploadPrescription,name="UploadPrescription"),
    path("DoctorIndex",views.DoctorIndex,name="DoctorIndex"),
    path("PatientReq",views.PatientReq,name="PatientReq"),
    path("ProfileDoctor",views.ProfileDoctor,name="ProfileDoctor"),
    path("PrescriptionReq",views.PrescriptionReq,name="PrescriptionReq"),
    path("UpadtePrescription/<int:pk>",views.UpadtePrescription,name="UpadtePrescription"),

    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)