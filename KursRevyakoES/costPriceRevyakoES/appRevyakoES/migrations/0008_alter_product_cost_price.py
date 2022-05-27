# Generated by Django 3.2.9 on 2022-05-22 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRevyakoES', '0007_alter_product_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Себестоимость'),
        ),
    ]