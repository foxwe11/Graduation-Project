from django.db import models

# Create your models here.

class User(models.Model):
    login = models.CharField(max_length=100, verbose_name="Логин")
    password = models.CharField(max_length=100, verbose_name="Пароль")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'User'

class Product(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    output_volume = models.IntegerField()
    period = models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.cost_price * self.output_volume


    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'Product'

class Material_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    material_name = models.CharField(max_length=100)
    count = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)



    def __str__(self):
        return self.material_name

    class Meta:
        db_table = 'Material_costs'

class Labor_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    salary = models.IntegerField()
    deduction = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.profession

    class Meta:
        db_table = 'Labor_costs'

class Amortization_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=100)
    count_equipment = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_life = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.equipment_name

    class Meta:
        db_table = 'Amortization_costs'

class Invoice_costs(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice_name = models.CharField(max_length=100)
    count = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.invoice_name

    class Meta:
        db_table = 'Invoice_costs'