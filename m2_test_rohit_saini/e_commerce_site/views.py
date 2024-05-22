from django.http import HttpResponse
from django.views import View
from .models import product_management,UserProduct,shiping_detail,ordered
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
def none(request):
    return redirect('home')
def delete(request,id):
    try:
        if not request.user.is_superuser and not request.user.is_staff:
            return redirect('home')
        obj=product_management.objects.get(pk=id)
        obj.delete()
        return redirect('admin')
    except Exception as e:
        return HttpResponse(e)
#@decorator
def create(request):
    try:
        if not request.user.is_superuser and not request.user.is_staff:
            return redirect('home')
        if request.method == 'POST' or request.FILES:
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            quantity = request.POST['quantity']
            image = request.FILES['image']
            isinstance = product_management(name=name, description=description, price=price, quantity=quantity,
                                            image=image)
            isinstance.save()
            return redirect('admin')
        return render(request, 'create_product.html')

    except Exception as e:
        return HttpResponse(e)

class update(View):
    temp='update_item.html'


    def get(self,request,id):
        try:
            if not request.user.is_superuser and not request.user.is_staff:
                return redirect('home')
            obj=product_management.objects.filter(pk=id)
            return render(request,self.temp,{'data':obj})
        except Exception as e:
            return HttpResponse(e)


    def post(self,request,id):
        try:
            if not request.user.is_superuser and not request.user.is_staff:
                return redirect('home')
            if request.method=='POST' or request.file:
                name = request.POST['name']
                description = request.POST['description']
                price = request.POST['price']
                quantity = request.POST['quantity']
                if 'image' in request.FILES:
                    image = request.FILES['image']
                else:
                    image=None

                item = product_management.objects.get(pk=id)
                item.name=name
                item.description=description
                item.price=price
                item.quantity=quantity
                if image is not None:
                    item.image=image
                item.save()
                messages.success(request, 'Your model instance has been created/updated successfully.')
                return redirect('admin')
            return redirect('update')
        except Exception as e:
            return HttpResponse(e)

def signup(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            password2=request.POST['password2']
            email = request.POST['email']
            # Check if username is already taken
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'Username already taken'})
            elif len(password) < 8:
                return render(request, 'signup.html', {'error': 'password too short'})
            elif password2 != password:
                return render(request, 'signup.html', {'error': 'password not same'})
            elif  not any(char in '!@#$%^&*()_+{}":;\'>?<,./|\\' for char in password):
                return render(request, 'signup.html', {'error': 'use any special character'})
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                return redirect('login')
        return render(request, 'signup.html')
    except Exception as e:
        return HttpResponse(e)



class home(View):
    def get(self,request):
        ob=product_management.objects.all()
        obj=ob[:12]
        total_items = len(obj)
        half_index = total_items // 2
        f = obj[:half_index]
        s = obj[half_index:]
        first=f[:half_index]
        second=f[half_index:]
        third=s[:half_index]
        forth=s[half_index:]
        if request.user.is_authenticated:
            user=request.user
        else:
            user='Login'
        context = {
            'first': first,
            'second': second,
            'third':third,
            'forth':forth,
            'data':ob[::-1],
            'username':user,
            'circle':ob[3:8],
            'pro':ob[1:4],
        }


        return render(request,'home.html',context)



def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            request.session['username'] = username
            messages.success(request, 'You have been logged in successfully.')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('admin'))
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            return render(request, 'login.html')
    except Exception as e:
        return HttpResponse(e)

def user_logout(request):
    try:
        logout(request)



        if 'username' in request.session:
            del request.session['username']
            messages.success(request, 'You have been logged out successfully.')



        return redirect(reverse('home'))
    except Exception as e:
        return HttpResponse(e)
class admin(View):
    tem='admin.html'


    def get(self,request):

        try:
            if not request.user.is_superuser and not request.user.is_staff:
                return redirect('home')
            obj=product_management.objects.all()
            total_items = len(obj)
            half_index = total_items // 2
            first_half = obj[:half_index]
            second_half = obj[half_index:]

            context = {
                'first_half': first_half,
                'second_half': second_half,
            }

            return render(request,self.tem,context)
        except Exception as e:
            return HttpResponse(e)

class select_item(View):


    def get(self,request,id):
        try:
            if request.user.is_authenticated:
                user = request.user
            else:
                user = 'Login'
            obj=product_management.objects.get(pk=id)
            obj1=product_management.objects.all()
            obj2=obj1[::-1]
            contex={'data':obj,'data2':obj1,'data3':obj2,'username':user}

            return render(request,'select_item.html',contex)
        except Exception as e:
            return HttpResponse(e)

    def post(self,request,id):
        try:

            if request.method=='POST':

                if not request.user.is_authenticated:
                    user='login'
                    return redirect('login')
                else:
                    user = request.user
                    user_quantity=int(request.POST['quantity'])
                    product = get_object_or_404(product_management, pk=id)
                    obj=product_management.objects.get(pk=id)
                    if obj.quantity < user_quantity:
                        obj = product_management.objects.get(pk=id)
                        obj1 = product_management.objects.all()
                        obj2 = obj1[::-1]
                        contex = {'data': obj, 'data2': obj1, 'data3': obj2,'error':'enter quantity out of stoke','username':user}

                        return render(request, 'select_item.html', contex)

                    price=obj.price
                    cart=UserProduct(user=request.user,product=product,quantities=user_quantity,total_price=user_quantity*price)
                    cart.save()
            return redirect('home')
        except Exception as e:
            return HttpResponse(e)
class cart(View):

    def get(self,request):
        try:
            if not request.user.is_authenticated:
                return redirect('login')

            obj1=UserProduct.objects.filter(user=request.user)


            return render(request,'cart.html',{'obj':obj1,'username':request.user})
        except Exception as e:
            return HttpResponse(e)

    def post(self,request):
        try:
            if not request.user.is_authenticated:
                return redirect('login')
            if request.method=='POST':
                quantity=int(request.POST['quantities'])
                id=request.POST['id']
                obj=UserProduct.objects.get(pk=id)

                price=obj.total_price//obj.quantities

                obj.quantities=quantity
                obj.total_price=quantity*price

                obj.save()

            return redirect('cart')
        except Exception as e:
            return HttpResponse(e)

def delete_cart_product(request,id):
    try:
        obj=UserProduct.objects.get(pk=id)
        obj.delete()
        return redirect('cart')
    except Exception as e:
        return HttpResponse(e)
class checkout(View):
    def get(self,request):
        try:
            if not request.user.is_authenticated:
                return redirect('login')
            return render(request,'checkout.html',{'username':request.user})
        except Exception as e:
            return HttpResponse(e)

    def post(self,request):
        try:
            if request.method=='POST':

                name=request.POST['name']
                email=request.POST['email']
                address=request.POST['address']
                phone=request.POST['phone']
                card=request.POST['card']
                expiry=request.POST['expiry']
                cvv=request.POST['cvv']
                obj=shiping_detail(user=request.user,name=name,email=email,address=address,phone=phone,card=card,expiry=expiry,cvv=cvv)
                obj.save()


                li=[]
                object=UserProduct.objects.filter(user=request.user)



                for i in object:

                        objj=ordered(user=request.user,product=i.product,total_price=i.total_price,status='packing')
                        objj.save()
                        user_id = objj.id
                        li.append(user_id)
                        obj1=UserProduct.objects.get(pk=i.pk)
                        obj1.delete()

                        oobj=product_management.objects.get(name=i.product)
                        oobj.quantity=oobj.quantity-i.quantities
                        oobj.save()




                superusers = User.objects.filter(is_superuser=True)
                superusers_email = [user.email for user in superusers]
                usr=User.objects.get(username=request.user)
                try:
                    subject1 = 'Order Confirmation'
                    subject2='New Order'
                    message1 = f'Thank you for your order! Your order has been successfully placed.orders id_s={ li }.'
                    message2 = f'New order will be added by { request.user }.https://www.apple.com/in/'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list1 = [usr.email]
                    recipient_list2 = superusers_email

                    send_mail(subject1, message1, email_from, recipient_list1)
                    send_mail(subject2, message2, email_from, recipient_list2)
                except:
                    print("enter you email or password to send emals")

            return redirect('orders')
        except Exception as e:
            return HttpResponse(e)

        finally:
            return redirect('orders')
def orders(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        obj=ordered.objects.filter(user=request.user)

        return render(request,'orders.html',{'data':obj,'username':request.user})
    except Exception as e:
        return HttpResponse(e)
class admin_order(View):

    def get(self,request):
        try:


            if not request.user.is_superuser or not request.user.is_staff:
                return redirect('login')



            obj = ordered.objects.all()


            return render(request,'admin_orders.html',{'data':obj})
        except Exception as e:
            return HttpResponse(e)

    def post(self,request):
        try:
            if request.method=='POST':
                status=request.POST['status']
                id=request.POST['id']

                obj=ordered.objects.get(pk=id)
                obj.status=status
                obj.save()
                return redirect('admin_orders')
        except Exception as e:
            return HttpResponse(e)
