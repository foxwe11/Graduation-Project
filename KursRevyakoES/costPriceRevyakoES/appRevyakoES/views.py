from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

from .models import User ,Product, Material_costs, Labor_costs, Amortization_costs, Invoice_costs

# Create your views here.



def calc(request, id):
    if request.method == "POST":
        us = User.objects.get(id=id)

        try:
            prod = Product.objects.get(product_name = request.POST.get("name_product"))
            if prod:
                prod.delete()
        except:
            pass

        product = Product()
        product.product_name = request.POST.get("name_product")
        product.cost_price = request.POST.get("cost_price")
        product.currency = request.POST.get("currency")
        product.output_volume = request.POST.get("value_all")
        product.period = request.POST.get("value_days")
        us.product_set.add(product, bulk=False)


        mas = request.POST.get("materials")
        if (mas != ''):
            result = list(map(int, mas.split(' ')))
            for i in result:
                mat = Material_costs()
                try:
                    mat.material_name = request.POST.get("material_name[{}]".format(i))
                    mat.count = request.POST.get("count[{}]".format(i))
                    mat.cost = request.POST.get("cost[{}]".format(i))
                    mat.total_price = float(mat.count)*float(mat.cost)
                    product.material_costs_set.add(mat, bulk=False)
                except:
                    continue


        mas = request.POST.get("labors")
        if(mas != ''):
            result = list(map(int, mas.split(' ')))
            for i in result:
                lab = Labor_costs()
                try:
                    lab.profession = request.POST.get("profession[{}]".format(i))
                    lab.number_of_people = request.POST.get("number_of_people[{}]".format(i))
                    lab.salary = request.POST.get("salary[{}]".format(i))
                    lab.deduction = request.POST.get("deduction[{}]".format(i))
                    lab.total_price = float(lab.number_of_people)*(float(lab.salary)+float(lab.salary)*float(lab.deduction)/100)/30*float(product.period)
                    product.labor_costs_set.add(lab, bulk=False)
                except:
                    continue


        mas = request.POST.get("amortizations")
        if (mas != ''):
            result = list(map(int, mas.split(' ')))
            for i in result:
                am = Amortization_costs()
                try:
                    am.equipment_name = request.POST.get("equipment_name[{}]".format(i))
                    am.count_equipment = request.POST.get("count_equipment[{}]".format(i))
                    am.cost = request.POST.get("cost[{}]".format(i))
                    am.service_life = request.POST.get("service_life[{}]".format(i))
                    am.total_price = float(am.count_equipment)*float(am.cost)*((100/float(am.service_life))/100*float(product.period)/365)
                    product.amortization_costs_set.add(am, bulk=False)
                except:
                    continue


        mas = request.POST.get("invoices")
        if (mas != ''):
            result = list(map(int, mas.split(' ')))
            for i in result:
                inv = Invoice_costs()
                try:
                    inv.invoice_name = request.POST.get("invoice_name[{}]".format(i))
                    inv.count = request.POST.get("count[{}]".format(i))
                    inv.cost = request.POST.get("cost[{}]".format(i))
                    inv.total_price = float(inv.count)*float(inv.cost)
                    product.invoice_costs_set.add(inv, bulk=False)
                except:
                    continue


    return render(request, "calc.html", {"user_id": id})


def prod(request, id):
    product = Product.objects.filter(user_id = id)
    mat = Material_costs.objects.all()
    lab = Labor_costs.objects.all()
    am = Amortization_costs.objects.all()
    inv = Invoice_costs.objects.all()
    data = {"product": product, "mat": mat, "lab": lab, "am": am, "inv": inv, "user_id": id}
    return render(request, "products.html", data)


def auth(request):
    if request.method == "POST":
        user = User.objects.all()
        get_user = request.POST.get("username")
        get_password = request.POST.get("password")

        for us in user:
            if get_user == us.login and get_password == us.password:
                return HttpResponseRedirect("/user/{}/calc/".format(us.id))
                # return calc(us.id)

        data = {"login": get_user, "password": get_password}
        messages.error(request, 'Неверный логин или пароль!')
        return render(request, "auth.html", data)

    return render(request, "auth.html")


def reg(request):
    if request.method == "POST":
        user = User.objects.all()
        get_user = request.POST.get("username")
        get_password = request.POST.get("password")

        for us in user:
            if get_user == us.login:
                data = {"login": get_user, "password": get_password}
                messages.error(request, 'Пользователь с таким логином уже существует!')
                return render(request, "reg.html", data)

        new_user = User.objects.create(login=get_user, password=get_password)
        return HttpResponseRedirect("/user/{}/calc/".format(new_user.id))
    return render(request, "reg.html")


def delete(request, id, prod_id):
    try:
        product = Product.objects.get(id=prod_id)
        product.delete()
    except Product.DoesNotExist:
        pass
    return prod(request, id)


def load(request, id, prod_id):
    mat1=""
    lab1=""
    am1=""
    inv1=""

    product = Product.objects.filter(id=prod_id)
    mat = Material_costs.objects.filter(product_id_id = prod_id)
    lab = Labor_costs.objects.filter(product_id_id = prod_id)
    am = Amortization_costs.objects.filter(product_id_id = prod_id)
    inv = Invoice_costs.objects.filter(product_id_id = prod_id)

    for m in mat:
        if(mat1 == ""):
            mat1=mat1 + "10" + str(m.id)
        else:
            mat1=mat1 + " 10" + str(m.id)

    for l in lab:
        if(lab1 == ""):
            lab1=lab1 + "20" + str(l.id)
        else:
            lab1=lab1 + " 20" + str(l.id)

    for a in am:
        if(am1 == ""):
            am1=am1 + "30" + str(a.id)
        else:
            am1=am1 + " 30" + str(a.id)

    for i in inv:
        if(inv1 == ""):
            inv1=inv1 + "40" + str(i.id)
        else:
            inv1=inv1 + " 40" + str(i.id)

    data = {"product": product, "mat": mat, "lab": lab, "am": am, "inv": inv,
            "user_id": id, "mat1": mat1, "lab1": lab1, "am1": am1, "inv1": inv1}
    return render(request, "calc_load.html", data)



# # получение данных из бд
# def index(request):
#     people = Person.objects.all()
#     return render(request, "index.html", {"people": people})
#
#
# # сохранение данных в бд
# def create(request):
#     if request.method == "POST":
#         person = Person()
#         person.name = request.POST.get("name")
#         person.age = request.POST.get("age")
#         person.save()
#     return HttpResponseRedirect("/")

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