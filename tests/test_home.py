from wacmo import create_app


def test_homepage():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"WACMO" in response.data
    assert b"Schedule of Events" in response.data
    assert b"Photo Gallery" in response.data


def test_stylesheet():
    app = create_app()
    client = app.test_client()

    response = client.get("/static/css/site.css")
    assert response.status_code == 200
