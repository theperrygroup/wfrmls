"""Validate the built documentation's metadata, sitemap, and internal links."""

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.title = []
        self.in_title = False
        self.meta = {}
        self.canonical = []
        self.ids = set()
        self.duplicate_ids = set()
        self.links = []
        self.json_data = []
        self.in_json = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.duplicate_ids.add(attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            self.meta.setdefault(attrs.get("name") or attrs.get("property"), []).append(
                attrs.get("content", "")
            )
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href", ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True
            self.json_data.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_json = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_json:
            self.json_data[-1] += data


def check(site, site_url):
    site = site.resolve()
    base = urlsplit(site_url)
    errors = []
    pages = {}
    titles = {}
    descriptions = {}
    canonicals = set()

    def fail(path, message):
        errors.append(f"{path.relative_to(site)}: {message}")

    for path in sorted(site.rglob("*.html")):
        page = Page(path)
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
        if page.duplicate_ids:
            fail(path, f"duplicate HTML IDs: {sorted(page.duplicate_ids)}")
        if path.name == "404.html":
            continue
        relative = path.relative_to(site).as_posix()
        if path.name == "index.html":
            relative = relative[: -len("index.html")]
        expected = urljoin(site_url, relative)
        if page.canonical != [expected]:
            fail(path, f"expected one canonical URL: {expected}")
        canonicals.add(expected)
        title = "".join(page.title).strip()
        if not title:
            fail(path, "missing title")
        elif title in titles:
            fail(path, f"duplicate title with {titles[title]}")
        titles[title] = path.relative_to(site)
        for key in (
            "description",
            "og:title",
            "og:description",
            "og:url",
            "og:site_name",
            "og:type",
            "twitter:card",
            "twitter:title",
            "twitter:description",
        ):
            values = page.meta.get(key, [])
            if len(values) != 1 or not values[0].strip():
                fail(path, f"expected one nonempty {key}")
        description = page.meta.get("description", [""])[0]
        if description in descriptions:
            fail(path, f"duplicate description with {descriptions[description]}")
        descriptions[description] = path.relative_to(site)
        if page.meta.get("og:url") != [expected]:
            fail(path, "Open Graph URL differs from canonical URL")
        if page.meta.get("og:description") != [description]:
            fail(path, "Open Graph description differs from page description")
        if page.meta.get("twitter:description") != [description]:
            fail(path, "Twitter description differs from page description")
        try:
            data = [json.loads(item) for item in page.json_data]
            if not any(
                item.get("@type") == "WebPage" and item.get("url") == expected
                for item in data
            ):
                fail(path, "missing matching WebPage JSON-LD")
        except (ValueError, AttributeError):
            fail(path, "invalid JSON-LD")

    for path, page in pages.items():
        relative = path.relative_to(site).as_posix()
        page_url = urljoin(site_url, relative)
        for href in page.links:
            target = urlsplit(urljoin(page_url, href))
            if target.scheme not in ("http", "https") or target.netloc != base.netloc:
                continue
            if not target.path.startswith(base.path):
                continue  # Another project on the same GitHub Pages host.
            target_path = site / unquote(target.path[len(base.path) :])
            if target_path.is_dir():
                target_path /= "index.html"
            target_path = target_path.resolve()
            if not target_path.is_relative_to(site) or not target_path.is_file():
                fail(path, f"broken internal link: {href}")
            elif target.fragment and target_path in pages:
                if unquote(target.fragment) not in pages[target_path].ids:
                    fail(path, f"missing fragment: {href}")

    try:
        sitemap = ElementTree.parse(site / "sitemap.xml")
        urls = {
            node.text
            for node in sitemap.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        }
        if urls != canonicals:
            errors.append(f"sitemap differs from canonical pages: {urls ^ canonicals}")
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f"invalid sitemap: {exc}")

    if not canonicals:
        errors.append("no documentation pages found")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        f"Validated {len(canonicals)} pages: unique metadata, JSON-LD, canonicals, "
        "sitemap, and internal links."
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--site-url", default="https://theperrygroup.github.io/wfrmls/")
    args = parser.parse_args()
    sys.exit(check(args.site, args.site_url))
