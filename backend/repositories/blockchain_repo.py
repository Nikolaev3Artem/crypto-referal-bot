from backend.models import Addresses
from utils.base_repository import BaseRepository


class BlockchainRepository(BaseRepository):
    ...


blockchain_repository = BlockchainRepository(model=Addresses)
