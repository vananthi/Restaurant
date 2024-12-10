
from django.db import models  # Importing the models module from Django
from Menu.models import Table # Importing the Table model from Menu app
from Menu.models import MenuItem # Importing the MenuItem model from Menu app
import uuid  # For generating unique identifiers (UUID)
from django.contrib.auth.models import User

# Customer model to store customer information
class Customer(models.Model):
    # UUID field to serve as the primary key (unique identifier)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    phone_number=models.CharField(max_length=100,null=True,blank=True)
    
    # String representation of the Customer model to display meaningful info
    def __str__(self):
        return f'{self.user}===={self.phone_number}=====id:{self.id}'

# Order model to store order information
class Order(models.Model):
    # UUID field to serve as the primary key (unique identifier)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False)

    # Foreign key relation to Table, on delete set to null, can be blank
    table=models.ForeignKey(Table,on_delete=models.SET_NULL,null=True,blank=True) 

     # Foreign key relation to Customer, on delete set to null, can be blank
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)


    # Automatically set the order time when the order is created
    order_time=models.DateTimeField(auto_now_add=True)

     # Status field to store the current status of the order, can be null or blank
    status=models.CharField(max_length=100,null=True,blank=True)

    # Many-to-Many relationship with MenuItem model, allowing multiple items in an order
    menu_items = models.ManyToManyField(MenuItem)

     # String representation of the Order model to display meaningful info
    def __str__(self):
        if self.table:  # Checking if a table is associated with the order
            table_info = self.table
        else:
            table_info = 'No Table'
        if self.customer:  # Checking if a customer is associated with the order
            customer_info=self.customer
        else:
            customer_info='No Customer'
     # Returning a string with table and customer info
        return f"Order at {table_info}====={customer_info}===order_id:{self.id}"


# Payment model to store payment information
class Payment(models.Model):
    # UUID field to serve as the primary key (unique identifier)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False)

    # Foreign key relation to Order, on delete set to null, can be blank
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    # Decimal field to store the payment amount, max 10 digits, 2 decimal places, default value of 1
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=1)
    payment_method=models.CharField(max_length=100,null=True,blank=True)    # Field to store the payment method, can be null or blank
    payment_time=models.DateTimeField(auto_now_add=True)  # Automatically set the payment time when the payment is created
    status=models.CharField(max_length=100,null=True,blank=True) # Field to store the payment status, can be null or blank

    # String representation of the Payment model to display meaningful info
    def __str__(self):
        if self.order: # Checking if an order is associated with the payment
            order_info = f"Order ID: {self.order.id}"
        else:
            order_info = 'No Order'

        if self.payment_method: # Checking if a payment method is specified
            payment_method_info = self.payment_method
        else:
            payment_method_info = 'No Payment Method'
        
         # Returning a string with order ID, amount, and payment method info
        return f" {order_info}=====${self.amount}==={payment_method_info}==={self.payment_time}==={self.status}==={self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}"