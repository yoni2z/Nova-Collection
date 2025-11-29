# shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from .models import Order, Cart, UserProfile
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login

def home(request):
    return render(request, 'home.html')

def glass(request):
    return render(request, 'glass.html')

def order_now(request):
    return render(request, 'order_now.html')


def electronics(request):
    category = get_object_or_404(Category, name='Electronics')
    products = Product.objects.filter(category=category)
    return render(request, 'electronics.html', {'products': products})

def cosmetics_view(request):
    category = Category.objects.get(name='Cosmetics')
    products = Product.objects.filter(category=category)
    return render(request, 'cosmetics.html', {'products': products, 'category': category})

def household(request):
    category = Category.objects.get(name='Household')
    products = Product.objects.filter(category=category)
    return render(request, 'household.html', {'products': products, 'category': category})

def sports(request):
    category = Category.objects.get(name='Sports')
    products = Product.objects.filter(category=category)
    return render(request, 'sports.html', {'products': products, 'category': category})

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_items_total': total_price
    }
    return render(request, 'cart.html', context)



def login_view(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    return render(request, 'logout.html')


from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# shop/views.py

def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    print(products)  # Debugging: Print the products retrieved
    return render(request, f'{category_name.lower()}.html', {'category': category, 'products': products})



# shop/views.py

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Get all cart items
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')



@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'user_profile': user_profile, 'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_items = order.cart.items.all()
    return render(request, 'order_detail.html', {'order': order, 'cart_items': cart_items})


# shop/views.py (add this logic where appropriate, e.g., in a checkout view)

from django.utils import timezone

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(
        user=request.user,
        cart=cart,
        total_price=sum(item.total_price() for item in cart.items.all()),
        created_at=timezone.now(),
        status='Pending'
    )
    # Clear the cart or handle further logic
    cart.items.all().delete()  # Optional: Clear the cart items after order
    return redirect('order_detail', order_id=order.id)
