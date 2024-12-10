# from tokenize import _Position
from django.http import HttpResponse
from rest_framework.response import Response # Used to send HTTP responses
from rest_framework.views import APIView # Base class for creating API views
from .models import * # Importing all models from the current directory's models.py
from .serializers import * # Importing all serializers from the current directory's serializers.py
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 




# ListCustomer API class to handle GET and POST requests for listing customers
class ListCustomer(APIView):
   authentication_classes = [authentication.TokenAuthentication]
   permission_classes = [permissions.IsAuthenticated]
   def get(self, request):
        data = request.query_params # Extracting query parameters (name, phone number, email)

         # Excluding a customer based on the provided name, phone number, and email, then ordering by name
        customer= Customer.objects.exclude(name=data['name'],phone_number=data['phone_number'],email=data['email']).order_by('name')

        serializer = ListCustomerSerializer(customer,many=True).data  # Serializing the resulting customer queryset
        return Response ({"Customer_name":serializer})   # Returning the serialized data in a Response
   
   def post(self, request):
        data = request.data  # Extracting data from the request body

        # Same logic as the GET method
        customer= Customer.objects.all()

        #if 'name' in data:
            #customer=customer.filter(name__icontains=data['name'])
        if 'phone_number' in data:
            customer=customer.filter (phone_number=data['phone_number'])
        #if 'email' in data:
            #customer=customer.filter(email=data['email'])                             
                                     
        serializer = ListCustomerSerializer(customer,many=True).data # Serializing the customer queryset
  
        return Response({"Customer_name":serializer})   # Returning the serialized data
   

   authentication_classes = []
   permission_classes = []
   def get_instance_customer(self,Customer,id):
       instance=object(Customer,id)
       return ({instance})
   
   

class GetCustomerDetails(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data
        customer=Customer.objects.get(id=data['id'])
        serializer=ListCustomerSerializer(customer).data
        return Response({"get customer details":serializer})   
     
    
    
# CreateCustomer API class to handle customer creation and updates
class CreateCustomer(APIView):
    authentication_classes = []
    permission_classes = []    
    def post(self, request):
        data=request.data  # Extracting data from the request body

        if 'id' in data:   # If an 'id' is provided, update the customer details
            customer=Customer.objects.get(id=data['id']) #Get customer by id
            #customer.name=data['name'] # update name
            customer.phone_number=data['phone_number'] # update phone number
            #customer.email=data['email'] # update email
            customer.save() # save customer changes
            return Response("Customer information updated successful")
        else:
            customer={} # create a new customer details
            #customer['name']=data['name'] # Assign customer name
            print(data,"-----------------------------------------")
            user={}
            user['username']=data['email']
            user['email']=data['email']
            user['first_name']=data['first_name']
            user=User.objects. create(**user)

            token = Token.objects.create(user=user)
            print(token.key)

            customer['phone_number']=data['phone_number'] #Assign phone number
            #customer['email']=data['email'] #Assign email
            customer['user']=user
            customer= Customer.objects.create(**customer) #create  new customer 
            customer.save()
            return Response({"Customer_name":"Customer information creation successful"})


# DeleteCustomer API class to handle customer deletion        
class DeleteCustomer(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data # Extracting data from the request body

        if "id" in data: # If 'id' is provided, delete the customer
            customer=Customer.objects.get(id=data['id']) # Get customer by id
            customer.delete() # Deleting the customer
            return Response("Customer detail delete successful")
        else:
            return Response("Customer detail not deleted")
    
# ListOrder API class to handle listing an order based on table number       
class ListOrder(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        data=request.query_params   # Extracting query parameters (table number)
        order = Order.objects.get(table=data['table'],customer=data['customer'])  #Fetching the order based on table
        serializer = ListOrderSerializer(order).data  # Serializing the order
        return Response({"Orders":serializer})  # Returning the serialized order data
    
    authentication_classes = []
    permission_classes = []
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    def get_instance_order(self,Order,id):
        instance=object(Order,id)
        return ({instance})
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data   # Similar logic to GET but using request data
        order = Order.objects.all()

        print(order,"132333333333333333333333333")

        if 'table' in data:
            order=order.filter(table=data['table'])
            print(order,"5555555555555555555555555555555555555555555555")
        
        if 'customer' in data:
            order=order.filter(customer=data['customer'])
        if 'menu_items' in data:
            order=order.filter(menu_items=data['menu_items'])
        print(order,"----------------=======================================")
        
        serializer = ListOrderSerializer(order,many=True).data
        return Response({"Orders":serializer})
    
class GetOrderDetails(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data
        order=Order.objects.get(id=data['id'])
        serializers=ListOrderSerializer(order).data
        return Response({'get order detail':serializers})    

# CreateOrder API class to handle order creation and updates
class CreateOrder(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data  # Extracting data from the request body

        if "id" in data:   # If 'id' is provided, update the order
            order=Order.objects.get(id=data['id']) #Get order by id
            order.table.number=data['table']['number'] #update table number
            order.table.capacity=data['table']['capacity'] #update table capacity
            order.table.is_occupied=data['table']['is_occupied'] #update table occupied detail
            order.table.save() # save table changes

            order.customer.name=data['customer']['name'] #update customer name
            order.customer.phone_number=data['customer']['phone_number'] #update customer phone number
            order.customer.email=data['customer']['email'] # update customer email
            order.customer.save() # save customer changes
            
            order.save() # save order changes
            return Response("Order updation successful")
        else:
             order_detail={} #create a new order 
             
             table={} # Create a new table and assign it to the order
             table['number']=data['table']['number'] #Assign table number
             table['capacity']=data['table']['capacity'] #Assign table capacity
             table['is_occupied']=data['table']['is_occupied'] #Assign table occupied detail
             table=Table.objects.create(**table)  #cfeate table objects
             
              # Create and save a new user and customer
             customer={} # create a new customer details
            #customer['name']=data['name'] # Assign customer name
             print(data,"-----------------------------------------")
             user_details={}
             user_details['username']=data['customer']['username']
             user_details['email']=data ['customer']['email']
             user_details['first_name']=data ['customer']['first_name']
             user=User.objects. create(**user_details)

             token = Token.objects.create(user=user)
             print(token.key)

             customer['phone_number']=data['customer']['phone_number'] #Assign phone number
            #customer['email']=data['email'] #Assign email
             customer['user']=user
             customer= Customer.objects.create(**customer) 

                # Create and save a new order
             order_detail['table']=table
             order_detail['customer']=customer
             order = Order.objects.create(**order_detail) #create order objects
             order.menu_items.set(data['menu_items']) # Assigning menu items to the order
             order.status=data['status']
             order.save() # saving the order
             return Response({"Orders":"Order create successful"})

# DeleteOrder API class to handle order deletion        
class DeleteOrder(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data # Extracting data from the request body

        if "id" in data:  # If 'id' is provided, delete the order
            order=Order.objects.filter(id=data['id'])  #Get order by id
            order.delete() # deleting the order
            return Response("Order detail delete successful")
        else:
            return Response("Order detail not deleted")       
     
       
# ListPayment API class to handle listing payments based on amount        
class ListPayment(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        data=request.query_params   # Extracting query parameters (amount)
        payment = Payment.objects.filter(amount=data['amount'])  # Filtering payments by amount
        serializer = ListPaymentSerializer(payment,many=True).data  # Serializing the payments
        return Response({"Payment":serializer})   # Returning the serialized payment data
    
    authentication_classes = []
    permission_classes = []    
    def get_instance_payment(self,Payment,id):
        instance=object(Payment,id)
        return ({instance})
        
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data=request.data 
        # Similar logic to GET but excluding by amount
        payment=Payment.objects.all()

        if 'amount' in data:
            payment=payment.filter(amount=data['amount'])
        if 'payment_method' in data:
            payment=payment.filter(payment_method=data['payment_method'])
        if 'payment_time' in data:
            payment=payment.filter(payment_time=data['payment_time'])
        if 'status'in data:
            payment=payment.filter(status=data['status'])
        if 'order' in data:
            payment=payment.filter(order=data['order'])
        serializer = ListPaymentSerializer(payment,many=True).data
        return Response({"Payment":serializer})   # Returning the serialized data

class GetPaymentDetails(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data
        payment=Payment.objects.get(id=data['id'])
        serializers=ListPaymentSerializer(payment).data
        return Response({"det payment details":serializers})

# CreatePayment API class to handle payment creation and updates    
class CreatePayment(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data=request.data # Extracting data from the request body

        
        if 'id' in data:  # If 'id' is provided, update the payment
            payment=Payment.objects.get(id=data['id']) #Get payment by id
            #order = payment.order  # Assuming the payment is related to an order

            payment.order.table.capacity=data['table']['capacity']
            order.table.number=data['table']['number']
            order.table.is_occupied=data['table']['is_occupied']
            order.table.save()

            order.customer.name=data['customer']['name'] #update customer name
            order.customer.phone_number=data['customer']['phone_number'] #update customer phone number
            order.customer.email=data['customer']['email'] # update customer email
            order.customer.save()
            "================="
            payment.amount=data['amount'] #update amount
            payment.payment_method=data['payment_method'] # update payment method
            payment.payment_time=data['payment_time']
            payment.status=data['status']
            payment.save() #Save payment changes
            return Response('Payment updated successful')
        else:
            # Creating a new payment if 'id' is not provided
            payment_detail={} # create payment
            payment_detail['amount']=data['amount'] #Assign amount
            payment_detail['payment_method']=data['payment_method'] #Assign payment menthod
            payment_detail['payment_time']=data['payment_time']
            payment_detail['status']=data['status']
            
            table_detail={}
            table_detail['capacity']=data['table']['capacity']
            table_detail['number']=data['table']['number']
            table_detail['is_occupied']=data['table']['is_occupied']
            table=Table.objects.create(**table_detail)
            
            customer_detail={} # create a new customer details
            user={}
            user['username']=data['customer']['username']
            user['email']=data['customer']['email']
            user['first_name']=data['customer']['first_name']
            user=User.objects. create(**user)

            token = Token.objects.create(user=user)
            print(token.key)
            #customer_detail['name']=data['customer']['name'] # Assign customer name
            customer_detail['phone_number']=data['customer']['phone_number'] #Assign phone number
            #customer_detail['email']=data['customer']['email'] #Assign email
            customer_detail['user']=user
            customer= Customer.objects.create(**customer_detail) #create  new customer

            order_detail={}
            order_detail['table']=table #Assign table to order
            order_detail['customer']=customer #Assign customer to order


            order = Order.objects.create(**order_detail) #create order objects
            order.menu_items.set(data['menu_items']) # Assigning menu items to the order
            order.save() # saving the order

            payment_detail['order']=order
            # payment_detail['customer']=customer

                
        # Code inside the view after `payment` creation
        payment = Payment.objects.create(**payment_detail)  # Payment creation logic

        # Generate report after payment creation
        buffer = generate_order_report(order, payment)

        # Return the PDF as an HTTP response
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="order_{order.id}_receipt.pdf"'
        buffer.close()
        return response

            
    
    
#payment = Payment.objects.create(**payment_detail) #create new payment
# return Response({"Payment":"payment creation successful"})
    
 # DeletePayment API class to handle payment deletion   
class DeletePayment(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data # Extracting data from the request body

        if "id" in data: # If id is provided delete the payment
            payment=Payment.objects.get(id=data['id']) #Get payment id
            payment.delete() # Deleting the payment
            return Response("Payment detail delete successful")
        else:
            return Response("payment detail not deleted")
        



def generate_order_report(order, payment):
    """Generates a PDF report for the order and payment details."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Payment Receipt")
    pdf.setFont("Helvetica", 12)

    # Order and customer details
    pdf.drawString(100, 720, f"Order ID: {order.id}")
    pdf.drawString(100, 700, f"Table Number: {order.table.number}")
    pdf.drawString(100, 680, f"Customer Name: {order.customer.user.first_name}")
    pdf.drawString(100, 660, f"Customer Phone: {order.customer.phone_number}")
    pdf.drawString(100, 640, f"Customer Email: {order.customer.user.email}")


    # Menu items details
    y_position = 620
    pdf.drawString(100, y_position, "Ordered Items:")
    y_position -= 20

    total_amount = 0
    for order_item in order.orderitem_set.all():
        menu_item = order_item.menu_item 
        quantity = order_item.quantity
        price = menu_item.price
        line_total = quantity * price
        total_amount += line_total
        pdf.drawString(120, y_position, f"{menu_item.name} x {quantity} @ {price} = {line_total}")
        y_position -= 20

    # Payment details
    GST_PERCENTAGE = 5
    gst_amount = total_amount * GST_PERCENTAGE / 100
    total_with_gst = total_amount + gst_amount

    y_position -= 20
    pdf.drawString(100, y_position, "Payment Details:")
    y_position -= 20
    pdf.drawString(120, y_position, f"Payment Amount: {payment.amount}")
    pdf.drawString(120, y_position - 20, f"Payment Method: {payment.payment_method}")
    pdf.drawString(120, y_position - 40, f"Payment Status: {payment.status}")
    pdf.drawString(120, y_position - 60, f"GST ({GST_PERCENTAGE}%): {gst_amount}")
    pdf.drawString(120, y_position - 80, f"Total Amount Paid: {total_with_gst}")

    # Thank you note
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 120, "Thank you for dining with us!")

    pdf.save()
    buffer.seek(0)
    return buffer






       
           
