from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import uuid
def detailOrder(request):
    if request.user.is_authenticated:
        customer = request.user
        id = request.GET.get('id','')
        orderNotSold, created = Order.objects.get_or_create(customer =customer, complete = False)
        order, created = Order.objects.get_or_create(customer =customer, id = id)
        items = order.orderitem_set.all()
        cartItems = orderNotSold.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    context = {'items':items, 'order' :order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/detailOrder.html', context)
def history(request):
    if request.user.is_authenticated:
        customer = request.user
        orderNotSold, created = Order.objects.get_or_create(customer =customer, complete = False)
        orders = Order.objects.filter(customer=customer, complete=True).order_by('-id')
        all_items = []
        for order in orders:
            items = order.shippingaddress_set.all()
            all_items.extend(items)
        cartItems = orderNotSold.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
        return redirect("login")
    categories = Category.objects.filter(is_sub = False)

    context = {'categories': categories,'cartItems':cartItems,'items':all_items, 'orders' :orders,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/history.html', context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id= id)
    categories = Category.objects.filter(is_sub = False)

    context = {'products':products,'categories': categories,'items':items, 'order' :order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/detail.html', context)

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category_slug = request.GET.get('category', '')
    active_category = get_object_or_404(Category, slug=active_category_slug) if active_category_slug else None
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    if active_category:
        products = Product.objects.filter(category=active_category)
    else:
        products = Product.objects.all()

    context = {'categories': categories, 'products': products, 'active_category': active_category,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/category.html', context)
def search(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub = False)

    products = Product.objects.all()

    if request.method =="POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__icontains=searched)
    return render(request, 'app/search.html' ,{"searched": searched, "keys":keys,'products':products, 'cartItems':cartItems, 'user_not_login':user_not_login,'user_login':user_login,'categories': categories,})
def register(request):
    form = CreateUserForm()
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else: messages.info(request,'The username is overlapped, please re-enter!')


    user_not_login = "show"
    user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)

    context ={'categories': categories,'form': form, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None :
            login(request, user)
            return redirect('home')
        else: messages.info(request,'user or password not correct')
    categories = Category.objects.filter(is_sub = False)
    user_not_login = "show"
    user_login = "hidden"

    context ={'categories': categories,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/login.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
        return redirect("login")
    # Trong hàm checkout
    if request.method == "POST":
        # Lấy dữ liệu từ request.POST
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        # Kiểm tra xem đơn hàng đã tồn tại chưa
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        if not created:
            # Nếu đơn hàng đã tồn tại, cập nhật thông tin đơn hàng
            order.transaction_id = str(uuid.uuid4())
            order.save()

            # Tạo ShippingAddress mới
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address,
                mobile=mobile
            )

            # Cập nhật trạng thái đơn hàng
            order.complete = True
            order.save()
            return redirect('history')
        else:
            # Đơn hàng chưa tồn tại, xử lý như bình thường
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address,
                mobile=mobile
            )
            # Cập nhật trạng thái đơn hàng và transaction_id
            order.complete = True
            order.transaction_id = str(uuid.uuid4())
            order.save()

            return redirect('history')
    categories = Category.objects.filter(is_sub=False)

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'app/checkout.html', context)

def logoutPage (request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    context = {'categories': categories,'products':products, 'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
        return redirect("login")
    categories = Category.objects.filter(is_sub = False)

    context = {'categories': categories,'items':items, 'order' :order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/cart.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer =customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order =order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
