"""Regression tests for Streamlit's inline-SVG sanitization behavior."""
import base64
import unittest
from pathlib import Path
from html.parser import HTMLParser

from portal_render import portal_html

PAGE = Path(__file__).resolve().parents[1] / "landing.html"


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.images.append(dict(attrs))


class PortalArtTests(unittest.TestCase):
    def test_all_inline_svg_rendered_as_image_elements(self):
        original = PAGE.read_text(encoding="utf-8")
        output = portal_html(PAGE)
        self.assertEqual(output.count("<svg"), 0)
        doc = Images()
        doc.feed(output)
        self.assertEqual(len(doc.images), original.count("<svg"))
        self.assertGreater(len(doc.images), 10)
        for img in doc.images:
            self.assertTrue(img["src"].startswith("data:image/svg+xml;base64,"))
            decoded = base64.b64decode(img["src"].split(",", 1)[1]).decode()
            self.assertIn('xmlns="http://www.w3.org/2000/svg"', decoded)
            self.assertNotIn("currentColor", decoded)
            self.assertNotIn("<script", decoded)

    def test_hero_and_two_scientific_icons_survive(self):
        doc = Images()
        doc.feed(portal_html(PAGE))
        alt = [image.get("alt") for image in doc.images]
        self.assertIn("Illustration of a well plate", alt)
        self.assertIn("Illustration of a ThT aggregation curve", alt)
        self.assertIn("Microplate icon", alt)
        self.assertIn("", alt)

    def test_original_app_links_remain_unchanged(self):
        result = portal_html(PAGE)
        self.assertIn("tht-plate-planner-qh8azentmh5onkv3wli4gz.streamlit.app/", result)
        self.assertIn("tht-aggregation-analysis-ez3ofuwmdkhuunhtcg4q6p.streamlit.app/", result)

    def test_image_css_selectors_exist(self):
        page = PAGE.read_text(encoding="utf-8")
        for selector in (
            '.prs-access img {', '.prs-hero-art img {',
            '.prs-card-illustration > img {', '.prs-cta img {',
            '.prs-resource img {',
        ):
            self.assertIn(selector, page)


if __name__ == '__main__':
    unittest.main()
