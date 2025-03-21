"""Test all the core methods of the Raindrop API."""

from pathlib import Path

import pytest
import requests

from raindropiopy import Raindrop, RaindropType
from tests.api.conftest import vcr


@pytest.fixture
def sample_raindrop_link():
    """Fixture to return sample raindrop data."""
    return (
        "https://www.google.com/",
        {
            "excerpt": "excerpt/description text",
            "important": True,
            "tags": ["abc", "def"],
            "title": "a Title",
        },
    )


@pytest.fixture
def search_raindrops(api):
    """Fixture to setup and teardown 2 link-based raindrops for search testing."""
    link, args = (
        "https://www.google.com/",
        {
            "title": "ELGOOG 1234567890",
            "tags": ["ABCDEFG", "HIJKLMO"],
            "please_parse": True,
        },
    )
    raindrop_google = Raindrop.create_link(api, link, **args)

    link, args = (
        "https://www.python.com/",
        {
            "title": "NOHTYP 1234567890",
            "tags": ["HIJKLMO", "PQRSTUV"],
            "please_parse": True,
        },
    )
    raindrop_python = Raindrop.create_link(api, link, **args)

    # Before we let the test rip, allow time for asynchronuous indexing on Raindrop's backend to catch-up.
    import time

    time.sleep(10)

    yield

    Raindrop.delete(api, id=raindrop_google.id)
    Raindrop.delete(api, id=raindrop_python.id)


@vcr.use_cassette()
def test_lifecycle_raindrop_link(api, sample_raindrop_link) -> None:
    """Test that we can roundtrip a regular/link-based raindrop, ie. create, update, get and delete."""
    # TEST: Create
    link, args = sample_raindrop_link
    raindrop = Raindrop.create_link(api, link, **args)
    assert raindrop is not None
    assert isinstance(raindrop, Raindrop)
    assert raindrop.id
    assert raindrop.link == link
    assert raindrop.important == args.get("important")
    assert raindrop.tags == args.get("tags")
    assert raindrop.title == args.get("title")
    assert raindrop.excerpt == args.get("excerpt")
    assert raindrop.type == RaindropType.link

    # TEST: Edit...
    title = "a NEW/EDITED Title"
    edited_raindrop = Raindrop.update(api, raindrop.id, title=title)
    assert edited_raindrop.title == title

    # TEST: Delete...
    Raindrop.delete(api, id=raindrop.id)
    with pytest.raises(requests.exceptions.HTTPError):
        Raindrop.get(api, raindrop.id)


@vcr.use_cassette()
def test_lifecycle_raindrop_file(api) -> None:
    """Test that we can roundtrip a *file-base* raindrop, ie. create, update, get and delete."""
    # TEST: Create a link using this test file as the file to upload.
    path_ = Path(__file__).parent / Path("test_raindrop.pdf")

    raindrop = Raindrop.create_file(
        api,
        path_,
        "application/pdf",
        title="A Sample Title",
        tags=["SampleTag"],
    )
    assert raindrop is not None
    assert isinstance(raindrop, Raindrop)
    assert raindrop.id
    assert raindrop.file.name == path_.name
    assert raindrop.type == RaindropType.document

    # TEST: Delete...
    Raindrop.delete(api, id=raindrop.id)
    with pytest.raises(requests.exceptions.HTTPError):
        Raindrop.get(api, raindrop.id)


@vcr.use_cassette()
def test_search(api, search_raindrops) -> None:
    """Test that we can *search* raindrops."""

    def _print(results):
        links = [drop.link for drop in results]
        return ",".join(links)

    # TEST: Can we search by "word"?
    results = Raindrop.search(api, search="ELGOOG")  # Title
    assert len(results) == 1, f"Sorry, expected 1 for 'ELGOOG' but got the following {_print(results)}"

    # TEST: Can we search by "word"?
    results = Raindrop.search(api, search="ELGOOG")  # Title
    assert len(results) == 1, f"Sorry, expected 1 for 'ELGOOG' but got the following {_print(results)}"

    results = Raindrop.search(api, search="1234567890")
    assert len(results) == 2, f"Sorry, expected 2 for '1234567890' but got the following {_print(results)}"

    # TEST: Can we search by "tag"?
    results = Raindrop.search(api, search="#ABCDEFG")
    assert len(results) == 1, f"Sorry, expected 1 for tag 'ABCDEFG' but got the following {_print(results)}"

    results = Raindrop.search(api, search="#HIJKLMO")
    assert len(results) == 2, f"Sorry, expected 2 for tag 'HIJKLMO' but got the following {_print(results)}"

    # TEST: What happens if we search with NO parameters? We should get back ALL the bookmarks
    #       associated with the current test token's environment, including the test ones.
    results = Raindrop.search(api)

    # Confirm that *at least* the 2 test cases are also in the results (at least in case
    # previous tests left leftover entries)
    found = sum(map(lambda raindrop: "1234567890" in raindrop.title, results))
    assert found >= 2, "Sorry, expected to find the 2 entries we setup in the test for wildcard search but didn't!"
