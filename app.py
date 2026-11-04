"""Public Plate Reader Suite portal for the Beck–Barkai Lab.

The two scientific applications run independently. This landing page has no
login, experimental data access, or laboratory credentials.
"""
from pathlib import Path

import streamlit as st

from portal_render import portal_html

st.set_page_config(
    page_title="Plate Reader Suite | Beck–Barkai Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Beck–Barkai Lab | Plate Reader Suite"},
)

st.html(portal_html(Path(__file__).with_name("landing.html")))
