from backend.models import Users
from backend.repositories.user_repo import user_repository
from backend.schemas.user import UserCreate
from backend.services.point_coefficient import PointCoefficientService

class UserService():
    
    @staticmethod
    async def get_user(id: int) -> Users:
        return await user_repository.get_user(id=id)
    
    @staticmethod
    async def create_user(user: UserCreate):
        return await user_repository.create_user(user)

    @staticmethod
    async def reward_on_connection(user_id: int):
        points = await PointCoefficientService.get_on_connection()
        return await user_repository.reward_on_connection(id=user_id, points=points)