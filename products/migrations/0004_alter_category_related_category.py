# Generated by Django 3.2.8 on 2021-10-09 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_related_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='related_category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
