from typing import Optional
from sqlmodel import Field, SQLModel

class FilmModel(SQLModel, table=True):
    __tablename__ = 'filmes'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default=None, index=True)
    genre: str = Field(default=None, index=True)
    imdb_rating: float = Field(default=None, index=True)
    director: str = Field(default=None, index=True)
    year: int = Field(default=None, index=True)
