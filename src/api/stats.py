from typing import List

from fastapi import APIRouter, status, Depends, Path
from fastapi.responses import JSONResponse

from src.api.protocols import StatServiceProtocol, UserServiceProtocol
from src.stats.models import StatResponseV1, StatUpdateRequestV1, StatRequestV1

router = APIRouter(
    tags=['Stats']
)


@router.get(
    path='/v1/stats',
    response_model=List[StatResponseV1],
    summary='Статистика',
    description='Возвращает список всех стат записей.'
)
def get_all_stats(
        stat_service: StatServiceProtocol = Depends()
):
    return stat_service.get_all()


@router.get(
    path='/v1/stats/{id}',
    response_model=StatResponseV1,
    summary='Информация о статистике',
    description='Возвращает информацию о статистике'
)
def get_stats_by_id(
        id: int = Path(..., ge=1),
        stat_service: StatServiceProtocol = Depends()
):
    return stat_service.get_one(id)


@router.put(
    path='/v1/stats',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить статистику',
    description='Добавляет статистику для отслеживания популярности репозиториев.',
)
def add_stats(
        stat_data: StatRequestV1,
        stat_service: StatServiceProtocol = Depends()
):
    stat_service.create(stat_data)


@router.delete(
    path='/v1/stats/{id}',
    summary='Удалить статистику',
    description='Удаляет статистику.'
)
def delete_stats(
        id: int = Path(..., ge=1),
        stat_service: StatServiceProtocol = Depends()
):
    stat_service.delete(id)


@router.patch(
    path='/v1/stats/{stat_id}',
    response_model=StatResponseV1,
    summary='Изменить запись о репозитории',
    description='Изменяет запись о репозитории.'
)
def update_stats_by_id(
        stat_data: StatUpdateRequestV1,
        # uid: int = Path(..., ge=1),
        stat_id: int = Path(..., ge=1),
        stat_service: StatServiceProtocol = Depends(),
        user_service: UserServiceProtocol = Depends(),
):
    # user = user_service.get_one(uid)
    return stat_service.update(stat_id, stat_data)
