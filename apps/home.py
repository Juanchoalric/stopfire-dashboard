import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests

def app():

    st.title("Mapa de Camaras")

    st.markdown(
        """
    Un mapa donde se puede ver la ubicacion de cada camara deployada para alertar
    """
    )

    data = {
        "latitude": [-27.757737, -27.748806, -27.854678,-27.990941, -28.028142, -28.061742],
        "longitude": [-57.196302,-56.909063,-56.690196,-57.453417,-57.240926,-56.529937],
        "zones": [1, 1, 2, 3,3, 4],
        "camera_id": [1,2,3,4,5,6],
        "camera_type": ["Punto fijo", "Punto fijo", "Punto fijo", "Punto fijo", "Punto fijo", "Punto fijo"]
    }

    df = pd.DataFrame.from_dict(data)

    m = leafmap.Map(center=(-31.416668, -64.183334), zoom=5)

    m.add_points_from_xy(data=df, x='longitude', y='latitude', color_column="zones", icon_colors=["camera"])

    m.to_streamlit(height=700)
