# Generated by Django 4.2.6 on 2024-11-22 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0011_mailings_send"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addresses",
            name="blockchain",
            field=models.CharField(choices=[("Eth/Base/BSC/Pol", "Ethereum"), ("Solana", "Solana"), ("Tron", "Tron")]),
        ),
        migrations.AlterField(
            model_name="addresses",
            name="owner_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to="backend.users"
            ),
        ),
        migrations.AlterField(
            model_name="mailings",
            name="message",
            field=models.TextField(default="None", max_length=3000),
        ),
    ]
