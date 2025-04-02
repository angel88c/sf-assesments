import streamlit as st
from PIL import Image

def set_global_styles():
    st.markdown("""
        <style>           
            /* Cambiar el fondo de la página */
            body {
                background-color: #f0faf9 !important; /* Color gris claro */
            }

            /* Opcional: cambiar el color de fondo del contenedor principal */
            [data-testid="stAppViewContainer"] {
                background-color: #f0faf9 !important;
            }

            /* Asegurar que los formularios mantengan su color por defecto */
            div[data-testid="stForm"] {
                background-color: white !important;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
            
            div[data-testid="stForm"] button {
                background-color: #16337d !important; /* Naranja */
                color: white !important;
                border-radius: 5px;
                border: 2px solid #16337d;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            
                height: 30px;
            }

            /* Efecto hover para el botón */
            div[data-testid="stForm"] button:hover {
                background-color: #00072d !important; /* Color más oscuro al pasar el mouse */
                border-color: #00072d;
            }
        </style>
    """, unsafe_allow_html=True)


def load_ibtest_logo():
    logo = Image.open("logo_ibtest.png")
    st.image(logo, width=150)
