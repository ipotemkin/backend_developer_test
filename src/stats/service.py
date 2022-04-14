from sqlalchemy.future import Engine
from sqlalchemy import select

from src.dao.basic import BasicDAO
from src.database.tables import stats
from .models import StatResponseV1, StatRequestV1


class StatService(BasicDAO):
    def __init__(
            self,
            engine: Engine,
            model=stats,
            schema=StatRequestV1,
            schema_safe=StatResponseV1
    ):
        super().__init__(engine, model, schema, schema_safe)

    def get_stats_by_user_id(self, user_id: int, date_from, date_to):
        query = select(self.model).where(self.model.c.user_id == user_id)
        if date_from:
            query = query.where(self.model.c.date >= date_from)
        if date_to:
            query = query.where(self.model.c.date <= date_to)

        with self._engine.connect() as connection:
            stats_data = connection.execute(query)

        items = []
        for stat_data in stats_data:
            stat = StatResponseV1(**stat_data)
            items.append(stat)

        return items
