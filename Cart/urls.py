from django.urls import path  
from .import views 

urlpatterns = [

    
    path("AddToCart/<int:pk>",views.AddToCart,name="AddToCart"),
    path("CartPage",views.CartPage,name="CartPage"),
    path("IncreaseQuantity/<int:pk>",views.IncreaseQuantity,name="IncreaseQuantity"),
    path("DecreaseQuantity/<int:pk>",views.DecreaseQuantity,name="DecreaseQuantity"),
    path("DeleteCartItem/<int:pk>",views.DeleteCartItem,name="DeleteCartItem"),
    path("ProceedCheckout",views.ProceedCheckout,name="ProceedCheckout"),
    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("Success1",views.Success1,name="Success1"),
    path("MyOrderes",views.MyOrderes,name="MyOrderes"),
    path("deleteordermanu/<int:pk>",views.deleteordermanu,name="deleteordermanu"),
    path("deleteordercus/<int:pk>",views.deleteordercus,name="deleteordercus"),
    path("EmergencyBuy/<int:pk>",views.EmergencyBuy,name="EmergencyBuy"),
    path("deleteordercusEmry/<int:pk>",views.deleteordercusEmry,name="deleteordercusEmry"),
    
    
]
