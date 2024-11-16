from backend.constants.enums import BlockchainEnum
from pydantic import BaseModel
from backend.schemas.user import UserBase

class AddressBase(BaseModel):
    blockchain: BlockchainEnum | None = None
    balance: float
    owner_id: UserBase

class AddressCreate(UserBase):
    ...

class AddressGet(UserBase):
    id: int

class AddressUpdate(BaseModel):
    blockchain: BlockchainEnum | None = None
    balance: float | None = None
    owner_id: UserBase | None = None