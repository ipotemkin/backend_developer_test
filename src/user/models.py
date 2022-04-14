from typing import List, Optional

from pydantic import BaseModel, Field

from src.stats.models import StatResponseV1


class UserResponseV1(BaseModel):
    id: Optional[int]
    login: str
    name: str


class UserRequestV1(BaseModel):
    login: str
    name: str


class UserUpdateRequestV1(BaseModel):
    id: Optional[int]
    login: Optional[str]
    name: Optional[str]


class UserStatsResponseV1(BaseModel):
    user: UserResponseV1
    stats: List[StatResponseV1]
