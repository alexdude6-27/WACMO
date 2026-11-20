from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import pytest

from wacmo import create_app


ROOT = Path(__file__).resolve().parents[1]

PAGES = (
    ("flyers", "/ride-flyers",
     "https://www.wacmo.org/flyers-rides--invites/"),
    ("photo-gallery", "/galleries",
     "https://www.wacmo.org/photo-gallery/"),
)


class ArticleReader(HTMLParser):
    def __init__(self, target):
        super().__init__(convert_charrefs=True)
        self.target = target
        self.depth = 0
        self.found = 0
        self.text_parts = []
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if not self.depth:
            if (
                tag == "div"
                and self.target in
                attrs.get("class", "").split()
            ):
                self.depth = 1
                self.found += 1
            return

        if tag == "div":
            self.depth += 1
        elif tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        elif tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text_parts.append(data)

    @property
    def text(self):
        return " ".join(
            " ".join(self.text_parts).split()
        )


@pytest.mark.parametrize("slug,route,base_url", PAGES)
def test_original_article_preserved(slug, route, base_url):
    archive = (
        ROOT / "reference/original-site" /
        f"{slug}.html"
    )

    original = ArticleReader("article-content")
    original.feed(archive.read_text())

    client = create_app().test_client()
    response = client.get(route)

    assert response.status_code == 200

    migrated = ArticleReader("heritage-article-body")
    migrated.feed(response.get_data(as_text=True))

    assert original.found == 1
    assert migrated.found == 1

    if slug == "photo-gallery":
        assert original.text == ""
        assert len(original.images) == 12
        assert len(original.links) == 12
    else:
        assert original.text

    assert original.text == migrated.text

    assert [
        urljoin(base_url, link)
        for link in original.links
    ] == migrated.links

    assert [
        urljoin(base_url, image)
        for image in original.images
    ] == migrated.images
