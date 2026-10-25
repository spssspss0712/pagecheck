import os
from datetime import datetime
from sqlalchemy import create_engine, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

db_url = os.getenv("DATABASE_URL", "sqlite:///./pagecheck.db")
engine = create_engine(db_url, echo=True, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Check(Base):
    __tablename__ = "checks"
    id: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[datetime]
    result: Mapped[dict | None] = mapped_column(JSON)
    error: Mapped[str | None]


Base.metadata.create_all(engine)
