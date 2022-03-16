from rest_framework import serializers

from appRevyakoES.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


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

class ProductSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many = True)
    labors = LaborSerializer(many = True)
    amortizations = AmortizationSerializer(many = True)
    invoices = InvoiceSerializer(many = True)
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['cost_price', 'return_on_sales', 'breakeven_point']



class ProductCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id', 'product_name', 'currency', 'cost_price',
                            'return_on_sales', 'breakeven_point', 'user_id']

# class CalculationSerializer(serializers.ModelSerializer):
#   sale_price = serializers.SerializerMethodField('sale')
#
#   def sale(self):
#       return 1
#
#   class Meta:
#     model = Product
#
#     fields = ('id', 'product_name', 'cost_price', 'currency', 'output_volume',
#               'period', 'sale_price')

# class MaterialSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = Material_costs
#         fields = ("product_id", "material_name", "count", "cost")