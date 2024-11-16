from backend.models import Users
from backend.repositories.user_repo import user_repository
from backend.schemas.user import UserCreate

class UserService():
    
    @staticmethod
    async def get_user(id: int) -> Users:
        return await user_repository.get_user()
    
    @staticmethod
    async def create_user(user: UserCreate):
        return await user_repository.create_user(user)