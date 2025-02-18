from typing import List

from fastapi import APIRouter, status, Depends, Path

from src.api.protocols import StatServiceProtocol
from src.stats.models import (
    StatResponseV1,
    StatUpdateRequestV1,
    StatRequestV1,
    StatResponseListV1
)

router = APIRouter(
    tags=['Stats']
)


@router.get(
    path='/v1/stats',
    response_model=List[StatResponseListV1],
    summary='Статистика',
    description='Возвращает список всех стат записей.'
)
def get_all_stats(
        stat_service: StatServiceProtocol = Depends()
):
    return stat_service.get_all()


@router.get(
    path='/v1/stats/{id}',
    response_model=StatRequestV1,
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
    path='/v1/stats/{id}',
    response_model=StatResponseV1,
    summary='Изменить запись о репозитории',
    description='Изменяет запись о репозитории.'
)
def update_stats_by_id(
        stat_data: StatUpdateRequestV1,
        id: int = Path(..., ge=1),
        stat_service: StatServiceProtocol = Depends(),
):
    return stat_service.update(id, stat_data)


@router.post(
    path='/v1/stats/update_or_create',
    response_model=StatResponseV1,
    status_code=status.HTTP_201_CREATED,
    summary='Изменить запись о репозитории или создать новую',
    description='Изменяет запись о репозитории или создает новую.'
)
def update_or_create_stats(
        stat_data: StatUpdateRequestV1,
        stat_service: StatServiceProtocol = Depends(),
):
    print(stat_data)
    filter_d = {
        'date': stat_data.date,
        'repo_id': stat_data.repo_id,
        'user_id': stat_data.user_id
    }
    print('before update_or_create')
    stat_service.update_or_create(filter_d, stat_data)

    # return stat_service.update(id, stat_data)


# @router.patch(
#     path='/v1/stats',
#     response_model=StatResponseV1,
#     summary='Изменить запись о репозитории',
#     description='Изменяет запись о репозитории.'
# )
# def update_stats_by_id(
#         stat_data: StatUpdateRequestV1,
#         id: int = Path(..., ge=1),
#         stat_service: StatServiceProtocol = Depends(),
# ):
#     return stat_service.update(id, stat_data)
