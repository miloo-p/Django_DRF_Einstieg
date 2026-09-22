from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer
from market_app.models import Market, Seller


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
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)


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
        serialzier = SellerDetailSerializer(sellers, many=True)
        return Response(serialzier.data)
    if request.method == 'POST':
        serialzier = SellerCreateSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)
