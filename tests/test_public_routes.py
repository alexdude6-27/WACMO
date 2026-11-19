import pytest

from wacmo import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize(
    ("path", "title"),
    [
        ("/", "Adventure starts with a direction."),
        ("/events", "Event Calendar"),
        ("/ride-flyers", "Ride Flyers"),
        ("/galleries", "Photo Galleries"),
        ("/riding-areas", "Riding Areas"),
        ("/about", "About WACMO"),
    ],
)
def test_public_pages(client, path, title):
    response = client.get(path)
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert title in body
    assert 'aria-current="page"' in body
    assert body.count('aria-current="page"') == 1


def test_home_navigation(client):
    body = client.get("/").get_data(as_text=True)

    for path in (
        "/events",
        "/ride-flyers",
        "/galleries",
        "/riding-areas",
        "/about",
    ):
        assert f'href="{path}"' in body


def test_unknown_public_page(client):
    response = client.get("/not-a-page")
    assert response.status_code == 404
