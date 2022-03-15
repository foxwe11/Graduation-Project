from rest_framework import serializers

from appRevyakoES.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['cost_price']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material_costs
        fields = "__all__"
        read_only_fields = ['total_price']

class LaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labor_costs
        fields = "__all__"
        read_only_fields = ['total_price']

class AmortizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amortization_costs
        fields = "__all__"
        read_only_fields = ['total_price']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_costs
        fields = "__all__"
        read_only_fields = ['total_price']

# class MaterialSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = Material_costs
#         fields = ("product_id", "material_name", "count", "cost")