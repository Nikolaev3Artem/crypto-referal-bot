# Generated by Django 5.1.3 on 2024-11-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0002_alter_botmessages_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="botmessages",
            name="message",
            field=models.CharField(default="None", max_length=3000),
        ),
        migrations.AlterField(
            model_name="botmessages",
            name="title",
            field=models.CharField(default="None", max_length=200),
        ),
    ]