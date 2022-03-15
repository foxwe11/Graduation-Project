from django.db import models

# Create your models here.

class User(models.Model):
    login = models.CharField(max_length=100, verbose_name="Логин")
    password = models.CharField(max_length=100, verbose_name="Пароль")

    def __str__(self):
        return str(self.login)

    class Meta:
        db_table = 'User'


class Product(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product_name = models.CharField(max_length=100, verbose_name="Название продукции")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Себестоимость")
    currency = models.CharField(max_length=10, verbose_name="Валюта")
    output_volume = models.IntegerField(verbose_name="Объём выпуска")
    period = models.IntegerField(default=1, verbose_name="Период")
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Цена продажи")
    return_on_sales = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Рентабельность продаж (%)")
    breakeven_point = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Точка безубыточности")

    @property
    def total_cost(self):
        return self.cost_price * self.output_volume

    def price(self):
        mat = Material_costs.objects.filter(product_id = self.id)
        lab = Labor_costs.objects.filter(product_id = self.id)
        am = Amortization_costs.objects.filter(product_id = self.id)
        inv = Invoice_costs.objects.filter(product_id = self.id)
        price = 0.0
        price1 = 0.0

        for m in mat:
            price = price + float(m.total_price)
        for l in lab:
            price1 = price1 + float(l.total_price)
        for a in am:
            price1 = price1 + float(a.total_price)
        for i in inv:
            price1 = price1 + float(i.total_price)

        price2 = price +price1
        return float (price2) / float (self.output_volume)

    def sale(self):
        return (float(self.sale_price) - float(self.cost_price))/float(self.sale_price)*100

    def breakeven(self):
        mat = Material_costs.objects.filter(product_id=self.id)
        lab = Labor_costs.objects.filter(product_id=self.id)
        am = Amortization_costs.objects.filter(product_id=self.id)
        inv = Invoice_costs.objects.filter(product_id=self.id)
        price = 0.0
        price1 = 0.0

        for m in mat:
            price = price + float(m.total_price)
        for l in lab:
            price1 = price1 + float(l.total_price)
        for a in am:
            price1 = price1 + float(a.total_price)
        for i in inv:
            price1 = price1 + float(i.total_price)

        return float(price1) / (float(self.sale_price) - float(price))

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'Product'


class Material_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукция")
    material_name = models.CharField(max_length=100, verbose_name="Название материала")
    count = models.IntegerField(verbose_name="Количество")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")

    def price(self):
        return float(self.cost) * float (self.count)

    def __str__(self):
        return self.material_name

    class Meta:
        db_table = 'Material_costs'


class Labor_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукция")
    profession = models.CharField(max_length=100, verbose_name="Профессия")
    number_of_people = models.IntegerField(verbose_name="Количество людей")
    salary = models.IntegerField(verbose_name="Зарплата")
    deduction = models.IntegerField(verbose_name="Отчисления")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")

    def price(self, product_id):
        product = Product.objects.get(id=product_id)
        return float(self.number_of_people) * (
                    float(self.salary) + float(self.salary) * float(self.deduction) / 100) / 30 * float(product.period)

    def __str__(self):
        return self.profession

    class Meta:
        db_table = 'Labor_costs'


class Amortization_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукция")
    equipment_name = models.CharField(max_length=100, verbose_name="Название оборудования")
    count_equipment = models.IntegerField(verbose_name="Количество")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    service_life = models.IntegerField(verbose_name="Срок эксплуатации")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")

    def price(self, product_id):
        product = Product.objects.get(id=product_id)
        return float(self.count_equipment)*float(self.cost)*((100/float(self.service_life))/100*float(product.period)/365)

    def __str__(self):
        return self.equipment_name

    class Meta:
        db_table = 'Amortization_costs'


class Invoice_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукция")
    invoice_name = models.CharField(max_length=100, verbose_name="Название")
    count = models.IntegerField(verbose_name="Количество")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")

    def price(self):
        return float(self.cost) * float (self.count)

    def __str__(self):
        return self.invoice_name

    class Meta:
        db_table = 'Invoice_costs'