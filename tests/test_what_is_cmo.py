from wacmo import create_app


def test_what_is_cmo_original_introduction():
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get("/what-is-cmo")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "The letters C.M.O. stand for" in body
    assert "Competitive Mounted Orienteering." in body
    assert "year-end placing and lifetime points" in body
    assert "orient your self on a provided" in body
    assert "Both CMO and Endurance are fast-paced" in body
    assert "two to four hours." in body
    assert 'aria-current="page"' in body
    assert "More adventures ahead" not in body


def test_what_is_cmo_assets():
    app = create_app()
    client = app.test_client()

    body = client.get(
        "/what-is-cmo"
    ).get_data(as_text=True)

    assert "cmo-map-preview.png" in body
    assert "Illustrative CMO map" in body

    assert client.get(
        "/static/images/cmo-map-preview.png"
    ).status_code == 200

    assert client.get(
        "/static/fonts/Rye-Regular.ttf"
    ).status_code == 200

    assert client.get(
        "/static/css/site.css"
    ).status_code == 200
