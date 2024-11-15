# Generated by Django 5.1.3 on 2024-11-14 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BotMessages",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("message", models.CharField(max_length=4000)),
            ],
            options={
                "verbose_name": "Сообщение бота",
                "verbose_name_plural": "Сообщения бота",
            },
        ),
        migrations.CreateModel(
            name="PointCoefficients",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_level_ref", models.FloatField(default=0.0)),
                ("second_level_ref", models.FloatField(default=0.0)),
                ("on_connection", models.FloatField(default=0.0)),
            ],
            options={
                "verbose_name": "Коефициент",
                "verbose_name_plural": "Коефициенты",
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255)),
                ("user_id", models.IntegerField()),
                ("referral_link", models.CharField(max_length=500)),
                ("points", models.FloatField(default=0.0)),
                ("language", models.CharField(blank=True, max_length=100, null=True)),
                ("bio", models.CharField(blank=True, max_length=140, null=True)),
                (
                    "invited_by",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referrals",
                        to="backend.users",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Mailings",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("message", models.CharField(max_length=4000)),
                ("users", models.ManyToManyField(related_name="airdrops", to="backend.users")),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.CreateModel(
            name="Airdrops",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("points", models.IntegerField()),
                ("users", models.ManyToManyField(related_name="airdrop", to="backend.users")),
            ],
            options={
                "verbose_name": "Аирдроп",
                "verbose_name_plural": "Аирдропы",
            },
        ),
        migrations.CreateModel(
            name="Addresses",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("address", models.CharField(max_length=300)),
                ("balance", models.FloatField(default=0.0)),
                (
                    "blockchain",
                    models.CharField(
                        choices=[
                            ("eth/base/plgn", "Ethereum/Base/Polygon"),
                            ("solana", "Solana"),
                            ("tron", "Tron"),
                            ("bsc", "BSC"),
                        ]
                    ),
                ),
                (
                    "owner_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="user", to="backend.users"
                    ),
                ),
            ],
        ),
    ]