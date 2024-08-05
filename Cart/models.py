from django.db import models
from manu.models import Medicine
from django.contrib.auth.models import User

class CartItems(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()
    
class CheckoutItems(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)


class EmergencyCheckout(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)


    
    
