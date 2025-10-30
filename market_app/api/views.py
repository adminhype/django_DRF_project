from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, ProductSerializer, SellerSerializer, SellerListSerializer
from market_app.models import Market, Seller, Product
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics


class MarketsView(generics.ListCreateAPIView):

    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class SellerOfMarketListView(generics.ListCreateAPIView):
    serializer_class = SellerListSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        market = Market.objects.get(pk=pk)
        return market.sellers.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        market = Market.objects.get(pk=pk)
        serializer.save(markets=[market])


# class SellerOfMarketListView(generics.ListAPIView):
#     serializer_class = SellerListSerializer

#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         market = Market.objects.get(pk=pk)
#         return market.sellers.all()


class MarketDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SellerView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view()
def sellers_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def products_view(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, many=True, fields=['name', 'price'])
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view()
def products_single_view(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
