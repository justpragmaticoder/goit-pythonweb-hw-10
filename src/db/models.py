from datetime import datetime, date

from sqlalchemy import Integer, String, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.sqltypes import DateTime, Date


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    birthday_date: Mapped[date] = mapped_column(
        "birthday_date", Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    info: Mapped[str] = mapped_column(String(500), nullable=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
