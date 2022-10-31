from itertools import zip_longest
from matplotlib.pyplot import xlabel
import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import datetime
import requests
from datetime import timedelta
import pathlib
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components


def send_false_positive(key):
    params = {"key": key}
    requests.put("http://54.207.31.1:5000/alert/", params=params)

def get_data_from_service():
    result = requests.get(url="http://54.207.31.1:5000/alerts")
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

def app():

    st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

    try:
        flag = 1
        df = get_data_from_service()
    except:
        st.title("Estamos trabajando para resolver el problema :)")
        st.image(f"{pathlib.Path(__file__).parent.parent}" + "/assets/StopFire_logo_center.png")
        flag = 2
    if flag == 1:

        st.title("Reporte de incendios")

        df["taken_at"] = pd.to_datetime(df["taken_at"])
        df["date"] = pd.to_datetime(df["taken_at"]).dt.date
        df["month"] = df["date"].apply(lambda x: str(x.year) + "-" + str(x.month))
        col1, col2 = st.columns(2)
        with col1:
            start_filter = st.date_input("Fecha de inicio: ", datetime.datetime.now() - timedelta(90))
        with col2:
            end_filter = st.date_input("Fecha de fin: ", datetime.datetime.now())
        if start_filter:
            df = df[df["date"] >= start_filter]
        if end_filter:
            df = df[df["date"] <= end_filter]
        if start_filter and end_filter:
            df = df[(df["date"] >= start_filter) & (df["date"] <= end_filter)]
        
        zones = df["zone"].unique()
        zones = list(zones)
        zones.append("Todo")

        col1, col2 = st.columns(2)

        with col1:
            zone = st.radio("Elegí una zona: ", list(reversed(zones)))

            if zone:
                if zone != "Todo":
                    df = df[df["zone"] == zone]

            camera_types = df["camera_type"].unique()

            camera_types = list(camera_types)
            camera_types.append("Todo")

        with col2:
            camera_type = st.radio("Elegí una cámara: ", list(reversed(camera_types)))

            if camera_type:
                if camera_type != "Todo":
                    df = df[df["camera_type"] == camera_type]
        

        col1, col2 = st.columns(2)


        with col1:
            st.dataframe(df[["taken_at", "latitude", "longitude", "zone","id_camera", "camera_type", "image"]].sort_values(by="taken_at", ascending=False).rename(
                columns={"taken_at": "Fecha de captura", "latitude": "Latitud", "longitude": "Longitud", "zone": "Zona", "id_camera": "ID de cámara", "camera_type": "Tipo de cámara", "image": "Imagen"}))
        df["image_html"] = df.image.apply(lambda x:"<img src='" + x + "' width=200/>") # Modify the link into HTML code

        with col2:
            df_zones = df.groupby("zone").count().rename(columns={"longitude": "Incendios"})
            st.bar_chart(data=df_zones, x=list(df_zones.index), y="Incendios")

        m = leafmap.Map(center=(-31.416668, -64.183334), zoom=5)

        m.add_points_from_xy(data=df, x='longitude', y='latitude', color_column="month", icon_colors=["fire"], popup=["image_html"])

        m.to_streamlit(height=700)

        df.columns.value_counts()
        
        col1, col2, col4, col5= st.columns(4)
        
        with col1:
            st.subheader("Fecha de captura")
        with col2:
            st.subheader("Lat, Long & Cámara")
        with col4:
            st.subheader("Imagen")
        with col5:
            st.subheader("Falso incendio")

        df.sort_values(by="taken_at", ascending=False, inplace=True)

        for i in df.iterrows():
            with st.container():
                col1, col2, col4, col5 = st.columns(4)
                taken_at = i[1][3]
                image = i[1][5]
                with col1:
                    st.write(f"{taken_at}")
                with col2:
                    st.write(f"({i[1][1]}, {i[1][0]})")
                    st.write(f"Cámara: {i[1][6]}")
                with col4:
                    st.image(image, width = 200)
                with col5:
                    button = st.button("No es un incendio", key=i[1][2])
                    if button:
                        send_false_positive(key=i[1][2])