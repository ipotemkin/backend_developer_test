import sqlalchemy as sa
from fastapi import FastAPI

import src.api.protocols
from src.api import users, protocols
from src.database import DatabaseSettings, create_database_url
from src.user.service import UserService


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0',
        docs_url="/",  # TODO comments
    )

    application.include_router(users.router)

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
    )
    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


app = get_application()
