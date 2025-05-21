from django.shortcuts import get_object_or_404, render,redirect
from .forms import CustomerSignUpForm
from .models import CustomUser,CustomerProfile,Product,Category,Cart,Address,Order,OrderItems
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from datetime import datetime,timedelta



# Create your views here.
def index(request):
    selected_categories=request.GET.getlist('category')
    products=Product.objects.all()
    categories=Category.objects.all()
    sort_order=request.GET.get('sort')
    search=request.GET.get('search')

    if selected_categories:
        products=Product.objects.filter(category__id__in = selected_categories).distinct()
    else:
        products=Product.objects.all()

    if sort_order == 'asc':
        products=products.order_by('price')
    elif sort_order == 'desc':
        products=products.order_by('-price')
        # give dash beside price is descending    

    if search:
        products=Product.objects.filter(name__icontains=search)
        # write i to do insensitive content

    context={
        'products':products,
    'categories':categories,
    'selected_categories':list(map(int,selected_categories)),
    'sort_order':sort_order
    }
    return render(request, 'index.html',context)

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            image=form.cleaned_data['image']
            contact=form.cleaned_data['contact']
            if password != confirm_password:
                messages.error(request, 'Password and Confirm Password does not match')
                return redirect('customer-signup')
            
            else:
                try:
                    user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=first_name,last_name=last_name,is_customer=True,contact=contact)
                    user.save()

                    customer=CustomerProfile(user=user,image=image)
                    customer.save()
                    return redirect('customer-signin')
                except:
                    messages.error(request, 'An error occurred while creating the account. Please try again.')
                    return redirect('customer-signup')
    else:
        form=CustomerSignUpForm()
    context={'form':form}    
    return render(request,'customer_signup.html',context)

def customer_signin(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('customer-signin')
    else:
        form = AuthenticationForm()

    context={'form':form}    
    return render(request,'customer_signin.html',context)

def customer_signout(request):
    logout(request)
    return redirect('customer-signin')

def customer_profile(request,id):
    return render(request, 'customer_profile.html')

def product_details(request,id):
    product = Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category.id).exclude(id=product.id)
    context = {'product': product, 
               'date': datetime.today().date()+timedelta(days=5),
               'related_products':related_products
               }
    return render(request, 'product_details.html', context)

def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    try:
        user=CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    cart_item,created=Cart.objects.get_or_create(product=product, user=user)

    if not created:
        cart_item.quantity+=1

    cart_item.save()

    return redirect('index')

def cart(request):
    try:
        user=CustomUser.objects.get(id=request.user.id)
        mycart=Cart.objects.filter(user=user)

        total_amount=0
        total_items=0


        for cart in mycart:
            total_amount+=cart.product.price*cart.quantity
            total_items+=cart.quantity

        gst=total_amount*3/100


    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    context={
        'mycart':mycart,
        'total_amount':total_amount,
        'total_items':total_items,
        'gst':gst
    }

    return render(request,'cart.html',context)

def update_quantity(request,id):
    product = Cart.objects.get(product=id,user=request.user.id)
    var=request.GET.get('q')
    if var=='0':
        if product.quantity>1:
            product.quantity-=1
        else:
            product.quantity=1
    else:
        product.quantity+=1
    product.save()
    return redirect('cart')

def remove_cart(request,id):
    product = Cart.objects.get(product=id,user=request.user.id)
    product.delete()
    return redirect('cart')

def address(request):
    if request.method =='POST':
        pass
    else:
        user_profile=CustomerProfile.objects.get(user=request.user)
        addresses=user_profile.address.all()
        context={
            'addresses':addresses
        }
    return render(request, 'address.html',context)

def confirm_order(request,id):
    address=Address.objects.get(id=id)
    try:
        user=CustomUser.objects.get(id=request.user.id)
        mycart=Cart.objects.filter(user=user)

        total_amount=0
        total_items=0


        for cart in mycart:
            total_amount+=cart.product.price*cart.quantity
            total_items+=cart.quantity

        gst=total_amount*3/100


    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    context={
        'mycart':mycart,
        'total_amount':total_amount,
        'total_items':total_items,
        'gst':gst,
        'address':address
    }

    return render(request,'confirm_order.html',context)

import random
import razorpay # type: ignore

def payment(request,id):
    if request.user.is_authenticated:
        try:
            user=CustomUser.objects.get(id=request.user.id)
            user_profile = CustomerProfile.objects.get(id = request.user.id)
            mycart = Cart.objects.filter(user=user)
            address=Address.objects.get(id=id)

            total_amount = 0

            for cart in mycart:
                total_amount += cart.product.price * cart.quantity

            gst = total_amount * 3 / 100
            order_amount = gst + total_amount
            order_id=random.randrange(1000,9999)

            order=Order.objects.create(order_id=order_id,customer=user_profile,shipping_address=address,order_amount=order_amount)
            order.save()

            for cart in mycart:
                OrderItems.objects.create(order_id=order,product=cart.product,quantity=cart.quantity,unit_price=cart.product.price)

            mycart.delete()

            client = razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ", "UOrbXQGnsEc2dhB1IFg0zNWZ"))

            data = { "amount": int(order_amount*100), "currency": "INR", "receipt": str(order_id) }

            payment = client.order.create(data=data)


            context={
                'data':data,
                'payment':payment,
            }

        except CustomUser.DoesNotExist:
            return redirect('customer-signin')

    return render(request,'payment.html',context)

def payment_success(request):
    payment_id=request.GET.get('payment_id','N/A')
    order_id=request.GET.get('order_id','N/A')
    order=get_object_or_404(Order,order_id=order_id)
    
    order.payment_status='paid'

    context={
        'payment_id':payment_id,
        'order_id':order_id
    }
    return render(request,'payment_success.html',context)

def generate_otp():
    otp=str(random.randrange(100000,999999))
    return otp 
# random otp function no need of views and urls same for all project


from django.core.mail import send_mail
from django.conf import settings

def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        try:
            user=CustomUser.objects.get(email=email)
            otp=generate_otp()

            request.session['otp']=otp #will send otp in email ir=t will check with otp stored in browser

            request.session['request_user']=user.id #will store otp in browsser

            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is : {otp}',

                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            return redirect('verify-otp')

        except CustomUser.DoesNotExist:
            messages.error(request,'email does not exist')
    return render(request,'forgot_password.html')


def verify_otp(request):
    if request.method=='POST':
        otp_entered = request.POST.get('otp') 
        otp_stored=request.session['otp']

        if otp_entered==otp_stored:
            user_id=request.session['request_user']
            if user_id:
                user=CustomUser.objects.get(id=user_id)
                return redirect('reset-password',user_id=user.id)
            else:
                messages.error(request,'Session expired please request for OTP again')


            
        else:
            messages.error(request,'Invalid OTP')

            return redirect('verify-otp')
    return render(request,'verify_otp.html')


from django.contrib.auth.forms import SetPasswordForm

def reset_password(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    
    if request.method=='POST':
        form=SetPasswordForm(user=user,data=request.POST)
        if form.is_valid():
            form.save()
            if 'otp' in request.session:
                del request.session['otp']

            if 'request_user' in request.session:
                del request.session['request_user']

            messages.success(request,'Your Password has been reset successfully')
            return redirect('customer-signin')

    else:
        form=SetPasswordForm(user=user)
    return render (request,'reset_password.html',{'form':form})