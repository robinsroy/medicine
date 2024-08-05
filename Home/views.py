from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserAddForm, DocPriscriptionAddForm
from .decorators import admin_only
from .blockgenerator import Block
from datetime import datetime
from .models import Block_2,Block_1,Block_3,Block_4
from .models import Block_1, UserProfile, Prescription, DoctorProfile, DoctorPrescription
from manu.models import Medicine 



@admin_only
def Index(request):
    medicine = Medicine.objects.all()
    context = {
        "medicine":medicine
    }
    return render(request,"index.html",context)

def MakerIndex(request):
    return render(request,'manufacturer/makerindex.html')



def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or Password Incorrecr")
            return redirect('SignIn')
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            email = user.email 
            password = user.password
            username = user.username
            regdata = {"name":username,'email':email,"password":password}
            
            BlockChain = Block(1, datetime.now(), regdata,"0")
            
            block = Block_1.objects.create(BlockIndex = 1,BlockTimeStrap = datetime.now(),BlockLink = user,BlockData = regdata,previous_hash = "0",Blockhash = BlockChain.hash)
            block.save()
            
            messages.info(request,"User Created")
            return redirect('SignIn')
    return render(request,"register.html",{"form":form})

def SignOut(request):
    logout(request)
    return redirect('SignIn')

def ViewMed(request,pk):
    medi = Medicine.objects.get(id = pk)
    context = {
        "medi":medi
    }
    return render(request,'viewmedicine.html',context)

def ValidateMedicine(request,pk):
    medicine = Medicine.objects.get(id = pk)
    block4 = Block_4.objects.get(MedicineBlock = medicine)
    block3 = Block_3.objects.get(MedicineBlock = medicine)
    block2 = Block_2.objects.get(MedicineBlock = medicine)
    block1 = block2.BlockLink
    meddata = {"name":medicine.name,"manufacturer":medicine.manufacturer,"batch_number":medicine.batch_number,"expiry_date":medicine.expiry_date,"date_of_manufacture":medicine.date_of_manufacture,"owner":medicine.owner}
    BlockChanin2 = Block(3,medicine.timestamp,meddata,block2.Blockhash)
    
    blockdata = [block1,block2,block3]
    blockhashvalue = Block(4,"time",blockdata,block3.Blockhash)
    print(blockhashvalue)
    
    if BlockChanin2.hash == block3.Blockhash:
        if blockhashvalue.hash == block4.Blockhash:
            messages.success(request,"This Medicine is Valid")
            return redirect("ViewMed",pk=pk)            
        else:
            messages.info(request,"This Medicine is InValid")
            return redirect("ViewMed",pk=pk)
    else:
        messages.info(request,"This Medicine is InValid")
        return redirect("ViewMed",pk=pk)


@login_required(login_url="SignIn")
def Userprofile(request):
    try:
        user = UserProfile.objects.get(user = request.user)
    except:
        user = UserProfile.objects.create(user = request.user,house = "nil",city = "nil",district = "nil",state = "nil",phone = "nil")

    if request.method == "POST":
        user.phone = request.POST['phone']
        user.city = request.POST['city']
        user.house = request.POST['house']
        user.district = request.POST['district']
        user.state = request.POST['state']
        user.save()
        messages.info(request,"User Updated..")
        return redirect("Userprofile")

    context = {
        "user":user
    }

    return render(request, "useprofile.html",context)


def AllMedicines(request):

    medicine = Medicine.objects.all()

    context = {
        "medicine":medicine
    }
    return render(request,"allmedicines.html",context)

@login_required(login_url="SignIn")
def Search(request):
    if request.method == "POST":
        search = request.POST["search"]
        medicine = Medicine.objects.filter(name__contains = search)

        context = {
            "medicine":medicine
        }

        return render(request, "searchresults.html",context)

def UploadPrescription(request):
    import PyPDF2
    import re
    import string
    import pandas as pd

    if request.method == "POST":
        pres = request.FILES["pres"]
        data = Prescription.objects.create(user=request.user,pres = pres)
        data.save()


        prescription = data.pres.url
        prescription = prescription.replace(prescription[0],"",1)
        print(prescription)
        pdfFileObj = open(prescription,'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)

        num_pages = len(pdfReader.pages)

        count = 0
        text = ""

        while count < num_pages:
            pageObj = pdfReader.pages[count]
            count +=1
            text += pageObj.extract_text()

        text = text.lower()
        text = re.sub(r'\d+','',text)
        text = text.translate(str.maketrans('','',string.punctuation))

        print(text)

        medicine = Medicine.objects.filter(name__contains = str(text).strip())
        context = {
            "medicine":medicine
        }

        return render(request, "searchresults.html",context)

    return render(request,'uploadprescription.html')


# doctor Modeles
# 
# 
@login_required(login_url="SignIn")
def DoctorIndex(request):
    pres = DoctorPrescription.objects.filter(doctor__user = request.user)

    context = {
        "pres":pres
    }
    return render(request,"doctorindex.html",context) 

@login_required(login_url="SignIn")
def UpadtePrescription(request,pk):
    if request.method == "POST":
        prescription = request.POST["prescription"]
        pres = DoctorPrescription.objects.get(id = pk)
        pres.Prescription = prescription
        pres.save()
        messages.info(request,"Preciption added Upadted")
        return redirect("DoctorIndex")

def PatientReq(request):
    return render(request,"patientrequests.html")

@login_required(login_url="SignIn")
def ProfileDoctor(request):
    if request.method == "POST":
        name  = request.POST["name"]
        spec  = request.POST["spec"]

        profile = DoctorProfile.objects.create(user = request.user,name= name,Specilisation = spec)
        profile.save()
        messages.info(request,"Profile Upadted")
        return redirect("ProfileDoctor")

    try:
        profile = DoctorProfile.objects.get(user = request.user)
    except:
        profile = {"user":request.user,"name":"Please Update","Specilisation":"Please Upadte" }
    
    context = {
        "profile":profile
    }
    return render(request,"doctorprofile.html",context)

@login_required(login_url="SignIn")
def PrescriptionReq(request):
    form = DocPriscriptionAddForm()
    mypri = DoctorPrescription.objects.filter(patient = request.user)
    if request.method == "POST":
        form = DocPriscriptionAddForm(request.POST)
        if form.is_valid():
            prescr = form.save()
            prescr.patient = request.user 
            prescr.save()
            messages.info(request,"Prescription Requested")
            return redirect("PrescriptionReq")

    context = {
        "form":form,
        "mypri":mypri
    }
    return render(request,"prescriptionrequest.html",context)








