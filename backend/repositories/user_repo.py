from typing import Union

from asgiref.sync import sync_to_async

from backend.models import Addresses, Users
from backend.schemas.user import UserCreate
from utils.base_repository import BaseRepository


class UserRepository(BaseRepository):

    @sync_to_async
    def get_user(self, id: int) -> Users:
        return Users.objects.prefetch_related("invited_by").get(user_id=id)

    @sync_to_async
    def create_user(self, user: UserCreate) -> Users:
        return Users.objects.create(**user.dict())

    @sync_to_async
    def reward_on_connection(self, user_id: int, points: float) -> int:
        user = Users.objects.get(user_id=user_id)
        user.points += points
        user.save()
        return user.points

    @sync_to_async
    def update_refferral_link_link(self, user_id: int, refferral_link: str) -> str:
        user = Users.objects.get(user_id=user_id)
        user.referral_link = refferral_link
        user.save()
        return user.referral_link

    @sync_to_async
    def update_invited_by(self, user_id: int, invited_by: int) -> int:
        refferer = Users.objects.get(user_id=invited_by)
        user = Users.objects.get(user_id=user_id)
        user.invited_by = refferer
        user.save()
        return user.invited_by

    @sync_to_async
    def refferer_user_first_level(self, user_id: int) -> Union[int, None]:
        user = self.model.objects.filter(user_id=user_id).first()
        if user.invited_by is not None:
            return user.invited_by.user_id
        else:
            return None

    @sync_to_async
    def reward_first_level(self, user_id: int, points: float) -> int:
        user = Users.objects.get(user_id=user_id)
        user.points += points
        user.save()
        return user.points

    @sync_to_async
    def refferer_user_second_level(self, user_id: int) -> Union[int, None]:
        user = self.model.objects.filter(user_id=user_id).first()
        if user.invited_by is not None:
            user = self.model.objects.filter(user_id=user.invited_by.user_id).first()
            if user.invited_by is not None:
                return user.invited_by.user_id
            else:
                return None

    @sync_to_async
    def reward_second_level(self, user_id: int, points: float) -> int:
        user = Users.objects.get(user_id=user_id)
        user.points += points
        user.save()
        return user.points

    @sync_to_async
    def user_exists_check(self, user_id: int) -> Users:
        user = self.model.objects.filter(user_id=user_id).first()
        return user

    @sync_to_async
    def get_user_refferals(self, user_id: int) -> list[Users]:
        return Users.objects.filter(invited_by__user_id=user_id).prefetch_related("invited_by").count()

    @sync_to_async
    def get_user_points(self, user_id: int) -> float:
        return Users.objects.get(user_id=user_id).points

    @sync_to_async
    def get_user_addresses(self, user_id: int) -> float:
        return Addresses.objects.filter(owner_id=user_id)


user_repository = UserRepository(model=Users)
