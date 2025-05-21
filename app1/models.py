from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class Address(models.Model):
    address_line=models.CharField(max_length=255)
    street= models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    landmark=models.CharField(max_length=255)
    pincode=models.CharField( max_length=50,validators=[RegexValidator(regex=r'^\d{6}$',message='enter pincode')])


class CustomUser(AbstractUser):
    is_seller=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)
    contact=models.CharField(max_length=10,validators=[RegexValidator(regex=r'^\d{10}$', message='contact must be 10 numbers')])
    email=models.EmailField(unique=True)

    class Meta:
        verbose_name = 'CustomUser'

class CustomerProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE ,related_name='customer_profile')
    image=models.ImageField(upload_to='customer_image',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    address=models.ManyToManyField(Address,related_name='customer_address', blank=True,null=True)

class SellerProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE ,related_name='seller_profile') 
    business_name=models.CharField(max_length=10)
    gst_number=models.CharField(max_length=15,validators=[RegexValidator(regex=r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[A-Z0-9]{1}$',message='27ABCDE1234F1Z5')])
    business_address=models.TextField()


class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    def  __str__(self):
        return self.name
        

class Product(models.Model):
        name=models.CharField(max_length=255,unique=True)
        category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
        price=models.DecimalField(max_digits=10, decimal_places=2)
        description=models.TextField(blank=True)
        image=models.ImageField(upload_to='product_images', blank=True, null=True)
        stock=models.PositiveIntegerField(default=0)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)

class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order(models.Model):
    order_id=models.CharField(max_length=50, primary_key=True)
    customer=models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    order_date=models.DateField(auto_now_add=True)
    shipping_address=models.ForeignKey(Address,on_delete=models.CASCADE)
    payment_status=models.CharField(max_length=20,choices=(('paid','Paid'),('unpaid','Unpaid')),default='unpaid')
    order_status=models.CharField(max_length=50,choices=(('pending','Pending'),('shipped','Shipped'),('delivered','Delivered')),default='pending')
    order_amount=models.DecimalField(max_digits=10, decimal_places=2)

    
class OrderItems(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    
    