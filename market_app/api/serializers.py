from rest_framework import serializers
from market_app.models import Market, Seller, Product

# CUSTOM VALIDATE OUTSIDE A CLASS - WITH SINGLE CHECK
# def validate_no_x(value):
#     if 'X' in value:
#         raise serializers.ValidationError('no X in location, please')
#     return value


# CUSTOM VALIDATE OUTSIDE A CLASS - WITH MORE CHECKS
def validate_no_x(value):
    errors = []
    if 'X' in value:
        errors.append('no X in location, please')
    if 'Z' in value:
        errors.append('no Z in location, please')
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        exclude = []

    # CUSTOM VALIDATE INSIDE A CLASS
    # def validate_location(value):
    #     if 'X' in value:
    #         raise serializers.ValidationError('no X in location, please')
    #     return value


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(),
                                                    many=True,
                                                    write_only=True,
                                                    source="markets")

    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["id", "name", "market_ids",
                  "market_count", "markets", "contact_info"]

    def get_market_count(self, obj):
        return obj.markets.count()


class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.market_id = validated_data.get(
            'market_id', instance.market_id)
        instance.seller_id = validated_data.get(
            'seller_id', instance.seller_id)

        instance.save()
        return instance
