# Generated by Django 5.2 on 2025-04-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
