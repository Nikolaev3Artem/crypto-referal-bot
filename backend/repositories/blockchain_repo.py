from asgiref.sync import sync_to_async

from backend.models import Addresses
from backend.schemas.address import AddressCreate, AddressUpdate
from utils.base_repository import BaseRepository


class BlockchainRepository(BaseRepository):

    @sync_to_async
    def get_address(self, id: int) -> Addresses:
        return self.model.objects.select_related("owner_id").prefetch_related("invited_by").get(id=id)

    @sync_to_async
    def create_address(self, address: AddressCreate):
        return self.model.objects.create(**address.dict())

    @sync_to_async
    def update_address(self, address: AddressUpdate) -> Addresses:
        return

    @sync_to_async
    def address_exists_check(self, address: str) -> Addresses:
        address = self.model.objects.filter(address=address).first()
        return address

blockchain_repository = BlockchainRepository(model=Addresses)
