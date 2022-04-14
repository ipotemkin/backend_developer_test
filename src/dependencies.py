import sqlalchemy as sa

from src.database import DatabaseSettings, create_database_url


def get_engine():

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True,
    )
    return engine
