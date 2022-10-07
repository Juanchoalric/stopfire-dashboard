import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, fire_spots  # import your app modules here
import pathlib

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": fire_spots.app, "title": "Fire", "icon": "map"}
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

st.sidebar.image(f"{pathlib.Path(__file__).parent.resolve()}" + "/assets/StopFire_logo.png", use_column_width=True)
with st.sidebar:
    selected = option_menu(
        "StopFire",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
