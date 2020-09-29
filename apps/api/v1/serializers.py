from rest_framework import serializers

from apps.core.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    # bonus = serializers.IntegerField(read_only=True)
    discount = serializers.FloatField(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('bonus',)

    def validate_discount(self, value):

        return value


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.get_absolute_url')
    link = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'category', 'description', 'image', 'price',
            'actual_price', 'link', 'discount'
        )
