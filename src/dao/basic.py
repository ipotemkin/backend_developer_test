from typing import List

from fastapi.responses import JSONResponse

from sqlalchemy import select, insert, delete, update
from sqlalchemy.future import Engine

from src.errors import (
    NotFoundError,
    NoContentError,
    BadRequestError,
    DatabaseError,
)


class BasicDAO:
    def __init__(self, engine: Engine, model, schema, schema_safe=None):
        self._engine = engine
        self.model = model
        self.schema = schema  # if validation needed while creating/updating a record
        self.schema_safe = schema_safe if schema_safe else schema

    def get_all(self) -> List:
        query = select(self.model)
        with self._engine.connect() as connection:
            items_data = connection.execute(query)

        return [self.schema_safe(**item_data) for item_data in items_data]

    def get_one(self, pk: int):
        query = select(self.model).where(self.model.c.id == pk)
        with self._engine.connect() as connection:
            item_data = connection.execute(query).first()

        if not item_data:
            raise NotFoundError

        return self.schema_safe(**item_data)

    # TODO return a new item endpoint
    def create(self, item) -> None:
        query = insert(self.model).values(**item.dict(exclude={"id"}))

        try:
            with self._engine.connect() as connection:
                connection.execute(query)
                connection.commit()
        except Exception as e:
            raise DatabaseError(e)

    def update(self, pk: int, item):
        if not item:
            raise NoContentError

        if ("id" in item) and (pk != item["id"]):
            raise BadRequestError

        query = update(self.model).where(self.model.c.id == pk).values(**item.dict(exclude_unset=True))

        try:
            with self._engine.connect() as connection:
                connection.execute(query)
                connection.commit()
        except Exception as e:
            raise DatabaseError(e)

        return self.get_one(pk)

    def delete(self, pk: int) -> None:
        query = delete(self.model).where(self.model.c.id == pk)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()
