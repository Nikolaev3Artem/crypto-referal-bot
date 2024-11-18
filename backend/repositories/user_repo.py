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
    def reward_on_connection(self, user_id: int, points: float) -> Users:
        user = Users.objects.get(user_id=user_id)
        user.points += points
        user.save()
        return user.points

    @sync_to_async
    def update_refferral_link_link(self, user_id: int, refferral_link: str) -> Users:
        user = Users.objects.get(user_id=user_id)
        user.referral_link = refferral_link
        user.save()
        return user.points
    
user_repository = UserRepository(model=Users)