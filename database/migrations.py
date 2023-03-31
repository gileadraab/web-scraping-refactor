from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import enum
from sqlalchemy import Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy import create_engine
import datetime
import os
from dotenv import load_dotenv


load_dotenv()

USER = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")


class Base(DeclarativeBase):
    pass


class UrlType(enum.Enum):
    PYTHON_REQUEST = 0
    SELENIUM = 1


class FetchStatus(enum.Enum):
    FETCHED = 0
    UNFETCHED = 1


class ProcessStatus(enum.Enum):
    PROCESSED = 0
    UNPROCESSED = 1


class HtmlType(enum.Enum):
    MOVIE_LIST = 0
    MOVIE = 1


class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    type: Mapped[enum] = mapped_column(Enum(UrlType))
    fetch_status: Mapped[enum] = mapped_column(Enum(FetchStatus))
    process_status: Mapped[enum] = mapped_column(Enum(ProcessStatus))
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Html(Base):
    __tablename__ = "html"

    id: Mapped[int] = mapped_column(primary_key=True)
    html: Mapped[str] = mapped_column(String)
    html_type = mapped_column(Enum(HtmlType))
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    rating: Mapped[Optional[float]]
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r}, rating={self.rating!r})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"

    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    ratings = relationship(
        "Rating", back_populates="user", cascade="all, delete-orphan"
    )


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    rating: Mapped[Optional[float]]
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="ratings")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    comment: Mapped[str] = mapped_column(String())
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="comments")


Base.metadata.create_all(engine)
