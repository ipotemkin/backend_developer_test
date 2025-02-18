from datetime import date
from typing import Optional

from pydantic import BaseModel


class StatResponseV1(BaseModel):
    id: Optional[int]
    repo_id: int
    date: date
    stargazers: int
    forks: int
    watchers: int


class StatResponseListV1(BaseModel):
    id: Optional[int]
    repo_id: int
    user_id: int
    date: date


class StatRequestV1(StatResponseV1):
    user_id: int


class StatUpdateRequestV1(BaseModel):
    id: Optional[int]
    repo_id: Optional[int]
    user_id: Optional[int]
    date: Optional[date]
    stargazers: Optional[int]
    forks: Optional[int]
    watchers: Optional[int]
