"""Render trusted portal SVG artwork as images for Streamlit's HTML sanitizer.

Streamlit st.html uses DOMPurify, which can remove inline SVG elements.
The checked-in SVG artwork is embedded as SVG images rather than inline nodes.
"""
from __future__ import annotations

import base64
import html
import re
from pathlib import Path

_SVG = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL)
_ATTR = re.compile(r'\b([\w-]+)="([^"]*)"')


def _resolve_ink(markup: str, start: int, attrs: dict[str, str]) -> str:
    """Bake inherited CSS colors into self-contained SVG image assets."""
    prefix = markup[:start]
    cls = attrs.get("class", "")
    if "check" in cls.split():
        latest_planner = prefix.rfind('<article class="prs-card planner"')
        latest_analysis = prefix.rfind('<article class="prs-card analysis"')
        return "#227e7a" if latest_planner > latest_analysis else "#7945a0"
    if prefix.rfind('class="prs-cta"') > prefix.rfind('</a>'):
        return "#ffffff"
    if prefix.rfind('class="prs-access"') > prefix.rfind('</a>'):
        return "#ffffff"
    return "#13283d"


def svg_images_for_streamlit(markup: str) -> str:
    """Convert only the project's static inline SVGs into ordinary images."""
    def replace(match: re.Match[str]) -> str:
        svg = match.group(0)
        attrs = dict(_ATTR.findall(svg.split(">", 1)[0]))
        svg = svg.replace("currentColor", _resolve_ink(markup, match.start(), attrs))
        prefix = markup[:match.start()]
        # Resource icons inherited fill:none and stroke from outside CSS.
        # Standalone SVG image assets must carry these properties themselves.
        if prefix.rfind('class="prs-resource"') > prefix.rfind('</a>'):
            svg = svg.replace(
                "<svg", '<svg fill="none" stroke="#13283d" stroke-width="1.8" '
                'stroke-linecap="round" stroke-linejoin="round"', 1
            )
        if "xmlns=" not in svg.split(">", 1)[0]:
            svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        cls = html.escape(attrs.get("class", ""), quote=True)
        alt = html.escape(attrs.get("aria-label", ""), quote=True)
        return (f'<img class="{cls}" alt="{alt}" decoding="async" '
                f'src="data:image/svg+xml;base64,{encoded}" />')

    return _SVG.sub(replace, markup)


def portal_html(path: Path) -> str:
    """Extract page content and convert artwork to sanitizer-safe images."""
    page = path.read_text(encoding="utf-8")
    css = page.split("<style>", 1)[1].split("</style>", 1)[0]
    markup = page.split('<div class="prs-shell"', 1)[1].split("</body>", 1)[0]
    return "<style>" + css + "</style>\n<div class=\"prs-shell\"" + svg_images_for_streamlit(markup)
