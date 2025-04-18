# Generated by Django 5.2 on 2025-04-15 00:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittlelemonAPI", "0005_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="LittlelemonAPI.order",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together={("order", "menuitem")},
        ),
    ]
