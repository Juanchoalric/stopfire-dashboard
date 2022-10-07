import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import datetime
import requests
from datetime import timedelta

def send_false_positive(key):
    params = {"key": key}
    requests.put("http://127.0.0.1:5000/alert/", params=params)

def app():

    result = requests.get(url="http://127.0.0.1:5000/alerts")
    
    data = result.json()["data"]

    fires = {
        "longitude": [],
        "latitude": [],
        "key": [],
        "taken_at": [],
        "zone": [],
        "image": [],
        "camera_type": []
    }

    for i in data:
        fires["key"].append(i["key"])
        fires["longitude"].append(i["longitude"])
        fires["latitude"].append(i["latitude"])
        fires["taken_at"].append(i["taken_at"])
        fires["zone"].append(i["zone"])
        fires["image"].append(i["image"])
        fires["camera_type"].append(i["camera_type"])
    
    df = pd.DataFrame.from_dict(fires)

    st.title("Fire Spots")

    df["taken_at"] = pd.to_datetime(df["taken_at"])
    df["date"] = pd.to_datetime(df["taken_at"]).dt.date
    df["month"] = df["date"].apply(lambda x: str(x.year) + "-" + str(x.month))
    start_filter = st.date_input("Dia de incio: ", datetime.datetime.now() - timedelta(90))
    end_filter = st.date_input("Dia de fin: ", datetime.datetime.now())
    if start_filter:
        df = df[df["date"] > start_filter]
    if end_filter:
        df = df[df["date"] < end_filter]
    if start_filter and end_filter:
        df = df[(df["date"] > start_filter) & (df["date"] < end_filter)]
    
    zones = df["zone"].unique()
    zones = list(zones)
    zones.append("All")

    zone = st.radio("Elegi una zona: ", list(reversed(zones)))
    
    if zone:
        if zone != "All":
            df = df[df["zone"] == zone]

    camera_types = df["camera_type"].unique()

    camera_types = list(camera_types)
    camera_types.append("All")

    camera_type = st.radio("Elegi una camara: ", list(reversed(camera_types)))


    if camera_type:
        if camera_type != "All":
            df = df[df["camera_type"] == camera_type]

    st.dataframe(df[["taken_at", "latitude", "longitude", "zone", "camera_type", "image"]].sort_values(by="taken_at", ascending=False))

    m = leafmap.Map(center=(-31.416668, -64.183334), zoom=5)
   #m.add_circle_markers_from_xy(
   #     df, 
   #     x="longitude", 
   #     y="latitude", 
   #     popup=["latitude", "longitude", "image", "taken_at", "zone"])

    m.add_points_from_xy(data=df, x='longitude', y='latitude', color_column="month", icon_colors=["fire"])

    m.to_streamlit(height=700)

    df.columns.value_counts()
    
    col1, col2, col4, col5= st.columns(4)
    
    with col1:
        st.subheader("Horario Tomada")
    with col2:
        st.subheader("Lat, Long & Camara")
    with col4:
        st.subheader("Imagen")
    with col5:
        st.subheader("Flag falso incendio")

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
                st.write(f"Camera: {i[1][6]}")
            with col4:
                st.image(image, width = 200)
            with col5:
                 button = st.button("No es un incendio", key=i[1][2])
                 if button:
                    send_false_positive(key=i[1][2])         