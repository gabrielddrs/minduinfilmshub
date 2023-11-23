from fastapi import APIRouter
from api.v1.endpoints import film
from api.v1.endpoints import serie

api_router = APIRouter()

api_router.include_router(film.router, prefix='/films', tags=["films"])
api_router.include_router(serie.router, prefix='/series', tags=["Series"])
