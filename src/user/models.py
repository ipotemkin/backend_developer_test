from typing import List, Optional

from pydantic import BaseModel, Field

from src.stats.models import StatResponseV1


class UserResponseV1(BaseModel):
    id: Optional[int]
    login: str
    name: str


class UserAddRequestV1(BaseModel):
    id: Optional[int]
    login: str
    name: str


class UserStatsResponseV1(BaseModel):
    user: UserResponseV1
    stats: List[StatResponseV1]
