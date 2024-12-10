from rest_framework import serializers # Importing serializers from Django REST Framework
from .models import *  # Importing all models from the current app
from django.contrib.auth.models import User

# Serializer to list customer details
class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer # Specifying the Customer model to be serialized
        fields = ['user','phone_number'] # Fields to include in the serialized data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')        

# Serializer to list order details, with customer and table details
class ListOrderSerializer(serializers.ModelSerializer):
    menu_items_detail=serializers.SerializerMethodField()
    customer_detail=serializers.SerializerMethodField() # Custom field to add customer details
    table_detail= serializers.SerializerMethodField()  # Custom field to add table details

    class Meta:
        model = Order # Specifying the Order model to be serialized
        fields = ['order_time','status','id','customer_detail','table_detail','menu_items_detail'] # Fields to includ
    
    def get_menu_items_detail(self,obj):
        
             menu_items = obj.menu_items.all()
             menu_items_data = []
             for items in menu_items:
                 menu_items_data.append({
                     'name': items.name,  # Adding the name of the menu item
                     'price': items.price,  # Adding the price of the menu item
            })
             return {
                 'menu_items': menu_items_data
        }
    
    def get_customer_detail(self,obj):
        
          return{
          'name':obj.customer.user.first_name,
          'phone_number':obj.customer.phone_number,
          'email':obj.customer.user.email
       }
       
    
    def get_table_detail(self,obj):
       
          return{
          'number':obj.table.number,
          'capacity':obj.table.capacity,
          'is_occupied':obj.table.is_occupied
       }
    
   
# Serializer to list payment details, with associated order details
class ListPaymentSerializer(serializers.ModelSerializer):
    order_detail=serializers.SerializerMethodField()

    
    class Meta:
        model = Payment # Specifying the Payment model to be serialized
        fields = ['id','amount','payment_method','payment_time','status','order_detail'] # Fields to include

    
    # Method to get order details related to the payment    
    
    def get_order_detail(self, obj):
        try:
        # Fetching all menu items related to the order (ManyToManyField)
          menu_items = obj.order.menu_items.all()
          menu_items_data = []

        # Iterating through each menu item to extract relevant details
          for item in menu_items:
            menu_items_data.append({
                'name': item.name,  # Adding the name of the menu item
                'price': item.price,  # Adding the price of the menu item
            })
        except:
        # In case of any exception, return None
          return None

    # Returning a dictionary with order details
        return {
           'table':obj.order.table_id,
           'number':obj.order.table.number,
           'customer':obj.order.customer_id,
           'name':obj.order.customer.user.first_name,
           'status': obj.order.status,  # Returning the order status
           'menu_items': menu_items_data  # Returning the list of menu items in the order
    }

      