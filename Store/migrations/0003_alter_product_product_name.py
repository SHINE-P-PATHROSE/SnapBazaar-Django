# Generated by Django 5.1 on 2024-09-09 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255),
        ),
    ]
