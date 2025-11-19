from typing import Optional

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime


engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class TaskOrm(Model):
   __tablename__ = "tasks"
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str]
   description: Mapped[str | None]


async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)