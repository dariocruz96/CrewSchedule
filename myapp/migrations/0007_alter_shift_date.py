# Generated by Django 5.0.2 on 2024-04-09 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_shift_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='date',
            field=models.DateField(),
        ),
    ]