from django.db import models


class BlockchainEnum(models.TextChoices):
    ETHEREUM = "Eth/Base/BSC/Pol"
    SOLANA = "Solana"
    TRON = "Tron"