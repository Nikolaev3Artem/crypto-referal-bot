# Generated by Django 4.2.6 on 2024-11-20 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0010_alter_addresses_address_alter_users_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailings",
            name="send",
            field=models.BooleanField(default=False),
        ),
    ]
