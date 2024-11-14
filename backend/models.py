from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=255, blank=False, null=False
    )  # но если ник как у Unknown где просто пробелы или нету ника
    user_id = models.IntegerField(blank=False, null=False)
    referral_link = models.CharField(max_length=500, blank=False, null=False)
    points = models.FloatField(blank=False, null=False, default=0.0)
    language = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=140, blank=True, null=True)

    invited_by = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, related_name="referrals")

    def __str__(self):
        return self.user_id


class BlockchainEnum(models.TextChoices):
    ETHBASEPLGN = "eth/base/plgn", "Ethereum/Base/Polygon"
    SOLANA = "solana", "Solana"
    TRON = "tron", "Tron"
    BSC = "bsc", "BSC"


class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=300, blank=False)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user")
    balance = models.FloatField(blank=False, null=False, default=0.0)
    blockchain = models.CharField(choices=BlockchainEnum.choices, blank=False)


class Airdrops(models.Model):
    id = models.AutoField(primary_key=True)
    points = models.IntegerField(blank=False)
    users = models.ManyToManyField(Users, related_name="airdrop")

    class Meta:
        verbose_name = "Аирдроп"
        verbose_name_plural = "Аирдропы"


class Mailings(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=3000)
    users = models.ManyToManyField(Users, related_name="airdrops")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.message


class PointCoefficients(models.Model):
    id = models.AutoField(primary_key=True)
    first_level_ref = models.FloatField(blank=False, default=0.0)
    second_level_ref = models.FloatField(blank=False, default=0.0)
    on_connection = models.FloatField(blank=False, default=0.0)

    class Meta:
        verbose_name = "Коефициент"
        verbose_name_plural = "Коефициенты"


class BotMessages(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    message = models.CharField(max_length=3000, blank=False)

    class Meta:
        verbose_name = "Сообщение бота"
        verbose_name_plural = "Сообщения бота"

    def __str__(self):
        return self.title
