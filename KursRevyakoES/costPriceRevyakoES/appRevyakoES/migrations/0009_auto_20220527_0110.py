# Generated by Django 3.2.9 on 2022-05-26 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRevyakoES', '0008_alter_product_cost_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='breakeven_point',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Точка безубыточности'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Себестоимость'),
        ),
        migrations.AlterField(
            model_name='product',
            name='period',
            field=models.IntegerField(verbose_name='Период'),
        ),
        migrations.AlterField(
            model_name='product',
            name='return_on_sales',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Рентабельность продаж (%)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена продажи'),
        ),
    ]