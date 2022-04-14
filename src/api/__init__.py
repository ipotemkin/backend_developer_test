import sqlalchemy as sa
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.api import users, protocols, stats
from src.database import DatabaseSettings, create_database_url
from src.dependencies import get_engine
from src.github_api import get_github_repos_by_login, update_stats

from src.stats.service import StatService
from src.user.service import UserService


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0',
        docs_url="/",  # TODO comments
    )

    application.include_router(users.router)
    application.include_router(stats.router)

    engine = get_engine()

    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service

    stat_service = StatService(engine)
    application.dependency_overrides[protocols.StatServiceProtocol] = lambda: stat_service

    return application


app = get_application()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # sets an interval for updating DB
async def on_startup():

    # TODO This code should be refactored
    engine = get_engine()
    stat_service = StatService(engine)
    user_service = UserService(engine)
    _users = user_service.get_all()
    for user in _users:
        repos = await get_github_repos_by_login(user.login)
        update_stats(user.id, repos, stat_service)
