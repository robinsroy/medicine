from django.db import models
from django.contrib.auth.models import User
from manu.models import Medicine

# Create your models here.

class Block_1(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(User,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)
    
class Block_2(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_1,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    MedicineBlock = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    Blockhash = models.CharField(max_length=255)
 
class Block_3(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_2,on_delete=models.CASCADE)
    MedicineBlock = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)
    
class Block_4(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_3,on_delete=models.CASCADE)
    MedicineBlock = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pres = models.FileField(upload_to="prescription")

class DoctorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    Specilisation = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " " + self.Specilisation


class DoctorPrescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete = models.SET_NULL,null=True,blank=True)
    patient = models.ForeignKey(User, on_delete = models.CASCADE,null=True, blank=True)
    Disease = models.CharField(max_length=255)
    Prescription = models.CharField(max_length=1000,null= True, blank=True)
    date = models.DateField(auto_now_add=True)
    


    
