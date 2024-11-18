from pydantic import BaseModel

from backend.constants.enums import BlockchainEnum
from backend.schemas.user import UserBase


class AddressBase(BaseModel):
    blockchain: BlockchainEnum
    balance: float | None = None  # может временно
    owner_id: UserBase
    address: str


class AddressCreate(AddressBase):
    pass


class AddressGet(BaseModel):
    id: int


class AddressUpdate(BaseModel):
    blockchain: BlockchainEnum | None = None
    balance: float | None = None
    owner_id: UserBase | None = None
    address: str | None = None
