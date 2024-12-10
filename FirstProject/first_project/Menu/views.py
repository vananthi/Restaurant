

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import * # Importing all models
from .serializers import * # Importing all serializers
from rest_framework import authentication, permissions

# API View to list and filter menu items
class ListMenuItem(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):  #Handle GET request for listing menu items
        data=request.query_params # Get query parameters

# Filter menu items by name, category, and price, then order by price        
        menuitem = MenuItem.objects.filter(name=data['name'],category=data['category'],price = data['price'],available=True).order_by('-price')
        serializer = ListMenuItemSerializer(menuitem,many=True).data # Serialize the filtered menu items
        return Response({"List_of_menu_item":serializer})
    
    authentication_classes = []
    permission_classes = []
    def get_instance_menu_item(self,MenuItem,id):
        instance=object(MenuItem,id)
        return ({instance})
   

    def post(self, request):   # Handle POST request for listing menu items
        data=request.data  # Get data from POST request

  # Start with all items      
        menuitem = MenuItem.objects.all()
         # Filter by name if provided in request data
        if 'name' in data:
         
         menuitem = menuitem.filter(name__icontains=data['name'])  # Filter by name

    # Filter by category if provided
        if 'category' in data:
          menuitem = menuitem.filter(category__name__icontains=data['category'])  # Assuming you're filtering by category name

    # Filter by price if provided
        if 'price' in data:
         menuitem = menuitem.filter(price=data['price'])  # Exact match for price, or use __lte/__gte for ranges

        if 'available' in data:
            menuitem=menuitem.filter(available=data['available'])

    # Order by price
        # menuitem = menuitem.order_by('price')
        serializer = ListMenuItemSerializer(menuitem,many=True).data  # Serialize the filtered menu items
        return Response({"List_of_menu_item":serializer})
 
 #API View to get menuitem details   
class GetMenuItemDetail(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data
        menuitem = MenuItem.objects.get(id=data['id'])
        serializer = ListMenuItemSerializer(menuitem).data # Serialize the filtered menu items
        return Response({"get_menu_item":serializer})
   
class WeeklyCalendar(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data= request.data
        calendar = WeeklyCalendar.objects.all().first()  # Adjust to get the desired calendar instance
        serializer = WeeklyCalendarSerializer(calendar).data
        return Response(serializer)
    
# API View to create or update a menu item
class CreateMenuItem(APIView):  
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data=request.data # Get data from POST request


        if 'id' in data: # If id exists, update the existing menu item
            menuitem=MenuItem.objects.get(id=data['id']) # Get menu item by id
            menuitem.name=data['name'] #update name
            menuitem.price=data['price'] #update price
            menuitem.available=data['available'] # update availablity
            menuitem.image=data['image'] # update image

            menuitem.category.name=data['category']['name'] #update categpry name
            menuitem.category.description=data['category']['description'] #update category description
            menuitem.category.save() #save category changes
            
            menuitem.save() ## Save menu item changes
            return Response({"Menuitem Updated successfully"})
        else:
            
            menuitems={} # Create a new menu item
            menuitems['name']=data['name'] # Assign name
            menuitems['price'] = data['price'] #Assign price
            menuitems['available']=data['available'] #Assign availablity
            menuitems['image']=data['image'] #Assign image

           
            
            category_items = {} # Create a new category and assign it to the menu item
            category_items['name']=data['category']['name'] #Assign category name
            category_items['description']=data['category']['description']
            category = Category.objects.create(**category_items) # Create category object
           
            menuitems['category'] = category ## Assign category to menu item
            menuitem = MenuItem.objects.create(**menuitems) # Create new menu item
            return Response({"Menuitem created successfuly"})
        
# API View to delete a menu item        
class DeleteMenuItem(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data  # Get data from POST request

       
        if 'id' in data: # If id exists, delete the menu item
            menuitem=MenuItem.objects.get(id=data['id']) # Get menu item by id
            menuitem.delete() # Delete the menu item
            return Response({"MenuItem Deleted Successfully"})
        else:
            return Response({"MenuItem not found"})
    
# API View to list and filter category  
class ListCategory(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request): # Handle GET request for listing category
        data=request.query_params #Get query params

# Filter category by name
        category = Category.objects.filter(name=data['name'],description=data['description'])
        serializer = ListCategorySerializer(category,many=True).data
        return Response({"list_of_Category":serializer})
    
    authentication_classes = []
    permission_classes = []
    
    def get_instance_category(self,Category,id):
        instance=object(Category,id)
        return ({instance})
    
    authentication_classes = []
    permission_classes = []
    def post(self,request): # Handle POSTrequest for listing category
        data=request.data # Get data from POST request
        category = Category.objects.all()

        if 'name' in data:
            category=category.filter(name__icontains=data['name'])
        
        serializer = ListCategorySerializer(category,many=True).data
        return Response({"list_of_Category":serializer})

class GetCategoryDetail(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data
        
        category = Category.objects.get(id=data['id'])
        print(category)
        serializer = ListCategorySerializer(category).data
        print(serializer,"--------------")

        return Response({"get category detail":serializer})
    
    
#API View to create or upload a category
class CreateCategory(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data # Get data from POST request

        if 'id' in data: # If id exists, update the existing category
            category=Category.objects.get(id=data['id']) # Get categorty by id
            category.name=data['name'] # update name
            category.description=data['description'] # update description
            category.save() #save category changes
            return Response({"Category updated successful"})
        else:
            category = Category.objects.create(name=data['name'],description=data['description']) #create a new category
            return Response("category create successfully")
        
# API View to delete a category       
class DeleteCategory(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data # Get data from POST request

        if 'id' in data: #If id exsist,delete a category
             category=Category.objects.get(id=data['id']) #Get category id
             category.delete() # delete the category
             return Response({"Category Delete Successful"})
        else:
            return Response({'Category Not found'})

#API View list and filter a table
class ListTable(APIView):
     authentication_classes = [authentication.TokenAuthentication]
     permission_classes = [permissions.IsAuthenticated]
     def post(self,request): #Handle GET request for listing table
        data=request.data # Get data from POST request

    

#filter table from capacity,number,is occupied then order by number        
        table = Table.objects.all()

        if 'capacity' in data:
            table=table.filter(capacity=data['capacity'])
        if 'number' in data:
            table=table.filter(number=data['number'])
        if 'is_occupied' in data:
            table=table.filter(is_occupied=data['is_occupied'])

    
        serializers = ListTableSerializer(table,many=True).data
        return Response({" list_of_table":serializers})
     
     authentication_classes = []
     permission_classes = []
     def get_instance_table(self,Table,id):
         instance=object(Table,id)
         return({instance})
    
class GetTableDetail(APIView):
    authentication_classes = []
    permission_classes = []
    def post (self,request):
        data=request.data
        print(data,11111111111111111)
        table=Table.objects.get(id=data['id'])
        print(table,22222222222222222)
        serializer = ListTableSerializer(table).data
        print(serializer,3333333333333333333)
        return Response({"get table detail":serializer})    
    
    
# API View to create or update atable    
class CreateTable(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request): #Handle GET request for listing table
        data=request.data # Get data from POST request

        if 'id' in data: # If id exsist,update a table
            table=Table.objects.get(id=data['id']) #Get table id
            table.capacity=data['capacity'] #upload capacity
            table.number=data['number'] # upload number
            table.is_occupied=data['is_occupied']  # Update is_occupied status
            table.save() #save table changes
            return Response({"Table update successful"})
        else:
            table = Table.objects.create(capacity=data['capacity'],number=data['number'],is_occupied=data['is_occupied']) #create a new table
            return Response({"Table creation successfuly"})
        
# API View to delete a table        
class DeleteTable(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        data=request.data

        if 'id' in data: #If id exsist ,delete a table
            table=Table.objects.get(id=data['id']) # Get table id
            table.delete() #delete a table
            return Response({"Table delete successful"})
        else:
            return Response({"Table not found"})
        