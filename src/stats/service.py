from typing import List

from pydantic import BaseModel
from sqlalchemy.future import Engine
from sqlalchemy import select

from datetime import date

from src.dao.basic import BasicDAO
from src.database.tables import stats
from .models import StatResponseV1, StatRequestV1, StatResponseListV1


class StatService(BasicDAO):
    def __init__(
            self,
            engine: Engine,
            model=stats,
            schema=StatRequestV1,
            # schema=StatResponseV1
            schema_list=StatResponseListV1
    ):
        super().__init__(engine, model, schema, schema_list)

    def get_stats_by_user_id(self, user_id: int, date_from: date, date_to: date) -> List[BaseModel]:
        query = select(self.model).where(self.model.c.user_id == user_id)
        if date_from:
            query = query.where(self.model.c.date >= date_from)
        if date_to:
            query = query.where(self.model.c.date <= date_to)

        with self._engine.connect() as connection:
            stats_data = connection.execute(query)

        return [StatResponseV1(**stat_data) for stat_data in stats_data]
