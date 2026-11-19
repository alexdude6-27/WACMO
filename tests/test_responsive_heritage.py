from wacmo import create_app


def test_mobile_navigation_markup():
    client = create_app().test_client()
    page = client.get("/").get_data(as_text=True)

    assert 'class="menu-toggle"' in page
    assert 'aria-controls="site-navigation"' in page
    assert 'id="site-navigation"' in page
    assert 'aria-expanded="false"' in page
    assert "js/navigation.js" in page

    assert client.get(
        "/static/js/navigation.js"
    ).status_code == 200


def test_original_national_footer():
    client = create_app().test_client()
    page = client.get(
        "/what-is-cmo"
    ).get_data(as_text=True)

    assert "Riding adventures and shared memories" not in page
    assert "For ride results and more information" in page
    assert "click on the NACMO logo to go to the National website!" in page
    assert 'href="https://www.nacmo.org/"' in page
    assert "wacmo_nacmo_logo.png" in page

    assert client.get(
        "/static/images/wacmo_nacmo_logo.png"
    ).status_code == 200

    assert client.get(
        "/static/images/wacmo_wood_texture.png"
    ).status_code == 200


def test_nine_original_navigation_links():
    page = create_app().test_client().get(
        "/"
    ).get_data(as_text=True)

    nav = page.split(
        '<nav class="site-nav"', 1
    )[1].split("</nav>", 1)[0]

    assert nav.count("<a ") == 9
    assert page.count('aria-current="page"') == 1
