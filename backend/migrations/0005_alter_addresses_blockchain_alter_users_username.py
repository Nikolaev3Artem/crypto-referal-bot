# Generated by Django 4.2.6 on 2024-11-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0004_delete_botmessages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addresses",
            name="blockchain",
            field=models.CharField(
                choices=[
                    ("Ethereum", "Ethereum"),
                    ("Base", "Base"),
                    ("Polygon", "Polygon"),
                    ("Solana", "Solana"),
                    ("Tron", "Tron"),
                    ("BSC", "Bsc"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="users",
            name="username",
            field=models.CharField(default="None", max_length=255),
        ),
    ]
