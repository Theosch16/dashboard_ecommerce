from django.shortcuts import render
from django.db.models import Count, Avg
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Localisation, Product, Customer, Order, OrderItem, OrderPayment, Seller
from .serializers import LocalisationSerializer, ProductSerializer, CustomerSerializer, OrderSerializer,OrderItemSerializer,OrderPaymentSerializer, SellerSerializer

# Create your views here.
@api_view(['GET'])
def get_localisation(request):
    localisations=Localisation.objects.all()

    city = request.query_params.get("city")
    state = request.query_params.get("state")
    zip_code = request.query_params.get("zip_code")

    if city:
        localisations = localisations.filter(city=city)
    if state:
        localisations = localisations.filter(state=state)
    if zip_code:
        localisations = localisations.filter(zip_code=zip_code)

    serializer=LocalisationSerializer(localisations, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_orders(request):
    orders = Order.objects.all()

    order_status = request.query_params.get("status")

    if order_status:
        orders = orders.filter(order_status=order_status)

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_product(request):
    products = Product.objects.all()
    category = request.query_params.get("category")

    if category:
        products = products.filter(product_category_name=category)

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_order_status_stats(request):
    stats = (
        Order.objects
        .values("order_status")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)

@api_view(["GET"])
def get_category_stats(request):
    stats = (
        Product.objects
        .values("product_category_name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)

@api_view(["GET"])
def get_payment_type_stats(request):
    stats = (
        OrderPayment.objects
        .values("payment_type")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)


@api_view(["GET"])
def get_orders_city_stats(request):
    stats = (
        Order.objects
        .values("customer__localisation__city")
        .annotate(latitude=Avg("customer__localisation__latitude"),longitude=Avg("customer__localisation__longitude"),count=Count("id"))
    )

    return Response(stats)

@api_view(["GET"])
def get_orders_location(request):
    stats = (
        Order.objects
        .values(
            "customer__localisation__city",
            )
        .annotate(
            count=Count("id"),
            latitude=Avg("customer__localisation__latitude"),
            longitude=Avg("customer__localisation__longitude")
        )
    )
    data = []

    for order in stats:
        data.append({
            "city": order["customer__localisation__city"],
            "latitude": float(order["latitude"]),
            "longitude": float(order["longitude"]),
            "count": order["count"],
        })

    return Response(data)