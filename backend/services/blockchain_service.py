from backend.models import Addresses
from backend.repositories.blockchain_repo import blockchain_repository
from backend.schemas.address import AddressCreate, AddressUpdate
from backend.services.user_service import UserService


class BlockchainService:

    @staticmethod
    async def get_address(id: int) -> Addresses:
        return await blockchain_repository.get_address()

    @staticmethod
    async def create_address(address: AddressCreate):
        user = await UserService.get_user(id=address.owner_id)
        address.owner_id = user
        return await blockchain_repository.create_address(address)

    @staticmethod
    async def update_address(address: AddressUpdate):
        return await blockchain_repository.update_address(address)

    @staticmethod
    async def validate_etereum_address(self, address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_base_address(self, address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_polygon_address(self, address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_solana_address(self, address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_tron_address(self, address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_bsc_address(self, address: str) -> bool:
        return True