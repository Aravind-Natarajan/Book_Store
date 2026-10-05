from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q

from .models import (
    Book,
    Category,
    CartItem,
    Order,
    OrderItem
)

from .forms import (
    RegisterForm,
    BookForm,
    CheckoutForm
)



def home(request):

    books = Book.objects.all().order_by('-created_at')[:8]

    categories = Category.objects.all()

    return render(
        request,
        'store/home.html',
        {
            'books': books,
            'categories': categories
        }
    )

def books(request):

    query = request.GET.get('q')

    category_id = request.GET.get('category')

    book_list = Book.objects.all()

    if query:

        book_list = book_list.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    if category_id:

        book_list = book_list.filter(
            category_id=category_id
        )

    categories = Category.objects.all()

    return render(
        request,
        'store/books.html',
        {
            'books': book_list,
            'categories': categories,
            'query': query
        }
    )

def book_detail(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    return render(
        request,
        'store/book_detail.html',
        {
            'book': book
        }
    )

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            login(request, user)

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'store/register.html',
        {
            'form': form
        }
    )
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'store/login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(
        request,
        'store/login.html'
    )

def user_logout(request):

    logout(request)

    return redirect('home')

@login_required
def add_to_cart(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    if book.stock <= 0:
        return redirect('book_detail', id=id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )

    if not created:

        if cart_item.quantity < book.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')

@login_required
def cart(request):

    items = CartItem.objects.filter(
        user=request.user
    )

    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        'store/cart.html',
        {
            'items': items,
            'total': total
        }
    )

@login_required
def remove_from_cart(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('cart')

@login_required
def checkout(request):

    items = CartItem.objects.filter(
        user=request.user
    )

    if not items.exists():

        return redirect('cart')

    total = sum(
        item.total_price()
        for item in items
    )

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user
            order.total_amount = total

            order.save()

            for item in items:

                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )

                item.book.stock -= item.quantity
                item.book.save()

            items.delete()

            return redirect('orders')

    else:

        form = CheckoutForm()

    return render(
        request,
        'store/checkout.html',
        {
            'form': form,
            'items': items,
            'total': total
        }
    )
@login_required
def orders(request):

    order_list = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/orders.html',
        {
            'orders': order_list
        }
    )