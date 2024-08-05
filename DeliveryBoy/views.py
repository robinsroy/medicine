from django.shortcuts import render, redirect 
from Cart.models import CartItems, EmergencyCheckout, CheckoutItems
from django.contrib.auth.models import User
from Home.models import UserProfile

def DeliveryIndex(request):
    emc = EmergencyCheckout.objects.all()
    ck = CheckoutItems.objects.all()

    context = {
        "emc":emc,
        "ck":ck,
        "lenemc":len(emc),
        "lemck":len(ck)
    }
    return render(request,"delivery/index.html",context)

def DeliverBoyOrderView(request):
    Eitems = EmergencyCheckout.objects.all()
    orderitems = CheckoutItems.objects.all()
    context = {
        "Eitems":Eitems,
        "orderitems":orderitems
    }
    return render(request, "delivery/orders.html",context)

def ChangeOrderStatus(request,pk,str):
    items = CheckoutItems.objects.get(id = pk)
    items.status = str
    items.save()
    return redirect("DeliverBoyOrderView")

def ChangeOrderStatusEM(request,pk,str):
    items = EmergencyCheckout.objects.get(id = pk)
    items.status = str
    items.save()
    return redirect("DeliverBoyOrderView")

def ViewCustomerAddress(request,pk):
    loguser = User.objects.get(id = pk)
    user = UserProfile.objects.get(user = loguser)

    context = {
        "user":user
    }
    return render(request, "delivery/customer.html",context)