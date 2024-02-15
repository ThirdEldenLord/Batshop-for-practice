from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.proccess_order, name="process_order"),
]