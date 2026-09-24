from django.shortcuts import render
from django.db.models import Count, Avg
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import ExtractYear
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

    status=Order.objects.all()

    city = request.query_params.get("city")
    states = request.query_params.get("states")
    year = request.query_params.get("year")

    if city:
        status = status.filter(customer__localisation__city=city)
    if states:
        status = status.filter(customer__localisation__state=states)
    if year:
        status = status.filter(order_purchase_timestamp__year=year)


    stats = (
        status
        .values("order_status")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)

@api_view(["GET"])
def get_category_stats(request):

    category=OrderItem.objects.all()

    city = request.query_params.get("city")
    states = request.query_params.get("states")
    year = request.query_params.get("year")

    if city:
        category = category.filter(order__customer__localisation__city=city)
    if states:
        category = category.filter(order__customer__localisation__state=states)
    if year:
        category = category.filter(order__order_purchase_timestamp__year=year)

    stats = (
        category
        .values("product__product_category_name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)

@api_view(["GET"])
def get_payment_type_stats(request):
    payment=OrderPayment.objects.all()

    city = request.query_params.get("city")
    states = request.query_params.get("states")
    year = request.query_params.get("year")

    if city:
        payment = payment.filter(order__customer__localisation__city=city)
    if states:
        payment = payment.filter(order__customer__localisation__state=states)
    if year:
        payment = payment.filter(order__order_purchase_timestamp__year=year)

    stats = (
        payment
        .values("payment_type")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)


@api_view(["GET"])
def get_orders_city_stats(request):

    city_order=Order.objects.all()

    city = request.query_params.get("city")
    states = request.query_params.get("states")
    year = request.query_params.get("year")

    if city:
        city_order = city_order.filter(customer__localisation__city=city)
    if states:
        city_order = city_order.filter(customer__localisation__state=states)
    if year:
        city_order = city_order.filter(order_purchase_timestamp__year=year)


    stats = (
        city_order
        .values("customer__localisation__city")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return Response(stats)

@api_view(["GET"])
def get_orders_location(request):

    city_location=Order.objects.all()

    city = request.query_params.get("city")
    states = request.query_params.get("states")
    year = request.query_params.get("year")

    if city:
        city_location = city_location.filter(customer__localisation__city=city)
    if states:
        city_location = city_location.filter(customer__localisation__state=states)
    if year:
        city_location = city_location.filter(order_purchase_timestamp__year=year)

    stats = (
        city_location
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


@api_view(['GET'])
def get_filters(request):
    selected_state = request.query_params.get('state')

    years = (
        Order.objects
            .annotate(year=ExtractYear('order_purchase_timestamp'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
    )

    states = (
        Localisation.objects
            .values_list('state', flat=True)
            .distinct()
            .order_by('state')
    )

    cities_query = Localisation.objects.all()

    if selected_state:
        cities_query = cities_query.filter(state=selected_state)

    cities = (
        cities_query
            .values_list('city', flat=True)
            .distinct()
            .order_by('city')
    )

    return Response({
        'years':list(years),
        'states' :list(states),
        'cities' :list(cities)
    })