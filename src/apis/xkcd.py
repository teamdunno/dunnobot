from pydantic import BaseModel, FileUrl
from annotated_types import Le, Gt
from typing import Annotated, Optional
import httpx


class Comic(BaseModel):
    num: Annotated[int, Gt(0)]
    title: str
    alt: str
    img: Annotated[str, FileUrl]

    month: Annotated[int, Le(12)]
    year: Annotated[int, Gt(0)]
    day: Annotated[int, Le(31)]

    link: Optional[str] = None


def get_current_comic() -> Comic:
    response = httpx.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    return Comic(**response.json())


def get_comic(comic_number: int) -> Comic:
    response = httpx.get(f"https://xkcd.com/{comic_number}/info.0.json")
    response.raise_for_status()
    return Comic(**response.json())
