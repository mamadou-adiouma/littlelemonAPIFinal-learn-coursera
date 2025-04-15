from django.contrib import admin
from LittlelemonAPI.models import MenuItem, Category, Cart, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('title', 'slug')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
     list_display = ('title', 'price', 'category')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
     list_display = ('user', 'menuitem', 'quantity', 'unit_price', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     list_display = ('user', 'delivery_crew', 'status', 'total')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
     list_display = ('order', 'user', 'menuitem', 'quantity', 'unit_price', 'price')