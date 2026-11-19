from html import unescape

import pytest

from wacmo import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_original_navigation_order(client):
    response = client.get("/")
    body = unescape(response.get_data(as_text=True))

    nav = body.split(
        '<nav class="site-nav"', 1
    )[1].split("</nav>", 1)[0]

    labels = (
        "Home",
        "What is CMO?",
        "CMO History",
        "Schedule of Events",
        "Flyers (Rides & Invites)",
        "Photo Gallery",
        "Maps",
        "Forms",
        "Links",
    )

    positions = [nav.index(label) for label in labels]
    assert positions == sorted(positions)
    assert nav.count("<a ") == 9


def test_original_home_content(client):
    response = client.get("/")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "WELCOME TO OUR 2026 SEASON!" in body
    assert "Our next ride is Oct 10th" in body
    assert "The Ultimate Horseback Scavenger Hunt!" in body
    assert "Your WACMO Board" in body
    assert "wacmoforms@gmail.com" in body
    assert "Historical homepage wording" in body


@pytest.mark.parametrize(
    "path",
    (
        "/what-is-cmo",
        "/cmo-history",
        "/forms",
        "/links",
        "/about",
    ),
)
def test_additional_pages(client, path):
    assert client.get(path).status_code == 200


def test_original_fir_asset(client):
    response = client.get(
        "/static/images/douglas-fir-ridge.svg"
    )

    assert response.status_code == 200
    assert b"<svg" in response.data
