# Generated by Django 5.1.3 on 2024-11-15 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_alter_botmessages_message_alter_botmessages_title"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BotMessages",
        ),
    ]
