from rest_framework import serializers
from market_app.models import Market, Seller

# CUSTOM VALIDATE OUTSIDE A CLASS - WITH SINGLE CHECK
# def validate_no_x(value):
#     if 'X' in value:
#         raise serializers.ValidationError('no X in location, please')
#     return value


# CUSTOM VALIDATE OUTSIDE A CLASS - WITH MORE CHECKS
def validate_no_x(value):
    errors = []
    if 'X' in value:
        raise errors.append('no X in location, please')
    if 'Z' in value:
        raise errors.append('no Z in location, please')
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(
        # IF CUSTOM VALIDATION OUTSIDE CLASS ADD HERE WITH validators=[name of def]
        max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

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

    # CUSTOM VALIDATE INSIDE A CLASS
    # def validate_location(value):
    #     if 'X' in value:
    #         raise serializers.ValidationError('no X in location, please')
    #     return value


class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(
        many=True)  # USE __str__ OF THE VIEW AS VALUE


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError(
                "One or more MarketIDs not found!")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller
