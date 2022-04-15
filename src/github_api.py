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

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            if resp.status == 200:
                repos = [GitHubData.parse_obj(repo).dict() for repo in response]
                update_stats(user_id, repos, stat_service)


def update_stats(
        user_id: int,
        repos: List[dict],
        stat_service
):
    for repo in repos:
        repo['date'] = datetime.now()
        repo['user_id'] = user_id
        stat_data = StatRequestV1.parse_obj(repo)

        res = stat_service.update_by_filter(
            {
                'date': repo['date'],
                'user_id': repo['user_id'],
                'repo_id': repo['repo_id'],
            },
            stat_data
        )
        print('res in update_stats')
        print(res)
        if not res:
            stat_service.create(stat_data)
