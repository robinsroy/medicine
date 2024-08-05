from django.urls import path  
from .import views 

urlpatterns = [
    path("DeliveryIndex",views.DeliveryIndex,name="DeliveryIndex"),
    path("DeliverBoyOrderView",views.DeliverBoyOrderView,name="DeliverBoyOrderView"),
    path("ChangeOrderStatus/<int:pk>/<str:str>",views.ChangeOrderStatus,name="ChangeOrderStatus"),
    path("ChangeOrderStatusEM/<int:pk>/<str:str>",views.ChangeOrderStatusEM,name="ChangeOrderStatusEM"),
    path("ViewCustomerAddress/<int:pk>",views.ViewCustomerAddress,name="ViewCustomerAddress"),
]
