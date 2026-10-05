from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'books/',
        views.books,
        name='books'
    ),

    path(
        'book/<int:id>/',
        views.book_detail,
        name='book_detail'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'orders/',
        views.orders,
        name='orders'
    ),
]