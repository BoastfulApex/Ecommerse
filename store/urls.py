from django.urls import path
from .views import *

urlpatterns = [
    path('login/', log_in, name="login"),
    path('register/', user, name="register"),
    path('logout/', userLogout, name="logout"),


    path('store/', store, name="store"),
    path('cart/', card, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),

]
