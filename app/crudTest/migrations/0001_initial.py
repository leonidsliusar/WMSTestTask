# Generated by Django 4.2.7 on 2023-11-18 07:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('parent', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crudTest.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('count', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)])),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('category_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crudTest.category')),
            ],
        ),
    ]
