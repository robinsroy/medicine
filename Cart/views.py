from django.shortcuts import render, redirect
from Home.blockgenerator import Block
from django.contrib import messages
from datetime import datetime
from Home.models import Block_2,Block_1,Block_3,Block_4
from Home.models import Block_1
from manu.models import Medicine
from django.contrib.auth.decorators import login_required
from .models import CartItems, CheckoutItems, EmergencyCheckout

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest




# Create your views here.
@login_required(login_url='SignIn')
def CartPage(request):
    cart = CartItems.objects.filter(user = request.user)
    total = 0
    for item in cart:
        total = total + item.price
    gst = total*18/100
    price = total - gst
    context = {
        "cart":cart,
        "total":total,
        "gst":gst,
        "price":price,
        'totalcart':len(cart)
    }
    return render(request,"cartpage.html",context)


@login_required(login_url='SignIn')
def AddToCart(request,pk):
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
            cart = CartItems.objects.create(medicine = medicine,user = request.user,stock = 1,price = medicine.MRP )
            cart.save()
            return redirect('CartPage')
        else:
            messages.info(request,"This Medicine is InValid You cannot buy This medicine")
            return redirect("ViewMed",pk=pk)
    else:
        messages.info(request,"This Medicine is InValid You cannot buy This medicine")
        return redirect("ViewMed",pk=pk)
    
    return render(request,"cartpage.html")
@login_required(login_url='SignIn')
def IncreaseQuantity(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.stock = cart.stock + 1
    cart.price = cart.price + cart.medicine.MRP
    cart.save()
    return redirect('CartPage')

@login_required(login_url='SignIn')
def DecreaseQuantity(request,pk):
    cart = CartItems.objects.get(id = pk)
    
    if cart.stock == 1:
        cart.delete()
    else:
        cart.stock = cart.stock - 1
        cart.price = cart.price - cart.medicine.MRP
        cart.save()
        
    return redirect('CartPage')

@login_required(login_url='SignIn')
def DeleteCartItem(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.delete()
    return redirect('CartPage')


razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url='SignIn')
def ProceedCheckout(request):
    cart = CartItems.objects.filter(user = request.user)
    for i in cart:
        Checkoutitems = CheckoutItems.objects.create(medicine = i.medicine,user=request.user,stock = i.stock,price = i.price,status = "item Ordered")
        Checkoutitems.save()
        dcart = CartItems.objects.get(id = i.id)
        dcart.delete()
    checkitems = CheckoutItems.objects.filter(user = request.user,payment_status = False)
    total = 0
    for item in checkitems:
        total = total + item.price
    currency = 'INR'
    amount = total * 100 # Rs. 200
    context = {}

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = "paymenthandler/"

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1",
    context['numitems'] = len(checkitems)
    context['total'] = total
    # context['amt'] = (product1.Product_price)*float(qty)
    
    return render(request,'checkoutpage.html',context)


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                checkitems = CheckoutItems.objects.filter(user = request.user,payment_status = False)
                total = 0
                for item in checkitems:
                    total = total + item.price
                    checkitems.payment_status = True
                    checkitems.save()
                amount = total * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')


@login_required(login_url='SignIn')
def MyOrderes(request):
    orderitems = CheckoutItems.objects.filter(user=request.user)
    Eitems = EmergencyCheckout.objects.filter(user = request.user)
    context = {
        "orderitems":orderitems,
        "Eitems":Eitems
    }
    return render(request,'myorders.html',context)



def deleteordermanu(request,pk):
    orderitems = CheckoutItems.objects.filter(id=pk).delete()
    return redirect("CustomerOrderes")
    
def deleteordercus(request,pk):
    orderitems = CheckoutItems.objects.get(id=pk).delete()
    return redirect("MyOrderes")

def deleteordercusEmry(request,pk):
    orderitems =  EmergencyCheckout.objects.get(id=pk).delete()
    return redirect("MyOrderes")


    
        
def EmergencyBuy(request,pk):
    medicine = Medicine.objects.get(id = pk)
    order = EmergencyCheckout.objects.create(medicine = medicine,user = request.user,stock = 1,price = medicine.MRP, status = "item Ordered" )
    order.save()
    return render(request,"confirmation.html")
    
