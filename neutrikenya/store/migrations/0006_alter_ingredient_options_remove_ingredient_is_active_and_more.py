# Generated by Django 5.2.1 on 2025-06-09 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_ingredient_product_compatible_products_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={},
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='product',
            name='compatible_products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='product',
            name='key_ingredients',
        ),
        migrations.RemoveField(
            model_name='product',
            name='skin_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='usage_instructions',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='scientific_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentration', models.CharField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.ingredient')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='store.product')),
            ],
            options={
                'ordering': ['ingredient__name'],
            },
        ),
        migrations.CreateModel(
            name='ComplementaryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('benefit_description', models.TextField()),
                ('recommended_usage', models.TextField(blank=True)),
                ('complementary_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complemented_by', to='store.product')),
                ('main_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complementary_products', to='store.product')),
            ],
            options={
                'unique_together': {('main_product', 'complementary_product')},
            },
        ),
    ]
