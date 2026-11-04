"""Public landing page for the Beck–Barkai Lab Plate Reader Suite.

The two scientific applications run independently; no credentials, files,
experiments, or session state are handled by this portal.
"""
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Plate Reader Suite | Beck–Barkai Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Beck–Barkai Lab | Plate Reader Suite"},
)

# st.html embeds a sanitized HTML *fragment* in Streamlit's existing document.
# Keep landing.html as a complete standalone HTML document for visual review,
# but pass only its <style> and page markup to avoid nested <html>/<body> tags.
page = Path(__file__).with_name("landing.html").read_text(encoding="utf-8")
css = page.split("<style>", 1)[1].split("</style>", 1)[0]
markup = page.split('<div class="prs-shell"', 1)[1].split("</body>", 1)[0]
st.html("<style>" + css + "</style>\n<div class=\"prs-shell\"" + markup)
