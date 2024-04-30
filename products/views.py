from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from .models import Product
from rest_framework.response import Response
from django.core.cache import cache

@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"
    if not cache.get(cache_key):
        print("cache miss")
        products=Product.objects.all()
        serialzer=ProductSerializer(products, many=True)
        json_data=serialzer.data
        cache.set(cache_key, json_data,180)
    response_data=cache.get(cache_key)
    return Response(response_data)