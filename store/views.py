from django.shortcuts import render,get_object_or_404,redirect 
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json
from django.contrib import messages
import datetime
from .utils import cookieCart, cartData ,guestOrder
from django.conf import settings
from django.contrib.auth import authenticate , login ,logout

# Create your views here.

def store(request):
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  products = Product.objects.all()
  context = {'products':products, 'cartItems':cartItems}
  return render(request, 'store/store.html', context)

def productDetail(request, id):
	data = cartData(request)

	cartItems = data['cartItems']
	product = get_object_or_404(Product, pk=id)
	data={
		'product':product,
		'cartItems':cartItems
	}
	return render(request, 'store/productDetail.html', data)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems,}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)


	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create( complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddresss.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def SignupPage(request):
	data = cartData(request)
	if request.method =='POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		confirm_password = request.POST.get('confirm_password')

		if password1 != confirm_password:
			return HttpResponse("Your password and Confirm password are not same!!")
		else:
			my_user = User.objects.create_user(username, email, password1)
			my_user.save()
			return redirect('login')


	cartItems = data['cartItems']
	context = { 'cartItems':cartItems}
	return render(request, 'store/signup.html',context)

def LoginPage(request):
	data = cartData(request)
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('store')
		else:
			return HttpResponse("Username or Password incorrect!!")


	cartItems = data['cartItems']
	context = { 'cartItems':cartItems}
	return render(request, 'store/login.html',context)

def LogoutPage(request):
	logout(request)
	return redirect('login')

def AboutusPage(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems,}
	return render(request, 'store/About.html', context) 

def ServicesPage(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems,}
	return render(request, 'store/Services.html', context) 

def ContactPage(request):
	data = cartData(request)
	if request.method =='POST':
		name = request.POST.get('name_c')
		email = request.POST.get('email')
		message = request.POST.get('message')

		contact = Contactus(name=name, email=email, message=message)
		contact.save()
		messages.success(request, 'Your message send successfully!!')
		return redirect('store')
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems,}
	return render(request, 'store/Contact.html', context) 

def search(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	if request.method == "POST":
		searched1 = request.POST['search_data']

		searched = Product.objects.filter(name__icontains=searched1)
		context = {'items':items, 'order':order, 'cartItems':cartItems,'searched':searched}
		return render(request,"store/search.html",context)
	else:
		return render(request,"store/search.html",{})


