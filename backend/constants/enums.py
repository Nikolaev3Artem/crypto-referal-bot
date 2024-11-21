from django.db import models


class BlockchainEnum(models.TextChoices):
    ETHEREUM = "Ethereum"
    BASE = "Base"
    POLYGON = "Polygon"
    SOLANA = "Solana"
    TRON = "Tron"
    BSC = "BSC"
