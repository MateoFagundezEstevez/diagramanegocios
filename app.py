import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Red de Contactos", layout="wide")
st.title("🔗 Red de Contactos por País u Organización")

# Cargar el archivo directamente del repositorio
try:
    df = pd.read_csv("contactos.csv")
    st.success("✅ Archivo 'contactos.csv' cargado correctamente.")

    # Crear grafo
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based(gravity=-50)

    for _, row in df.iterrows():
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

    # Guardar HTML temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html_path = tmp_file.name

    # Mostrar grafo en Streamlit
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        components.html(html_content, height=700, scrolling=True)

    os.remove(html_path)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'contactos.csv' en el repositorio.")
except Exception as e:
    st.error(f"⚠️ Error al procesar el archivo: {e}")
