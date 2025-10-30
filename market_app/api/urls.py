from django.urls import path
from .views import products_view, sellers_single_view, products_single_view, MarketsView, SellerView, MarketDetailView

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', sellers_single_view, name='seller-single'),
    path('product/', products_view, name='products-view'),
    path('product/<int:pk>/', products_single_view, name='products-single'),
]
