import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, fire_spots, about  # import your app modules here
import pathlib

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

apps = [
    {"func": home.app, "title": "Cámaras", "icon": "camera-fill"},
    {"func": fire_spots.app, "title": "Incendios", "icon": "map"},
    {"func": about.app, "title": "Sobre nosotros", "icon": "file-person-fill"}
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

st.sidebar.image(f"{pathlib.Path(__file__).parent.resolve()}" + "/assets/StopFire_logo_center.png", use_column_width=True)
with st.sidebar:
    selected = option_menu(
        "Menú",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

for app in apps:

    if app["title"] == selected:
        app["func"]()
        break
