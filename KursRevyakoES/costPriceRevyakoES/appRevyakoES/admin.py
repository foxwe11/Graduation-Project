from django.contrib import admin
from .models import User ,Product, Material_costs, Labor_costs, Amortization_costs, Invoice_costs

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Material_costs)
admin.site.register(Labor_costs)
admin.site.register(Amortization_costs)
admin.site.register(Invoice_costs)