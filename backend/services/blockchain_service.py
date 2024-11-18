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

        if not user:
            raise ValueError("User not found")

        address_data = address.dict()
        address_data["owner_id"] = user.id
        return await blockchain_repository.create_address(AddressCreate(**address_data))

    @staticmethod
    async def update_address(address: AddressUpdate):
        return await blockchain_repository.update_address(address)
