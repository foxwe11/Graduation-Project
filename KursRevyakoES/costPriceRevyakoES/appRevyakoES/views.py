from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from rest_framework import generics
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

class ProductAPIList(generics.ListCreateAPIView):
    """Список продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

