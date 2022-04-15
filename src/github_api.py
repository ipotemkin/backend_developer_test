import aiohttp

from typing import List
from datetime import datetime

from pydantic import BaseModel, Field

from src.stats.models import StatRequestV1


class GitHubData(BaseModel):
    repo_id: int = Field(None, alias='id')
    stargazers: int = Field(None, alias='stargazers_count')
    forks: int = Field(None, alias='forks_count')
    watchers: int = Field(None, alias='watchers_count')


async def update_repos_by_login(login: str, user_id: int, stat_service) -> None:
    url = f'https://api.github.com/users/{login}/repos'

    # breakpoint()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # print(f'обновляем статистику для login:{login}, user_id:{user_id}')
            response = await resp.json()
            # print(f'resp.status = {resp.status}')
            if resp.status == 200:
                repos = [GitHubData.parse_obj(repo).dict() for repo in response]
                update_stats(user_id, repos, stat_service)


def update_stats(
        user_id: int,
        repos: List[dict],
        stat_service
):
    for repo in repos:
        repo['date'] = datetime.now().date()
        repo['user_id'] = user_id
        stat_data = StatRequestV1.parse_obj(repo)

        stat_service.update_or_create(
            {
                'date': repo['date'],
                'user_id': repo['user_id'],
                'repo_id': repo['repo_id'],
            },
            stat_data
        )
