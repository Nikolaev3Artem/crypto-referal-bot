from backend.models import Addresses, Users
from backend.schemas.user import UserCreate
from backend.services.point_coefficient import PointCoefficientService
from utils.base_repository import BaseRepository
from asgiref.sync import sync_to_async
from backend.repositories.pointcoefficient_repo import point_coefficient_repository

class UserRepository(BaseRepository):
    
    @sync_to_async
    def get_user(self, id: int) -> Users:
        return Users.objects.prefetch_related("invited_by").get(user_id=id)
    
    @sync_to_async
    def create_user(self, user: UserCreate) -> Users:
        return Users.objects.create(**user.dict())

    @sync_to_async
    def reward_on_connection(self, id: int, points: float) -> Users:
        user = Users.objects.get(user_id=id)
        user.points += points
        user.save()
        return user.points

user_repository = UserRepository(model=Users)