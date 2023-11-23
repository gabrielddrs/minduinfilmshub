from typing import Optional
from sqlmodel import SQLModel, Field

class SerieModel(SQLModel, table=True):
    __tablename__ = 'series'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default=None, index=True)
    genre: str = Field(default=None, index=True)
    imdb_rating: float = Field(default=None, index=True)
    episodes: int = Field(default=None)
    seasons: int = Field(default=None)
