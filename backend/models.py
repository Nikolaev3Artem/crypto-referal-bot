from django.db import models

from backend.constants.enums import BlockchainEnum


class Users(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=False, default="None")
    referral_link = models.CharField(max_length=500, blank=False, default="None")
    points = models.FloatField(blank=False, default=0.0)
    language = models.CharField(max_length=100, blank=True, null=True, default="None")
    bio = models.CharField(max_length=255, blank=True, null=True, default="None")

    invited_by = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="referrals")

    def __str__(self):
        return str(self.user_id)


class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=300, blank=False, unique=True)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user")
    balance = models.FloatField(blank=False, default=0.0)
    blockchain = models.CharField(choices=BlockchainEnum.choices, blank=False)


class Airdrops(models.Model):
    id = models.AutoField(primary_key=True)
    points = models.FloatField(blank=False, default=0.0)
    users = models.ManyToManyField(Users, related_name="airdrop")

    class Meta:
        verbose_name = "Airdrop"
        verbose_name_plural = "Airdrops"


class Mailings(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=3000, blank=False, default="None")
    users = models.ManyToManyField(Users, related_name="airdrops")

    class Meta:
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"

    def __str__(self):
        return self.message


class PointCoefficients(models.Model):
    id = models.AutoField(primary_key=True)
    first_level_ref = models.FloatField(blank=False, default=0.0)
    second_level_ref = models.FloatField(blank=False, default=0.0)
    on_connection = models.FloatField(blank=False, default=0.0)

    class Meta:
        verbose_name = "Coefficient"
        verbose_name_plural = "Coefficients"
