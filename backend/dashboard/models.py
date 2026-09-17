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
    localisation=models.ForeignKey(Localisation, on_delete=models.PROTECT)
    customer_name= models.CharField(max_length=32)
    customer_unique_id=models.CharField(max_length=32, null=False)

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_name=models.CharField(max_length=32)
    order_purchase_timestamp = models.DateTimeField()
    order_review = models.IntegerField(null=True)
    order_delivered_carrier_date=models.DateTimeField(null=True)
    order_estimated_delivery_date=models.DateField()
    order_delivered_customer_date=models.DateTimeField(null=True)
    order_status=models.CharField(max_length=32)

class Seller(models.Model):
    localisation=models.ForeignKey(Localisation, on_delete=models.PROTECT)
    seller_name=models.CharField(max_length=32)

class OrderPayment(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=12)
    payment_installments=models.IntegerField()
    payment_value= models.DecimalField(max_digits=9, decimal_places=2)
    payment_sequential=models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(payment_installments__gte=0),
                name="payment_installments_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(payment_value__gte=0),
                name="payment_value_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(payment_sequential__gte=1),
                name="payment_sequential_positive",
            ),
        ]

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_name=models.CharField(max_length=32)
    price=models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="order_item_price_positive",
            ),
        ]