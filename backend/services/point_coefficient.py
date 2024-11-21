from backend.repositories.pointcoefficient_repo import point_coefficient_repository


class PointCoefficientService:

    @staticmethod
    async def get_coefficient_points_on_connection() -> float:
        point_coefficient = await point_coefficient_repository.get_coefficient()
        return point_coefficient.on_connection

    @staticmethod
    async def get_first_level_referral_points() -> float:
        point_coefficient = await point_coefficient_repository.get_coefficient()
        return point_coefficient.first_level_ref

    @staticmethod
    async def get_second_level_referral_points() -> float:
        point_coefficient = await point_coefficient_repository.get_coefficient()
        return point_coefficient.second_level_ref
