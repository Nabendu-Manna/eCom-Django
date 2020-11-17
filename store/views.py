from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as djLogout
from itertools import chain
import datetime
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

#############################################################################

#Brand
def insertBrand(request):
     form = uploadBrandForm()
     return render(request, 'products/insertBrand.html', {'form': form})

def uploadBrand(request):
     if request.method == 'POST':
          form = uploadBrandForm(request.POST, request.FILES)
          if form.is_valid():
               brandName = request.POST['name']
               checkBrand = Brands.objects.filter(name = brandName)
               if not checkBrand:
                    form.save()
                    
     return redirect('insertBrand/')

def byBrand(request):
     if request.method == 'GET':
          brandId = request.GET['id']
          data = Product.objects.filter(brandId = brandId)
          return render(request, 'products/products.html', { 'data': data})

#end Brand

#Catagory
def insertCatagory(request):
     form = uploadCatagoryForm()
     return render(request, 'products/insertCatagory.html', {'form': form})

def uploadCatagory(request):
     if request.method == 'POST':
          form = uploadCatagoryForm(request.POST, request.FILES)
          if form.is_valid():
               catagoryName = request.POST['name']
               checkCatagory = Catagories.objects.filter(name = catagoryName)
               if not checkCatagory:
                    form.save()
     
     return redirect('insertCatagory/')

def byCatagory(request):
     if request.method == 'GET':
          catagoryId = request.GET['id']
          data = Product.objects.filter(catagoryId = catagoryId)
          return render(request, 'products/products.html', { 'data': data})

#end Catagory

#Product
def insertProduct(request):
     form = uploadProductForm()
     catagories = Catagories.objects.all()
     brands = Brands.objects.all()
     context = {'form': form,'catagories': catagories, 'brands': brands}
     return render(request, 'products/insertProduct.html', context)

def uploadProduct(request):
     if request.method == 'POST':
          form = uploadProductForm(request.POST, request.FILES)
          if form.is_valid():
               productName = request.POST['name']
               checkProduct = Product.objects.filter(name = productName)
               if not checkProduct:
                    form.save()
     
     return redirect('insertProduct/')

def details(request):
     if request.method == 'GET':
          productId = request.GET['id']
          productData = Product.objects.filter(id = productId)
          data = productData[0]
          return render(request, 'products/details.html', { 'data': data})

def search(request):
     if request.method == 'GET':
          search = request.GET['search']
          
          catagory = Catagories.objects.filter(name = search)
          if catagory:
               catagoryId = catagory[0].id
          
          brand = Brands.objects.filter(name = search)
          if brand:
               brandId = brand[0].id
          
          if catagory:
               print("catagoryId")
               print(catagoryId)
               data = Product.objects.filter(catagoryId = catagoryId)
          elif brand:
               print("brandId")
               print(brandId)
               data = Product.objects.filter(brandId = brandId)
          else:
               data = Product.objects.filter(Q(name__contains = search) | Q(details__contains = search) | Q(price__contains = search))
          
          return render(request, 'products/products.html', { 'data': data})

#end Product

#user

def signup(request):
     if request.user.is_authenticated:
          messages.info(request, 'You are Logged in!!!')
          return redirect('/')
     else:
          if request.method == "POST":
               form = signupForm(request.POST)
               print('POST')
               if form.is_valid():
                    print('valid')
                    form.save()

                    admin = request.POST['admin']
                    name = request.POST['username']
                    
                    u = User.objects.filter(username = name)
                    userId = u[0]
                    customer = Customer(user = userId, admin = admin, name = name)
                    customer.save()

                    userName = request.POST['username']
                    userPassword = request.POST['password1']
                    print(userName)
                    print(userPassword)
                    
                    user = authenticate(username = userName, password = userPassword)
                    if user is not None:
                         print("Log In")
                         login(request, user)
                         return redirect('/')
                    else:
                         return redirect('/signin/')
               else:
                    messages.info(request, 'please enter valid information!!!')
                    return render(request, 'customer/signup.html', {'form': form})
          else:
               form = signupForm()
               return render(request, 'customer/signup.html', {'form': form})

def signin(request):
     if request.user.is_authenticated:
          messages.info(request, 'You are Logged in!!!')
          return redirect('/')
     else:
          if request.method == "POST":
               form = AuthenticationForm(request = request, data = request.POST)
               if form.is_valid():
                    print("Lvvvv")
                    userName = form.cleaned_data['username']
                    userPassword = form.cleaned_data['password']
                    user = authenticate(username = userName, password = userPassword)
                    if user is not None:
                         print("Log In")
                         login(request, user)
                         return redirect('/')
                    else:
                         messages.info(request, 'please enter valid information!!!')
               else:
                    messages.info(request, 'please enter valid information!!!')
          else:
               form = AuthenticationForm()
          return render(request, 'customer/signin.html', {'form': form})

def signout(request):
     if request.user.is_authenticated:
          djLogout(request)
          return redirect('/')
     else:
          messages.info(request, 'You are not Logged in. Please Log In and try again!!!')
          return redirect('/signin/')

def addToCart(request):
     if request.user.is_authenticated:
          productId = request.GET['productId']
          action = request.GET['action']
          print('Action:', action)
          print('Product:', productId)
          customer = request.user.customer
          product = Product.objects.get(id=productId)
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
          if action == 'add':
               orderItem.quantity = (orderItem.quantity + 1)
          # elif action == 'remove':
          #      orderItem.quantity = (orderItem.quantity - 1)
          orderItem.save()

          # if orderItem.quantity <= 0:
          #      orderItem.delete()

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer = customer, complete = False)
          items = order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0}

     context = {'items': items, 'order': order}
     return render(request, 'store/cart.html', context)
     # return render(request, 'store/cart.html')

def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer = customer, complete = False)
          items = order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0}
     
     customerId = request.user.customer
     orderId = Order.objects.get(customer=customer, complete=False)
     
     # form = ShippingAddressForm()
     context = {'items': items, 'order': order, 'customerId': customerId, 'orderId': orderId}
     return render(request, 'store/checkout.html', context)

def plusItem(request):
     if request.user.is_authenticated:
          productId = request.GET['productId']
          print('Product:', productId)
          customer = request.user.customer
          product = Product.objects.get(id=productId)
          order = Order.objects.get(customer=customer, complete=False)
          orderItem= OrderItem.objects.get(order=order, product=product)
          orderItem.quantity = (orderItem.quantity + 1)
          orderItem.save()
     return redirect('/cart/')

def minusItem(request):
     if request.user.is_authenticated:
          productId = request.GET['productId']
          print('Product:', productId)
          customer = request.user.customer
          product = Product.objects.get(id=productId)
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
          orderItem.quantity = (orderItem.quantity - 1)
          orderItem.save()
          if orderItem.quantity <= 0:
               orderItem.delete()
     return redirect('/cart/')

def checkoutUpload(request):
     if request.user.is_authenticated:
          print('.....checkoutUpload.....')
          if request.method == 'POST':
               address = request.POST['address']
               city = request.POST['city']
               state = request.POST['state']
               zipcode = request.POST['zipcode']
               customer = request.user.customer
               order = Order.objects.get(customer = customer, complete = False)
               shippingAddress, created = ShippingAddress.objects.get_or_create(customer = customer, order = order, address = address, city = city, state = state, zipcode = zipcode )
               
               order.complete = True
               order.save()
               print('.....checkoutUpload.....')

          
     return redirect('/')

def trackOrder (request):
     if request.method == 'GET':
          oId = request.GET['id']
          order = Order.objects.get(id = oId)
          items = order.orderitem_set.all()
          customer = request.user.customer
          shippingAddress = ShippingAddress.objects.get(order = order.id)
     # print(items[1].order)
     context = {'shippingAddress': shippingAddress, 'items': items}
     return render(request, 'customer/trackOrder.html', context)

def profile(request):
     customer = request.user.customer
     orders = Order.objects.filter(customer = customer, complete = True)
     # items = orders.orderitem_set.all()
     # items = []
     # for order in orders:
     #      # i = Order.objects.get(id = order.id)
     #      print(order.id)
     #      print(order.date_ordered)
     #      items = list(chain(items, Order.objects.all()))

     # orders = list( chain(orders, Order.objects.filter(customer = customer, complete = False)))
     
     catagories = Catagories.objects.all()
     brands = Brands.objects.all()
     products = Product.objects.all()
     
     context = {'orders': orders, 'catagories': catagories, 'brands': brands, 'products': products}
     return render(request, 'customer/profile.html', context)
     

#end user

###########################################################################

def index(request):
     catagories = Catagories.objects.all().order_by('?')[:4]
     brands = Brands.objects.all().order_by('?')[:4]
     products = Product.objects.all().order_by('?')[:8]
     
     # if request.user.is_authenticated:
     #      customer = request.user.customer
     #      order, created = Order.objects.get_or_create(customer = customer, complete = False)
     #      cartItems = order.get_cart_items
     # else:
     #      cartItems = 0
     
     context = { 'catagories':catagories, 'brands':brands, 'products':products, 'cartItems':cartItems }
     return render(request, 'store/index.html', context)

def cartItems(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer = customer, complete = False)
          cartItems = order.get_cart_items
     else:
          cartItems = 0
          
     return HttpResponse(cartItems)
     
########################################



##########################################################################