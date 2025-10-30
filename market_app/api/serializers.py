from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.StringRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Market
        exclude = []

        def validate_name(self, value):
            errors = []

            if 'X' in value:
                errors.append("Value cannot contain the letter 'X'.")
            if 'Y' in value:
                errors.append("Value cannot contain the letter 'Y'.")
            if errors:
                raise serializers.ValidationError(errors)
            return value


class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):

    # sellers = None

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Market
        fields = ['id', 'url', 'name', 'location', 'description', 'net_worth']


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(read_only=True, many=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), write_only=True, many=True, source='markets'
    )

    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'market_ids',
                  'market_count', 'markets', 'contact_info']

    def get_market_count(self, obj):
        return obj.markets.count()


class ProductSerializer(serializers.ModelSerializer):
    market = MarketSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    market_id = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), write_only=True, source='market'
    )

    class Meta:
        model = Product
        fields = ['market', 'market_id', 'seller',
                  'name', 'description', 'price',]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


# class ProductCreateSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     market_id = serializers.IntegerField(write_only=True)
#     seller_id = serializers.IntegerField(write_only=True)

#     def validate_market_id(self, value):
#         try:
#             Market.objects.get(id=value)
#         except Market.DoesNotExist:
#             raise serializers.ValidationError("Market ID not found.")
#         return value

#     def validate_seller_id(self, value):
#         try:
#             Seller.objects.get(id=value)
#         except Seller.DoesNotExist:
#             raise serializers.ValidationError("Seller ID not found.")
#         return value

#     def create(self, validated_data):
#         market = Market.objects.get(id=validated_data.pop('market_id'))
#         seller = Seller.objects.get(id=validated_data.pop('seller_id'))
#         product = Product.objects.create(
#             market=market, seller=seller, **validated_data)
#         return product
