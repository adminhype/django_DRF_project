from rest_framework import routers
from django.urls import include, path
from .views import ProductViewSet, products_view, sellers_single_view, products_single_view, MarketsView, SellerView, MarketSingleView, SellerOfMarketListView

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/',
         SellerOfMarketListView.as_view(), name='market-sellers'),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', sellers_single_view, name='seller-detail'),
    # path('product/', products_view, name='products-view'),
    # path('product/<int:pk>/', products_single_view, name='products-single'),
]
