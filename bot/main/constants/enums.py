from django.db import models


class StartMenuEnum(models.TextChoices):
    HELP = "help"
    ACCOUNT = "account"
