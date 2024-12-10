from rest_framework import serializers # Importing Django Rest Framework's serializers module
from .models import * # Importing all models from the current directory's models.py file

# Serializer for MenuItem model
class ListMenuItemSerializer(serializers.ModelSerializer):
    # SerializerMethodField is used to add a custom field (category_detail) which is derived from a method
    category_detail=serializers.SerializerMethodField()  

    class Meta:
        model = MenuItem # Specifies that this serializer is for the MenuItem model
        fields = ['name', 'price','description','available','category_detail','image'] # These are the fields that will be included in the serialized output
    # This method gets extra details about the category related to the MenuItem
    def get_category_detail(self,obj):
        return{
               'name':obj.category.name,  # Retrieves the name of the category
               'description':obj.category.description # Retrieves the description of the category
        }

class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ['id', 'name']

class WeeklyCalendarSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyCalendar
        fields = ['menu_items']

    
    def get_menu_items(self, obj):
     menu_items = {}

     if obj.day_mon:
        menu_items["Monday"] = obj.day_mon.name
     else:
        menu_items["Monday"] = "No Menu Item"

     if obj.day_tue:
        menu_items["Tuesday"] = obj.day_tue.name
     else:
        menu_items["Tuesday"] = "No Menu Item"

     if obj.day_wed:
        menu_items["Wednesday"] = obj.day_wed.name
     else:
        menu_items["Wednesday"] = "No Menu Item"

     if obj.day_thu:
        menu_items["Thursday"] = obj.day_thu.name
     else:
        menu_items["Thursday"] = "No Menu Item"

     if obj.day_fri:
        menu_items["Friday"] = obj.day_fri.name
     else:
        menu_items["Friday"] = "No Menu Item"

     if obj.day_sat:
        menu_items["Saturday"] = obj.day_sat.name
     else:
        menu_items["Saturday"] = "No Menu Item"

     if obj.day_sun:
        menu_items["Sunday"] = obj.day_sun.name
     else:
        menu_items["Sunday"] = "No Menu Item"

     return menu_items
        
 # Serializer for Category model
class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category # Specifies that this serializer is for the Category model
        fields=['id','name','description']  # These are the fields that will be included in the serialized output

        
# Serializer for Table model
class ListTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table # Specifies that this serializer is for the Table model
        fields = ['number','capacity','is_occupied'] # These are the fields that will be included in the serialized output
