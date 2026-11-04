"""Checks for the public portal: no secrets or dormant CTA links."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'landing.html').read_text(encoding='utf-8')
APP = (ROOT / 'app.py').read_text(encoding='utf-8')

class LandingPageTests(unittest.TestCase):
    def test_navigation_destinations(self):
        self.assertIn('https://tht-plate-planner-qh8azentmh5onkv3wli4gz.streamlit.app/', HTML)
        self.assertIn('https://tht-aggregation-analysis-ez3ofuwmdkhuunhtcg4q6p.streamlit.app/', HTML)

    def test_brand(self):
        self.assertIn('Plate Reader Suite', HTML)
        self.assertIn('Beck–Barkai Lab', HTML)

    def test_public_no_authentication(self):
        self.assertNotIn('LAB_ACCESS_PASSWORD', APP + HTML)
        self.assertNotIn('LAB_GITHUB_TOKEN', APP + HTML)
        self.assertNotIn('st.secrets', APP)

    def test_all_internal_links_target_sections(self):
        targets = set(re.findall(r'id="([a-z-]+)"', HTML))
        anchors = set(re.findall(r'href="#([a-z-]+)"', HTML))
        self.assertTrue(anchors <= targets, anchors - targets)

    def test_links_open_apps_in_new_tabs_safely(self):
        for match in re.finditer(r'<a\b([^>]*href="https://[^"]+"[^>]*)>', HTML):
            self.assertIn('target="_blank"', match.group(1))
            self.assertIn('rel="noopener noreferrer"', match.group(1))

    def test_responsive_and_motion(self):
        self.assertIn('@media (max-width: 900px)', HTML)
        self.assertIn('prefers-reduced-motion', HTML)

    def test_no_javascript_required(self):
        self.assertNotIn('<script', HTML.lower())

if __name__ == '__main__':
    unittest.main()
