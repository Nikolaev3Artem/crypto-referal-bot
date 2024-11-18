from pydantic import BaseModel

from backend.constants.enums import BlockchainEnum
from backend.models import Users
from backend.schemas.user import UserBase


class AddressBase(BaseModel):
    blockchain: BlockchainEnum
    balance: float | None = None  # может временно
    owner_id: Users
    address: str


class AddressCreate(AddressBase):
    pass


# class AddressGet(UserBase):
#     id: int


class AddressUpdate(BaseModel):
    blockchain: BlockchainEnum | None = None
    balance: float | None = None
    owner_id: UserBase | None = None
