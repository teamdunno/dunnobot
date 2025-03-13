from typing import Annotated, Optional
from pydantic import BaseModel, FileUrl, HttpUrl
import httpx


class User(BaseModel):
    login: str
    avatar_url: Annotated[str, FileUrl]
    url: Annotated[str, HttpUrl]
    html_url: Annotated[str, HttpUrl]
    repos_url: Annotated[str, HttpUrl]


class FullUser(User):
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None


class Repository(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    html_url: Annotated[str, HttpUrl]
    owner: User

    stargazers_count: int
    watchers_count: int
    language: Optional[str]


def get_user(username: str) -> FullUser:
    url = f"https://api.github.com/users/{username}"
    response = httpx.get(url)
    response.raise_for_status()
    return FullUser(**response.json())


def get_repo(repo: str) -> Repository:
    url = f"https://api.github.com/repos/{repo}"
    response = httpx.get(url)
    response.raise_for_status()
    return Repository(**response.json())
