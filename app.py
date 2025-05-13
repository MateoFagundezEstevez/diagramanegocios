import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Red de Contactos", layout="wide")
st.title("🔗 Red de Contactos por País u Organización")

# Cargar el archivo de contactos
uploaded_file = st.file_uploader("📤 Subí tu archivo CSV con los contactos", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ Archivo cargado correctamente.")

    # Crear el grafo con Pyvis
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")

    net.force_atlas_2based(gravity=-50)  # Para una distribución más natural

    # Crear nodos y edges
    contactos = df["Nombre"].fillna("Sin nombre")
    organizaciones = df["Organización"].fillna("Sin organización")
    paises = df["País de interés"].fillna("Desconocido")

    for i, row in df.iterrows():
        persona = row["Nombre"]
        pais = row["País de interés"]
        organizacion = row["Organización"]

        net.add_node(persona, label=persona, shape="dot", color="#007bff", title=f"{organizacion} ({pais})")

        if pd.notna(pais):
            net.add_node(pais, label=pais, shape="ellipse", color="#28a745")
            net.add_edge(persona, pais)

        if pd.notna(organizacion):
            net.add_node(organizacion, label=organizacion, shape="box", color="#ffc107")
            net.add_edge(persona, organizacion)

    # Guardar HTML temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html_path = tmp_file.name

    # Mostrar el grafo en Streamlit
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        components.html(html_content, height=700, scrolling=True)

    # Eliminar archivo temporal
    os.remove(html_path)

else:
    st.info("📁 Esperando que subas un archivo CSV con columnas como: Nombre, Organización, País de interés.")
