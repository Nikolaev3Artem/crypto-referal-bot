from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: int
    username: str | None
    language: str | None
    bio: str | None = None

class UserCreate(UserBase):
    ...

class UserGet(UserBase):
    invited_by: UserBase
    points: float
    referral_link: str | None