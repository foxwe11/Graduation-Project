from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *

class UserAPIList(generics.ListCreateAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """Редактирование пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginAPI(APIView):
    """Авторизация"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.all()
        get_user = data["login"]
        get_password = data["password"]

        for us in user:
            if get_user == us.login and get_password == us.password:
                serializer = UserLoginSerializer(us)
                return Response(serializer.data)

        return Response("Пользователь не найден")


# ------------------------------------------------------------------
class ProductAPIList(APIView):
    """Список продуктов"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        prod = Product()

        try:
            prod.product_name = data["product_name"]
            prod.currency = data["currency"]
            prod.output_volume = data["output_volume"]
            prod.period = data["period"]
            prod.sale_price = data["sale_price"]
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            user = User.objects.get(id=data["user_id"])
            user.product_set.add(prod, bulk=False)
        except:
            return Response("Не удалось создать запись")
        serializer = ProductSerializer(prod)
        return Response(serializer.data)


class ProductAPIDetail(APIView):
    """Список продуктов"""
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        prod = self.get_object(pk)
        data = request.data
        try:
            prod.product_name = data["product_name"]
            prod.currency = data["currency"]
            prod.output_volume = data["output_volume"]
            prod.period = data["period"]
            prod.sale_price = data["sale_price"]
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            user = User.objects.get(id=data["user_id"])
            prod.user_id = user
        except:
            return Response("Не удалось изменить запись")
        prod.save()
        serializer = ProductSerializer(prod)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        prod = self.get_object(pk)
        prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductCalculationAPIList(APIView):
    """Проведение расчётов продукции"""
    serializer_class = ProductCalculationSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            Response("Error http404")

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        data = request.data
        prod = Product.objects.get(id = pk)
        try:
            prod.output_volume = data["output_volume"]
            prod.period = data["period"]
            prod.sale_price = data["sale_price"]
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
        except:
            return Response("Не удалось рассчиать")
        serializer = ProductCalculationSerializer(prod)
        return Response(serializer.data)
# ------------------------------------------------------------------

class MaterialAPIList(APIView):
    """Список материальных затрат"""
    serializer_class = MaterialSerializer

    def get_queryset(self):
        materials = Material_costs.objects.all()
        return materials

    def get(self, request, *args, **kwargs):
        materials = self.get_queryset()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        mat = Material_costs()
        try:
            mat.material_name = data["material_name"]
            mat.count = data["count"]
            mat.cost = data["cost"]
            mat.total_price = mat.price()
            prod = Product.objects.get(id=data["product_id"])
            # prod.material_costs_set.add(mat, bulk=False)
            mat.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            mat.save()
            prod.save()
        except:
            return Response("Не удалось создать запись")
        serializer = MaterialSerializer(mat)
        return Response(serializer.data)


class MaterialAPIDetail(APIView):
    """Список материальных затрат"""
    serializer_class = MaterialSerializer

    def get_object(self, pk):
        try:
            return Material_costs.objects.get(pk=pk)
        except Material_costs.DoesNotExist:
            Response("Error http404")

    def get(self, request, pk, format=None):
        mat = self.get_object(pk)
        serializer = MaterialSerializer(mat)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mat = self.get_object(pk)
        data = request.data
        try:
            mat.material_name = data["material_name"]
            mat.count = data["count"]
            mat.cost = data["cost"]
            mat.total_price = mat.price()
            prod = Product.objects.get(id=data["product_id"])
            mat.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
        except:
            return Response("Не удалось изменить запись")
        mat.save()
        prod.save()
        serializer = MaterialSerializer(mat)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        mat = self.get_object(pk)
        mat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ------------------------------------------------------------------

class LaborAPIList(APIView):
    """Список трудозатрат"""
    serializer_class = LaborSerializer

    def get_queryset(self):
        labor = Labor_costs.objects.all()
        return labor

    def get(self, request, *args, **kwargs):
        labors = self.get_queryset()
        serializer = LaborSerializer(labors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        lab = Labor_costs()
        try:
            lab.profession = data["profession"]
            lab.number_of_people = data["number_of_people"]
            lab.salary = data["salary"]
            lab.deduction = data["deduction"]
            lab.total_price = lab.price(data["product_id"])
            prod = Product.objects.get(id=data["product_id"])
            # prod.labor_costs_set.add(lab, bulk=False)
            lab.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            lab.save()
            prod.save()
        except:
            return Response("Не удалось создать запись")
        serializer = LaborSerializer(lab)
        return Response(serializer.data)


class LaborAPIDetail(APIView):
    """Список трудозатрат"""
    serializer_class = LaborSerializer

    def get_object(self, pk):
        try:
            return Labor_costs.objects.get(pk=pk)
        except Labor_costs.DoesNotExist:
            Response("Error http404")

    def get(self, request, pk, format=None):
        lab = self.get_object(pk)
        serializer = LaborSerializer(lab)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        lab = self.get_object(pk)
        data = request.data

        # lab.profession = data["profession"]
        # lab.number_of_people = data["number_of_people"]
        # lab.salary = data["salary"]
        # lab.deduction = data["deduction"]
        # lab.total_price = lab.price(data["product_id"])
        # prod = Product.objects.get(id=data["product_id"])
        # lab.product_id = prod
        # prod.cost_price = prod.price()
        # prod.return_on_sales = prod.sale()
        # prod.breakeven_point = prod.breakeven()
        try:
            lab.profession = data["profession"]
            lab.number_of_people = data["number_of_people"]
            lab.salary = data["salary"]
            lab.deduction = data["deduction"]
            lab.total_price = lab.price(data["product_id"])
            prod = Product.objects.get(id=data["product_id"])
            lab.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
        except:
            return Response("Не удалось изменить запись")
        prod.save()
        lab.save()
        serializer = LaborSerializer(lab)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        lab = self.get_object(pk)
        lab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ------------------------------------------------------------------

class AmortizationAPIList(APIView):
    """Список амортизационных затрат"""
    serializer_class = AmortizationSerializer

    def get_queryset(self):
        amort = Amortization_costs.objects.all()
        return amort

    def get(self, request, *args, **kwargs):
        amort = self.get_queryset()
        serializer = AmortizationSerializer(amort, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        amort = Amortization_costs()
        try:
            amort.equipment_name = data["equipment_name"]
            amort.count_equipment = data["count_equipment"]
            amort.cost = data["cost"]
            amort.service_life = data["service_life"]
            amort.total_price = amort.price(data["product_id"])
            prod = Product.objects.get(id=data["product_id"])
            # prod.amortization_costs_set.add(amort, bulk=False)
            amort.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            amort.save()
            prod.save()
        except:
            return Response("Не удалось создать запись")
        serializer = AmortizationSerializer(amort)
        return Response(serializer.data)


class AmortizationAPIDetail(APIView):
    """Список амортизационных затрат"""
    serializer_class = AmortizationSerializer

    def get_object(self, pk):
        try:
            return Amortization_costs.objects.get(pk=pk)
        except Amortization_costs.DoesNotExist:
            Response("Error http404")

    def get(self, request, pk, format=None):
        amort = self.get_object(pk)
        serializer = AmortizationSerializer(amort)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        amort = self.get_object(pk)
        data = request.data
        try:
            amort.equipment_name = data["equipment_name"]
            amort.count_equipment = data["count_equipment"]
            amort.cost = data["cost"]
            amort.service_life = data["service_life"]
            amort.total_price = amort.price(data["product_id"])
            prod = Product.objects.get(id=data["product_id"])
            amort.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
        except:
            return Response("Не удалось изменить запись")
        amort.save()
        prod.save()
        serializer = AmortizationSerializer(amort)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        amort = self.get_object(pk)
        amort.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ------------------------------------------------------------------

class InvoiceAPIList(APIView):
    """Список накладных расходов"""
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        invoice = Invoice_costs.objects.all()
        return invoice

    def get(self, request, *args, **kwargs):
        invoice = self.get_queryset()
        serializer = InvoiceSerializer(invoice, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        inv = Invoice_costs()
        try:
            inv.invoice_name = data["invoice_name"]
            inv.count = data["count"]
            inv.cost = data["cost"]
            inv.total_price = inv.price()
            prod = Product.objects.get(id=data["product_id"])
            # prod.invoice_costs_set.add(inv, bulk=False)
            inv.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
            inv.save()
            prod.save()
        except:
            return Response("Не удалось создать запись")
        serializer = InvoiceSerializer(inv)
        return Response(serializer.data)


class InvoiceAPIDetail(APIView):
    """Список накладных расходов"""
    serializer_class = InvoiceSerializer

    def get_object(self, pk):
        try:
            return Invoice_costs.objects.get(pk=pk)
        except Invoice_costs.DoesNotExist:
            Response("Error http404")

    def get(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        inv = self.get_object(pk)
        data = request.data
        try:
            inv.invoice_name = data["invoice_name"]
            inv.count = data["count"]
            inv.cost = data["cost"]
            inv.total_price = inv.price()
            prod = Product.objects.get(id=data["product_id"])
            inv.product_id = prod
            prod.cost_price = prod.price()
            prod.return_on_sales = prod.sale()
            prod.breakeven_point = prod.breakeven()
        except:
            return Response("Не удалось изменить запись")
        inv.save()
        prod.save()
        serializer = InvoiceSerializer(inv)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        inv = self.get_object(pk)
        inv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ------------------------------------------------------------------