from django.urls import path
from .views import get_localisation, get_orders, get_product, get_order_status_stats, get_category_stats, get_payment_type_stats, get_orders_city_stats, get_orders_location
urlpatterns = [
    path("localisations/", get_localisation, name='get_localisation'),
    path("orders/", get_orders, name='get_orders'),
    path("products/", get_product, name='get_products'),
    path("stats_orders/", get_order_status_stats, name='get_order_status_stats'),
    path("stats_categories/", get_category_stats, name='get_category_stats'),
    path("stats_payment_type/", get_payment_type_stats, name='get_payment_type_stats'),
    path("stats_order_city/", get_orders_city_stats, name='get_orders_city_stats'),
    path("stats_order_city/", get_orders_city_stats, name='get_orders_city_stats'),
    path("stats_order_locations/", get_orders_location, name='get_orders_location')
]