from typing import List

from src.user.models import UserResponseV1, UserRequestV1, UserUpdateRequestV1
from src.stats.models import StatResponseV1, StatRequestV1, StatUpdateRequestV1


class UserServiceProtocol:
    def get_all(self) -> List[UserResponseV1]:
        raise NotImplementedError

    def get_one(self, id: int) -> UserResponseV1:
        raise NotImplementedError

    def create(self, user: UserRequestV1) -> None:
        raise NotImplementedError

    def update(self, user: UserUpdateRequestV1) -> UserResponseV1:
        raise NotImplementedError

    def delete(self, id: int) -> None:
        raise NotImplementedError


class StatServiceProtocol:
    def get_all(self) -> List[StatResponseV1]:
        raise NotImplementedError

    def get_one(self, id: int) -> StatResponseV1:
        raise NotImplementedError

    def create(self, stats: StatRequestV1) -> None:
        raise NotImplementedError

    def update(self, id: int, stat_data: StatUpdateRequestV1) -> StatResponseV1:
        raise NotImplementedError

    def delete(self, id: int) -> None:
        raise NotImplementedError

    def get_stats_by_user_id(self, id: int, date_from, date_to) -> StatResponseV1:
        raise NotImplementedError
