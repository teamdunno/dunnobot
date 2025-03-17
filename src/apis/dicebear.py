from enum import Enum


class Style(Enum):
    Adventurer = "adventurer"
    AdventurerNeutral = "adventurer-neutral"
    Avataaars = "avataaars"
    AvataaarsNeutral = "avataaars-neutral"
    BigEars = "big-ears"
    BigEarsNeutral = "big-ears-neutral"
    BigSmile = "big-smile"
    Bottts = "bottts"
    BotttsNeutral = "bottts-neutral"
    Croodles = "croodles"
    CroodlesNeutral = "croodles-neutral"
    Dylan = "dylan"
    FunEmoji = "fun-emoji"
    Glass = "glass"
    Icons = "icons"
    Identicon = "identicon"
    Initials = "initials"
    Lorelei = "lorelei"
    LoreleiNeutral = "lorelei-neutral"
    Micah = "micah"
    Miniavs = "miniavs"
    Notionists = "notionists"
    NotionistsNeutral = "notionists-neutral"
    OpenPeeps = "open-peeps"
    Personas = "personas"
    PixelArt = "pixel-art"
    PixelArtNeutral = "pixel-art-neutral"
    Rings = "rings"
    Shapes = "shapes"
    Thumbs = "thumbs"


ALL_STYLES = [style.value for style in Style]


def get_avatar_url(style: Style, seed: str, **kwargs) -> str:
    url = f"https://api.dicebear.com/9.x/{style.value}/png?seed={seed}"

    for k, v in kwargs.items():
        url += f"&{k}={v}"

    return url
