import streamlit as st


def app():
    title = "<h1>Quienes somos</h1>"
    somos = "<h2>Somos StopFire y venimos a parar el fuego.</h2>"
    autores = "<h2>Autores:</h2>"
    text_1 = "<h5>Somos estudiantes de ingeniería en informática de la Universidad Argentina de la Empresa (UADE) quienes de la mano del Instituto de Tecnología (INTEC) queremos contribuir con aplicaciones de machine learning para el uso sustentable de recursos naturales.</h5>"
    text_2 = "<h5>StopFire busca combinar internet de las cosas (IoT) con machine learning para analizar imágenes en tiempo real y determinar la existencia de un potencial incendio forestal, alertando así a las jurisdicciones encargadas de actuar de manera inmediata sobre el foco apenas se inicia el fuego.</h5>"
    text_3 = "<h5>Nuestra tesis se integra al proyecto de investigación del INTEC de la UADE llamado “A21T03 – Aplicaciones de Machine Learning para mejorar el uso de Recursos Naturales” y que es liderado por el Mg. Pablo Inchausti. A su vez, es continuación del Proyecto Final de Ingeniería (PFI) “AQUA: Desarrollo de un modelo de machine learning para prevenir incendios forestales en Pinamar” desarrollado por la Ing. Ana Martínez Saucedo.</h5>"
    text_4 = "<h5>Fue presentado el 6 de octubre de 2022 en la XXVIII edición del Congreso Argentino de Ciencias de la Computación (CACIC) dentro de la categoría de short paper(artículos breves). ISBN = por asignar.</h5>"

    st.markdown(title,  unsafe_allow_html=True)

    st.markdown(somos,  unsafe_allow_html=True)

    st.markdown("")

    st.markdown(text_1,  unsafe_allow_html=True)
    st.markdown(text_2,  unsafe_allow_html=True)
    st.markdown(text_3,  unsafe_allow_html=True)
    st.markdown(text_4,  unsafe_allow_html=True)

    st.markdown(autores,  unsafe_allow_html=True)

    st.write("ALRIC, Juan Cruz")

    st.write("CURBELO, Alejandra")