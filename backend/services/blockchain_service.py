from backend.models import Addresses
from backend.repositories.blockchain_repo import blockchain_repository
from backend.schemas.address import AddressCreate, AddressUpdate
from backend.services.user_service import UserService
import requests
from bot_backend.settings import ETHERSCAN_TOKEN, ETHERSCAN_HOST, TRONSCAN_HOST
class BlockchainService():

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
    async def validate_etereum_address(address: str) -> dict:
        responce = requests.get(f'{ETHERSCAN_HOST}?chainid=1&module=account&action=tokentx&address={address}&apikey={ETHERSCAN_TOKEN}')
        if responce.status_code == 200:
            return {"status": 200}
        elif responce.status_code == 0:
            return {"status": 404, "result": f"Такого адресса не существует: {address}"}
    
    @staticmethod
    async def validate_base_address(address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_polygon_address(address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_solana_address(address: str) -> bool:
        return True
    
    @staticmethod
    async def validate_tron_address(address: str) -> bool:
        responce = requests.get(f'{TRONSCAN_HOST}?address={address}&asset_type=0')
        print(responce.json())
        if int(responce.data['token_value']) > 0:
            return {"status": 200}
        elif int(responce.data['token_value']) == 0:
            return {"status": 404, "result": f"Такого адресса не существует: {address}"}
    
    @staticmethod
    async def validate_bsc_address(address: str) -> bool:
        return True