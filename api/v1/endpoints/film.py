from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar
from models.film_model import FilmModel
from core.deps import get_session

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()

#POST FILM
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=FilmModel)
async def post_film(film: FilmModel, db: AsyncSession = Depends(get_session)):
    film_new = FilmModel(
        title = film.title,
        genre = film.genre,
        imdb_rating = film.imdb_rating,
        director = film.director,
        year = film.year
    )

    db.add(film_new);
    await db.commit()

    return film_new

#GET FILMS
@router.get('/', response_model=List[FilmModel])
async def get_film(db: AsyncSession =  Depends(get_session)):
    async with db as session:
        query = select(FilmModel)
        result = await session.execute(query)
        films: List[FilmModel] = result.scalars().all()

        return films

#GET FILM
@router.get('/{id_film}', response_model=FilmModel)
async def get_film(id_film: int, db: AsyncSession= Depends(get_session)):
    async with db as session:
        query = select(FilmModel).filter(FilmModel.id == id_film)
        result = await session.execute(query)
        film: FilmModel = result.scalars().first()

        if not film:
            raise HTTPException(detail='Film not found. Try again', status_code=status.HTTP_404_NOT_FOUND)
        
        return film

#PUT FILM
@router.put('/{id_film}', status_code=status.HTTP_202_ACCEPTED, response_model=FilmModel)
async def put_film(id_film: int, film: FilmModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FilmModel).filter(FilmModel.id == id_film)
        result = await session.execute(query)
        film_up: FilmModel = result.scalars().first()

        if not film_up:
            raise HTTPException(detail='Film not found. Try again', status_code=status.HTTP_404_NOT_FOUND)

        film_up.title = film.title
        film_up.genre = film.genre
        film_up.imdb_rating = film.imdb_rating
        film_up.director = film.director
        film_up.year = film.year

        await db.commit()
        await db.refresh(film_up)

        return film_up

#DELETE FILM
@router.delete('/{id_film}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(id_film: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FilmModel).filter(FilmModel.id == id_film)
        result = await session.execute(query)
        film_del: FilmModel = result.scalars().first()

        if not film_del:
            raise HTTPException(detail='Film not found. Try again', status_code=status.HTTP_404_NOT_FOUND)
        
        await session.delete(film_del)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
