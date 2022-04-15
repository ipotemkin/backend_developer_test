from typing import List, Optional
from datetime import date

from fastapi import APIRouter, status, Depends, Path, Query

from src.api.protocols import UserServiceProtocol, StatServiceProtocol
from src.user.models import UserResponseV1, UserStatsResponseV1, UserRequestV1, UserResponseListV1

router = APIRouter(
    tags=['Users']
)


@router.get(
    path='/v1/users',
    response_model=List[UserResponseListV1],
    summary='Список пользователей',
    description='Возвращает список всех пользователей.'
)
def get_all_users(
        user_login: Optional[str] = Query(
            None, title="Login пользователя", description="Укажите login пользователя"
        ),
        user_name: Optional[str] = Query(
            None, title="Имя пользователя", description="Укажите имя пользователя"
        ),
        user_service: UserServiceProtocol = Depends()
):
    request_d = {}
    if user_login:
        request_d["login"] = user_login
    if user_name:
        request_d["name"] = user_name
    if request_d:
        return user_service.filter(request_d)
        # return user_service.execute_sql(user_login)
    return user_service.get_all()


@router.get(
    path='/v1/users/{id}',
    response_model=UserResponseV1,
    summary='Информация о пользователе',
    description='Возвращает информацию о пользователе.'
)
def get_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_one(id)


@router.put(
    path='/v1/users',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить пользователя',
    description='Добавляет пользователя для отслеживания популярности репозиториев.',
)
def add_user(
        user_data: UserRequestV1,
        user_service: UserServiceProtocol = Depends()
):
    user_service.create(user_data)


@router.delete(
    path='/v1/users/{id}',
    summary='Удалить пользователя',
    description='Удаляет пользователя.'
)
def delete_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    user_service.delete(id)


@router.get(
    path='/v1/users/{id}/stats',
    response_model=UserStatsResponseV1,
    summary='Получить репозитории пользователя',
    description='Выводит репозитории пользователя.'
)
def get_user_stats(
        id: int = Path(..., ge=1),
        date_from: Optional[date] = Query(
            None, title="Начальная дата", description="Укажите начальную дату для выборки"
        ),
        date_to: Optional[date] = Query(
            None, title="Конечная дата", description="Укажите конечную дату для выборки"
        ),
        stat_service: StatServiceProtocol = Depends(),
        user_service: UserServiceProtocol = Depends()

):
    user = user_service.get_one(id)
    stats = stat_service.get_stats_by_user_id(id, date_from, date_to)
    records_count = len(stats)
    repos_count = len(set([record.repo_id for record in stats]))

    return {
        'user': user,
        'summary': {
            'records_count': records_count,
            'repos_count': repos_count
        },
        'stats': stats
    }
