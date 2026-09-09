from django.db import models

# Create your models here.

class Localisation(models.Model):
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)

class Product(models.Model):
    product_name= models.CharField(max_length=32)
    product_category_name= models.CharField(max_length=40, null=True, blank=True)

class Customer(models.Model):
    localisation=models.ForeignKey(Localisation, on_delete=models.CASCADE)
    customer_name= models.CharField(max_length=32)
    customer_unique_id=models.CharField(max_length=32, null=False)

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_name=models.CharField(max_length=32)
    order_purchase_timestamp = models.DateField()
    order_review = models.IntegerField(null=True)
    order_delivered_carrier_date=models.DateField()
    order_estimated_delivery_date=models.DateField()
    order_delivered_customer_date=models.DateField()
    order_status=models.CharField(max_length=32)

class Seller(models.Model):
    localisation=models.ForeignKey(Localisation, on_delete=models.CASCADE)
    seller_name=models.CharField(max_length=32)

class OrderPayment(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=12)
    payment_installments=models.IntegerField()
    payment_value= models.DecimalField(max_digits=9, decimal_places=2)
    payment_sequential=models.IntegerField()

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_name=models.CharField(max_length=32)
    price=models.DecimalField(max_digits=9, decimal_places=2)