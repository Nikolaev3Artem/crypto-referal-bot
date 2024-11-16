from backend.models import Addresses, Users
from backend.schemas.user import UserCreate
from utils.base_repository import BaseRepository
from asgiref.sync import sync_to_async


class UserRepository(BaseRepository):
    
    @sync_to_async
    def get_user(self, id: int) -> Users:
        return Users.objects.prefetch_related("invited_by").get(user_id=id)
    
    @sync_to_async
    def create_user(self, user: UserCreate) -> Users:
        return Users.objects.create(**user.dict())

user_repository = UserRepository(model=Users)
