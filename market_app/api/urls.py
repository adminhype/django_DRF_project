from django.urls import path
from .views import market_view, market_single_view, sellers_view, products_view

urlpatterns = [
    path('market/', market_view, name='market-view'),
    path('market/<int:pk>/', market_single_view, name='market-single-view'),
    path('seller/', sellers_view, name='seller-view'),
    path('product/', products_view, name='products-view'),
]
