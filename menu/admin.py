from django.contrib import admin
from .models import Category, MenuItem, CartItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')  
    fields = ('name', 'priority')        
    
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'priority')  
    list_filter = ('category',)
    search_fields = ('name',)
    fields = ('category', 'name', 'description', 'price', 'image', 'priority') 
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(CartItem)

