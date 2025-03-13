import apis.xkcd as xkcdapi


def test_can_fetch():
    xkcdapi.get_comic(353)


def test_is_comic():
    assert type(xkcdapi.get_comic(353)) is xkcdapi.Comic


def test_comic_has_stats():
    comic = xkcdapi.get_comic(353)
    assert comic.num == 353
    assert comic.title == "Python"
