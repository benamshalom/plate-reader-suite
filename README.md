# Plate Reader Suite

A public, responsive home page for the **Beck–Barkai Lab** plate-reader applications. It closely follows the approved visual concept: dark navy top bar, translucent wave / plate artwork, teal Planner card, purple ThT Analysis card, and a compact resource footer.

## Applications

- [Plate Planner](https://tht-plate-planner-qh8azentmh5onkv3wli4gz.streamlit.app/)
- [ThT Analysis](https://tht-aggregation-analysis-ez3ofuwmdkhuunhtcg4q6p.streamlit.app/)

The portal **does not authenticate**, persist lab data, or share user sessions. Each application remains independently protected and maintained. All buttons are real links; auxiliary footer links show real informational sections within the portal.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy via Streamlit Community Cloud

1. Push the files to a GitHub repository (suggested name: `plate-reader-suite`).
2. In [share.streamlit.io](https://share.streamlit.io/), choose **Create app** → **Deploy a public app from GitHub**.
3. Select your repository, branch `main`, and entry point `app.py`.
4. Under advanced settings, use **Python 3.12**. Leave Secrets empty: this is a public landing page.
5. Deploy and test both "Open" buttons from desktop and mobile. If the applications sleep, the user may briefly see Streamlit's normal wake-up spinner.

The home page itself requires no secrets, tokens, GitHub data repository, or extra package beyond Streamlit. Do not move any scientific logic into this repo.

## Testing

```bash
python -m unittest discover -s tests -v
```

`landing.html` is static, containing all CSS and SVG artwork. It is embedded with `st.html` and can be previewed independently in a browser. No JavaScript is required.

## Editing

- Change destinations in `landing.html` (two external URLs).
- Change text, palette, or responsive layout in `landing.html`.
- Do not replace the two independent apps with iframes. This portal only navigates to them.