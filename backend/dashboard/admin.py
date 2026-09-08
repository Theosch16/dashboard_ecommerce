from django.contrib import admin
from .models import Localisation, Product, Customer, Order, OrderItem, OrderPayment, Seller

# Register your models here.

admin.site.register([Localisation, Product, Customer, Order, OrderItem, OrderPayment, Seller])