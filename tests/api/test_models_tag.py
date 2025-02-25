"""Test the Tag API."""

from unittest.mock import patch

from raindropiopy import API, Tag

TAG = {"_id": "a Sample Tag", "count": 1}


def test_get() -> None:
    """Test that we can lookup a tag."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"items": [TAG]}

        tags = Tag.get(api)

        assert len(tags) == 1

        tag = tags[0]
        assert tag.tag == "a Sample Tag"
        assert tag.count == 1
