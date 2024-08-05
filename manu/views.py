from django.shortcuts import render,redirect,HttpResponse
from .forms import MedicineForm
from django.contrib import messages
from Home.blockgenerator import Block
from datetime import datetime
from Home.models import Block_2,Block_1,Block_3,Block_4
from .models import Medicine
from Cart.models import CheckoutItems


def Medicine_Func(request):
    form = MedicineForm()
    medi = Medicine.objects.filter(owner = request.user)
    
    if request.method == "POST":
        form = MedicineForm(request.POST,request.FILES)
        if form.is_valid():
            med  = form.save()
            med.owner = request.user
            med.save()
            medicine = Medicine.objects.get(id = med.id)
            
            # Block Number 2 Creation----------------------------------------------
            
            user = request.user 
            logdata = {"name":user.first_name,"username":user.username,"password":user.password,"medicine":medicine}
            regblock = Block_1.objects.get(BlockLink = request.user)
            
            BlockChain = Block(2, datetime.now(), logdata,regblock.Blockhash)
            
            block2 = Block_2.objects.create(BlockIndex = 2,BlockTimeStrap = datetime.now(),BlockData=logdata,BlockLink = regblock,previous_hash = regblock.Blockhash,Blockhash = BlockChain.hash,MedicineBlock = medicine)
            block2.save()
            
            # Block Number 3 Creation----------------------------------------------
            
            meddata = {"name":medicine.name,"manufacturer":medicine.manufacturer,"batch_number":medicine.batch_number,"expiry_date":medicine.expiry_date,"date_of_manufacture":medicine.date_of_manufacture,"owner":medicine.owner}
            
            BlockChanin2 = Block(3,medicine.timestamp,meddata,block2.Blockhash)
            
            block3 = Block_3.objects.create(BlockIndex = 3, BlockTimeStrap = datetime.now(),BlockData = meddata,BlockLink = block2,MedicineBlock = medicine,previous_hash = block2.Blockhash,Blockhash = BlockChanin2.hash )
            block3.save()
            
            # Block Number 4 Creation----------------------------------------------
            
            blockdata = [regblock,block2,block3]
            
            BlockChanin3 = Block(4,"time",blockdata,block3.Blockhash)
            block4 = Block_4.objects.create(BlockIndex = 4,BlockTimeStrap = datetime.now(),BlockData = blockdata,BlockLink = block3,MedicineBlock = medicine,previous_hash = block3.Blockhash,Blockhash = BlockChanin3.hash)
            block4.save()
             
            messages.info(request,"New Medicine Added To secured Medicine List")
            return redirect("Medicine_Func")
        
    context = {
        "form":form,
        "medi":medi,
    }
    return render(request,"manufacturer/medicine.html",context)

def MedicineValidate(request,pk):
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
            messages.info(request,"Medicine is Valid")
            return redirect("Medicine_Func")
        else:
            messages.info(request,"Medicine is not valid")
            return redirect("Medicine_Func")
            
    else:
        messages.info(request,"Medicine is not valid")
        return redirect("Medicine_Func")
        
        
        
def CustomerOrderes(request):
    items = CheckoutItems.objects.all()
    context = {
        "items":items
    }
    return render(request,"manufacturer/orders.html",context)

def Deletemed(request,pk):
    Medicine.objects.get(id = pk).delete()
    messages.info(request,"Medicine deleted")
    return redirect("Medicine_Func")
    
