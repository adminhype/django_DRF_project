from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):
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


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(read_only=True, many=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), write_only=True, many=True, source='markets'
    )

    class Meta:
        model = Seller
        exclude = []


# class SellersDetailSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=100)
#     contact_info = serializers.CharField(max_length=100)
#     # markets = MarketSerializer(read_only=True, many=True)
#     markets = serializers.StringRelatedField(many=True)


# class SellerCreateSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     contact_info = serializers.CharField(max_length=100)
#     markets = serializers.ListField(
#         child=serializers.IntegerField(), write_only=True)

#     def validate_markets(self, value):
#         markets = Market.objects.filter(id__in=value)
#         if len(markets) != len(value):
#             raise serializers.ValidationError(
#                 "One or more market IDs not found.")
#         return value

#     def create(self, validated_data):
#         market_ids = validated_data.pop('markets')
#         seller = Seller.objects.create(**validated_data)
#         markets = Market.objects.filter(id__in=market_ids)
#         seller.markets.set(markets)
#         return seller


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    market = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get(
            'price', instance.price)
        instance.save()
        return instance


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    market_id = serializers.IntegerField(write_only=True)
    seller_id = serializers.IntegerField(write_only=True)

    def validate_market_id(self, value):
        try:
            Market.objects.get(id=value)
        except Market.DoesNotExist:
            raise serializers.ValidationError("Market ID not found.")
        return value

    def validate_seller_id(self, value):
        try:
            Seller.objects.get(id=value)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Seller ID not found.")
        return value

    def create(self, validated_data):
        market = Market.objects.get(id=validated_data.pop('market_id'))
        seller = Seller.objects.get(id=validated_data.pop('seller_id'))
        product = Product.objects.create(
            market=market, seller=seller, **validated_data)
        return product
