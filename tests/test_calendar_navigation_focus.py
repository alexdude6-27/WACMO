"""Keep the calendar in view when changing months."""

from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

from wacmo import create_app


class CalendarLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return

        attrs = dict(attrs)

        if "calendar-nav-button" in (
            attrs.get("class", "").split()
        ):
            self.links.append(attrs["href"])


def test_month_navigation_returns_to_calendar():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get(
        "/events?year=2026&month=11"
    )

    assert response.status_code == 200

    html = response.get_data(as_text=True)

    assert (
        'id="calendar-month" tabindex="-1"'
        in html
    )

    parser = CalendarLinks()
    parser.feed(html)

    assert len(parser.links) == 2

    months = set()

    for href in parser.links:
        parts = urlsplit(href)

        assert parts.path == "/events"
        assert parts.fragment == "calendar-month"

        query = parse_qs(parts.query)
        assert query["year"] == ["2026"]

        months.add(query["month"][0])

        page = client.get(
            parts.path + "?" + parts.query
        )

        assert page.status_code == 200

    assert months == {"10", "12"}
