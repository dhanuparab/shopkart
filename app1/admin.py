from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Address,CustomerProfile,SellerProfile,Category,Product,Cart,Order,OrderItems

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=[field.name for field in CustomUser._meta.fields]


class CustomerPofileAdmin(admin.ModelAdmin):
    list_display=[field.name for field in CustomerProfile._meta.fields]

class SellerProfileAdmin(admin.ModelAdmin):
    list_display=[field.name for field in SellerProfile._meta.fields]

class AddressAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Address._meta.fields]

class CategoryAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Category._meta.fields]

class ProductAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Product._meta.fields]

class CartAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Cart._meta.fields]    

class OrderAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Order._meta.fields]  

class OrderItemAdmin(admin.ModelAdmin):
    list_display=[field.name for field in OrderItems._meta.fields]  


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(CustomerProfile,CustomerPofileAdmin)
admin.site.register(SellerProfile,SellerProfileAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemAdmin)


