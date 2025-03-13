import apis.github as ghapi


def test_can_fetch_user():
    ghapi.get_user("ghost")


def test_can_fetch_repo():
    ghapi.get_repo("octocat/Spoon-Knife")


def test_repo_is_accurate():
    repo = ghapi.get_repo("octocat/Spoon-Knife")
    assert repo.full_name == "octocat/Spoon-Knife"
    assert repo.description == "This repo is for demonstration purposes only."
    assert repo.owner.login == "octocat"


def test_repo_is_case_insensitive():
    repo = ghapi.get_repo("OCTOCAT/SPOON-KNIFE")
    assert repo.full_name == "octocat/Spoon-Knife"
    assert repo.description == "This repo is for demonstration purposes only."
    assert repo.owner.login == "octocat"

    repo = ghapi.get_repo("octocat/spoon-knife")
    assert repo.full_name == "octocat/Spoon-Knife"
    assert repo.description == "This repo is for demonstration purposes only."
    assert repo.owner.login == "octocat"

    repo = ghapi.get_repo("OCTOCAT/spoon-knife")
    assert repo.full_name == "octocat/Spoon-Knife"
    assert repo.description == "This repo is for demonstration purposes only."
    assert repo.owner.login == "octocat"
