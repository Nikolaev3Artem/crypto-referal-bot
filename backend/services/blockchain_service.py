import re

import requests

from backend.models import Addresses
from backend.repositories.blockchain_repo import blockchain_repository
from backend.schemas.address import AddressCreate, AddressUpdate
from backend.services.user_service import UserService
from bot_backend.settings import ETHERSCAN_HOST, ETHERSCAN_TOKEN, TRONSCAN_HOST


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
    async def validate_etereum_address(address: str) -> dict:
        if not re.fullmatch(r"0x[a-fA-F0-9]{40}", address):
            return False
        chainids = [1, 8453, 56, 137]
        for item in chainids:
            responce = requests.get(
                f"{ETHERSCAN_HOST}?chainid={item}&module=account&action=tokentx&address={address}&apikey={ETHERSCAN_TOKEN}"
            )
            if responce.status_code == 200 and responce.json()["status"] == "1" and responce.json()["message"] == "OK":
                return True
        return False

    @staticmethod
    async def validate_solana_address(address: str) -> bool:
        if not re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{32,44}", address):
            return False
        return True

    @staticmethod
    async def validate_tron_address(address: str) -> bool:
        if not re.fullmatch(r"T[A-Za-z1-9]{33}", address):
            return False
        responce = requests.get(f"{TRONSCAN_HOST}?address={address}&asset_type=0")
        responce_data = responce.json()
        if responce_data["data"][0] is None or float(responce_data["data"][0]["token_value"]) == 0:
            return False
        if float(responce_data["data"][0]["token_value"]) > 0:
            return True
