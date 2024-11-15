from django.db import models


class BlockchainEnum(models.TextChoices):
    ETHBASEPLGN = "eth/base/plgn", "Ethereum/Base/Polygon"
    SOLANA = "solana", "Solana"
    TRON = "tron", "Tron"
    BSC = "bsc", "BSC"
