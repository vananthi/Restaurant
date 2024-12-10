from django.urls import path
from . import views


urlpatterns = [
    path('listMenuItem', views.ListMenuItem.as_view(), name='listMenuItem'),
    path('listCategory', views.ListCategory.as_view(), name='listCategory'),
    path('listTable',views.ListTable.as_view(),name='listTable'),
    path('getMenuItemDetail',views.GetMenuItemDetail.as_view(),name='getMenuItemDetail'),
    path('getCategoryDetail',views.GetCategoryDetail.as_view(),name='getCategoryDetail'),
    path('getTableDetail',views.GetTableDetail.as_view(),name='getTableDetail'),
    path('createMenuItem',views.CreateMenuItem.as_view(),name='createMenuItem'),
    path('createCategory',views.CreateCategory.as_view(),name='createCategory'),
    path('createTable',views.CreateTable.as_view(),name='createTable'),
    path('updateMenuItem',views.CreateMenuItem.as_view(),name='updateMenuItem'),
    path('updateCategory',views.CreateCategory.as_view(),name='updateCategory'),
    path('updateTable',views.CreateTable.as_view(),name='updateTable'),
    path('deleteMenuItem',views.DeleteMenuItem.as_view(),name='deleteMenuItem'),
    path('deleteCategory',views.DeleteCategory.as_view(),name='deleteCategory'),
    path('deleteTable',views.DeleteTable.as_view(),name='deleteTable'),
    path('get_instance_menu_item', views.ListMenuItem.as_view(), name='get_instance_menu_item'),
    path('get_instance_category', views.ListCategory.as_view(), name='get_instance_category'),
    path('get_instance_table', views.ListTable.as_view(), name='get_instance_table'),
    path('weeklyCalendar',views.WeeklyCalendar.as_view(), name='weeklyCalendar')
]





