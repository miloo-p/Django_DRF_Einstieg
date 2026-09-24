from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, ProductDetailSerializer, ProductCreateSerializer, SellerSerializer
from market_app.models import Market, Seller, Product


@api_view(['GET', 'POST'])
def markets_view(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        serialzier = MarketSerializer(markets, many=True)
        return Response(serialzier.data)
    if request.method == 'POST':
        serialzier = MarketSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):
    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serialzier = MarketSerializer(market)
        return Response(serialzier.data)

    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serialzier = MarketSerializer(market, data=request.data, partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)

    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serialzier = MarketSerializer(market)
        market.delete()
        return Response(serialzier.data)


@api_view(['GET', 'POST'])
def sellers_view(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serialzier = SellerSerializer(sellers, many=True)
        return Response(serialzier.data)
    if request.method == 'POST':
        serialzier = SellerSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def seller_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serialzier = SellerSerializer(seller)
        return Response(serialzier.data)

    if request.method == 'PUT':
        seller = Seller.objects.get(pk=pk)
        serialzier = SellerSerializer(seller, data=request.data, partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)

    if request.method == 'DELETE':
        seller = Seller.objects.get(pk=pk)
        serialzier = SellerSerializer(seller)
        seller.delete()
        return Response(serialzier.data)


@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serialzier = ProductDetailSerializer(products, many=True)
        return Response(serialzier.data)
    if request.method == 'POST':
        serialzier = ProductCreateSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def product_single_view(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serialzier = ProductDetailSerializer(product)
        return Response(serialzier.data)

    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serialzier = ProductCreateSerializer(
            product, data=request.data, partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)

    if request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        serialzier = ProductDetailSerializer(product)
        product.delete()
        return Response(serialzier.data)
