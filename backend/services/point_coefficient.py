from backend.models import Users
from backend.repositories.pointcoefficient_repo import point_coefficient_repository


class PointCoefficientService:

    @staticmethod
    async def get_on_connection() -> Users:
        point_coefficient = await point_coefficient_repository.get_coefficient()
        return point_coefficient.on_connection

    @staticmethod
    async def get_on_first_level_referal() -> Users:
        point_coefficient = await point_coefficient_repository.get_coefficient()
        return point_coefficient.first_level_ref
