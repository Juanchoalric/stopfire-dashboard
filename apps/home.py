import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import pathlib
from datetime import timedelta, datetime
from streamlit_autorefresh import st_autorefresh

def get_fires_from_service():
    result = requests.get(url="http://18.230.61.125:5000/alerts")
    data = result.json()["data"]

    fires = {
        "longitude": [],
        "latitude": [],
        "key": [],
        "taken_at": [],
        "zone": [],
        "image": [],
        "camera_type": [],
        "id_camera": []
    }

    for i in data:
        fires["key"].append(i["key"])
        fires["longitude"].append(i["longitude"])
        fires["latitude"].append(i["latitude"])
        fires["taken_at"].append(i["taken_at"])
        fires["zone"].append(i["zone"])
        fires["image"].append(i["image"])
        fires["camera_type"].append(i["camera_type"])
        fires["id_camera"].append(i["id_camera"])
    
    return pd.DataFrame.from_dict(fires)

def get_cameras_from_service():
    result = requests.get(url="http://18.230.61.125:5000/cameras")
    data = result.json()["data"]

    cameras = {
        "longitude": [],
        "latitude": [],
        "zone": [],
        "camera_type": [],
        "id_camera": []
    }

    for i in data:
        cameras["longitude"].append(i["longitude"])
        cameras["latitude"].append(i["latitude"])
        cameras["zone"].append(i["zone"])
        cameras["camera_type"].append(i["camera_type"])
        cameras["id_camera"].append(i["id_camera"])

    return pd.DataFrame.from_dict(cameras)

def app():

    st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh2")

    st.title("Mapa de cámaras")

    st.markdown(
        """
    Mapa donde se puede ver la ubicación de cada cámara instalada en la zona que pertenece a la red de dispositivos
    """
    )

    try:
        flag = 1
        df_fires = get_fires_from_service()
        df_fires["taken_at"] = pd.to_datetime(df_fires["taken_at"])
        df = get_cameras_from_service()

        m = leafmap.Map(center=(-31.416668, -64.183334), zoom=5)

        m.add_points_from_xy(data=df, x='longitude', y='latitude', color_column="zone", icon_names=["camera"])

        m.to_streamlit(height=700)

    except:
        st.title("Estamos trabajando para resolver el problema :)")
        st.image(f"{pathlib.Path(__file__).parent.parent}" + "/assets/StopFire_logo_center.png")
        flag = 2
    if flag == 1:

        fires_in_zones_less_24_hs = df_fires[df_fires["taken_at"] >= (datetime.now() - timedelta(days=1))].shape[0]
        cameras_in_zone = len(df["id_camera"])

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#7323B4;" /> """, unsafe_allow_html=True)


        col1, col2 = st.columns(2)

        #st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#cccccc;" /> """, unsafe_allow_html=True)
        
        with col1:
            text_1 = f"<h5>Incendios detectados últimas 24 hs: {fires_in_zones_less_24_hs}</h5>"
            st.markdown(text_1, unsafe_allow_html=True)

        with col2:
            text_1 = f"<h5>Numero de cámaras: {cameras_in_zone}</h5>"
            st.markdown(text_1, unsafe_allow_html=True)

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#4881DB;" /> """, unsafe_allow_html=True)

