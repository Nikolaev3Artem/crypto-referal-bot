from backend.models import PointCoefficients
from utils.base_repository import BaseRepository
from asgiref.sync import sync_to_async


class PointCoefficienRepository(BaseRepository):
    
    @sync_to_async
    def get_coefficient(self) -> PointCoefficients:
        return PointCoefficients.objects.filter().first()

point_coefficient_repository = PointCoefficienRepository(model=PointCoefficients)
