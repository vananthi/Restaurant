from django.urls import path
from . import views

urlpatterns = [
    path ('listCustomer', views.ListCustomer.as_view(), name='listCustomer'),
    path ('listOrder', views.ListOrder.as_view(), name='listOrder'),
    path ('listPayment', views.ListPayment.as_view(), name='listPayment'),
    path ('getCustomerDetails', views.GetCustomerDetails.as_view(), name='getCustomerDetails'),
    path ('getOrderDetails', views.GetOrderDetails.as_view(), name='getOrderDetails'),
    path ('getPaymentDetails', views.GetPaymentDetails.as_view(), name='getPaymentDetails'),
    path ('createCustomer', views.CreateCustomer.as_view(), name='createCustomer'),
    path ('createOrder', views.CreateOrder.as_view(), name='createOrder'),
    path ('createPayment', views.CreatePayment.as_view(), name='createPayment'),
    path ('updateCustomer', views.CreateCustomer.as_view(), name='updateCustomer'),
    path ('updateOrder', views.CreateOrder.as_view(), name='updateOrder'),
    path ('updatePayment', views.CreatePayment.as_view(), name='updatePayment'),
    path ('deleteCustomer', views.DeleteCustomer.as_view(), name='deleteCustomer'),
    path ('deleteOrder', views.DeleteOrder.as_view(), name='deleteOrder'),
    path ('deletePayment', views.DeletePayment.as_view(), name='deletePayment'),
    path ('get_instance_customer', views.ListCustomer.as_view(), name='get_instance_customer'),
    path ('get_instance_order', views.ListOrder.as_view(), name='get_instance_order'),
    path ('get_instance_payment', views.ListPayment.as_view(), name='get_instance_payment')
    


]

