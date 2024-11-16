from backend.models import Addresses
from backend.schemas.address import AddressCreate, AddressUpdate
from utils.base_repository import BaseRepository
from asgiref.sync import sync_to_async

class BlockchainRepository(BaseRepository):
    
    @sync_to_async
    def get_address(self, id: int) -> Addresses:
        return Addresses.objects.select_related("owner_id").prefetch_related("invited_by").get(id=id)
    
    @sync_to_async
    def create_address(self, address: AddressCreate):
        return Addresses.objects.create(**address.dict())
    
    @sync_to_async
    def update_address(self, address: AddressUpdate) -> Addresses:
        return

blockchain_repository = BlockchainRepository(model=Addresses)
