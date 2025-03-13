import apis.sona as sonaapi


def test_can_get_word():
    sonaapi.get_word("toki")


def test_word_type_is_correct():
    assert type(sonaapi.get_word("toki")) is sonaapi.Word


def test_word_has_stats():
    word = sonaapi.get_word("toki")
    assert word.word == "toki"
    assert word.book == sonaapi.Book.Pu
    assert word.coined_era == sonaapi.CoinedEra.PrePu
    assert word.creator == ["jan Sonja"]
