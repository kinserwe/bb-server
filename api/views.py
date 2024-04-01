from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product
from api.serializers import ProductSerializer


class ProductsView(APIView):
    def get(self, request):
        search_query = request.query_params.get("search")
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
