# Generated by Django 4.2.6 on 2024-11-16 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_mailings_message_alter_users_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]