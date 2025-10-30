from django.urls import path
from .views import market_single_view, products_view, sellers_single_view, products_single_view, MarketsView, SellerView

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', market_single_view, name='market-detail'),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', sellers_single_view, name='seller-single-view'),
    path('product/', products_view, name='products-view'),
    path('product/<int:pk>/', products_single_view, name='products-single-view'),
]
