from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar
from models.serie_model import SerieModel
from core.deps import get_session

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


router = APIRouter()

#POST SERIE
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=SerieModel)
async def post_serie(serie: SerieModel, db: AsyncSession = Depends(get_session)):
    new_serie = SerieModel(
        title=serie.title,
        genre=serie.genre,
        episodes=serie.episodes,
        seasons = serie.seasons
    )

    db.add(new_serie)
    await db.commit()
    return new_serie

#GET SERIES
@router.get('/', response_model=List[SerieModel])
async def get_series(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SerieModel)
        result = await session.execute(query)
        series: List[SerieModel] = result.scalars().all()

        return series

#GET SERIE
@router.get('/{id_serie}', response_model=SerieModel)
async def get_serie(id_serie: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SerieModel).filter(SerieModel.id==id_serie)
        result = await session.execute(query)
        serie: SerieModel = result.scalars().first()

        if not serie:
            raise HTTPException(detail='Serie not found', status_code=status.HTTP_404_NOT_FOUND)
        
        return serie

#PUT SERIE
@router.put('/{id_serie}', status_code=status.HTTP_202_ACCEPTED, response_model=SerieModel)
async def put_serie(id_serie: int, serie:SerieModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SerieModel).filter(SerieModel.id == id_serie)
        result = await session.execute(query)
        serie_up: SerieModel = result.scalars().first()

        if not serie_up:
            raise HTTPException(detail='Serie not found. Try again', status_code=status.HTTP_404_NOT_FOUND)
        
        serie_up.title = serie.title
        serie_up.genre = serie.genre
        serie_up.imdb_rating = serie.imdb_rating
        serie_up.episodes = serie.episodes
        serie_up.seasons = serie.seasons

        await db.commit()
        await db.refresh(serie_up)

        return serie_up

#DELETE SERIES
@router.delete('/{id_serie}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_serie(id_serie: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SerieModel).filter(SerieModel.id == id_serie)
        result = await session.execute(query)
        serie_del: SerieModel = result.scalars().first()

        if not serie_del:
            raise HTTPException(detail='Serie not found. Try again', status_code=status.HTTP_404_NOT_FOUND)
        
        await session.delete(serie_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
