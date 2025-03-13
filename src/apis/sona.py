from pydantic import BaseModel
from typing import Optional
from enum import Enum
import httpx


class Book(Enum):
    Pu = "pu"
    KuSuli = "ku suli"
    KuLili = "ku lili"
    NoBook = "none"


class CoinedEra(Enum):
    PrePu = "pre-pu"
    PostPu = "post-pu"
    PostKu = "post-ku"


class UsageCategory(Enum):
    Core = "core"
    Common = "common"
    Uncommon = "uncommon"
    Obscure = "obscure"
    Sandbox = "sandbox"


class Resources(BaseModel):
    sona_pona: Optional[str] = ""
    lipamanka_semantic: Optional[str] = ""


class Representations(BaseModel):
    sitelen_emosi: Optional[str] = ""
    sitelen_jelo: Optional[list[str]] = []
    ligatures: Optional[list[str]] = []
    sitelen_sitelen: Optional[str] = ""
    ucsur: Optional[str] = ""


class Etymology(BaseModel):
    word: Optional[str] = ""
    alt: Optional[str] = ""


class Audio(BaseModel):
    link: str
    author: str


class InnerEtymologyTranslation(BaseModel):
    definition: Optional[str] = ""
    language: str


class Translation(BaseModel):
    commentary: str
    definition: str
    etymology: list[InnerEtymologyTranslation]
    sp_etymology: str


class Word(BaseModel):
    id: str

    book: Book

    coined_era: CoinedEra
    coined_year: str

    creator: list[str]

    see_also: list[str]

    resources: Optional[Resources] = Resources()

    representations: Optional[Representations] = Representations()

    source_language: str

    usage_category: UsageCategory

    word: str

    deprecated: bool

    etymology: list[Etymology]

    audio: list[Audio]

    usage: dict[str, int]

    translations: dict[str, Translation]


def get_word(word: str, languages=["en"]) -> Word:
    response = httpx.get(
        f"https://api.linku.la/v1/words/{word}", params={"lang": ",".join(languages)}
    )
    response.raise_for_status()
    return Word(**response.json())
