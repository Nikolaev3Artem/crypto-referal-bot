# Generated by Django 4.2.6 on 2024-11-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0003_alter_botmessages_message_alter_botmessages_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="botmessages",
            name="message",
            field=models.TextField(default="None", max_length=3000),
        ),
    ]