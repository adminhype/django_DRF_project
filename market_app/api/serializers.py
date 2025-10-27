from rest_framework import serializers
from market_app.models import Market, Seller


def validate_no_x(value):
    errors = []

    if 'X' in value:
        errors.append("Value cannot contain the letter 'X'.")
    if 'Y' in value:
        errors.append("Value cannot contain the letter 'Y'.")
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=15, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.net_worth = validated_data.get(
            'net_worth', instance.net_worth)
        instance.save()
        return instance

    # def validate_location(self, value):
    #     if 'X' in value:
    #         raise serializers.ValidationError(
    #             "Location cannot contain the character 'X'.")
    #     return value


class SellersDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    contact_info = serializers.CharField(max_length=100)
    # markets = MarketSerializer(read_only=True, many=True)
    markets = serializers.StringRelatedField(many=True)


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    contact_info = serializers.CharField(max_length=100)
    markets = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError(
                "One or more market IDs not found.")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller
