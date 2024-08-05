from django.db import models
from django.contrib.auth.models import User


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manufacturer = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    distributer_price = models.FloatField()
    MRP = models.IntegerField()
    date_of_manufacture = models.DateField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    # transaction_id = models.CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='medicine_image')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name + self.manufacturer)
    