import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Red de Contactos", layout="wide")
st.title("🔗 Red de Contactos por País u Organización")

# Leer el archivo CONTACTOS.csv directamente
try:
    df = pd.read_csv("CONTACTOS.csv")
    st.success("✅ Archivo 'CONTACTOS.csv' cargado correctamente.")

    # Crear grafo
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based(gravity=-50)

    for _, row in df.iterrows():
        titulo = row["TITULO"]
        persona = row["NOMBRE"]
        pais = row["PAIS DE INTERÉS"]
        organizacion = row["Empresa u organización"]
        mail = row["MAIL"]
        telefono = row["TELÉFONO"]
        
        # Crear nodos para cada contacto
        net.add_node(persona, label=persona, shape="dot", color="#007bff", title=f"{titulo} {persona} - {organizacion} ({pais})")

        # Añadir nodo para país
        if pd.notna(pais):
            net.add_node(pais, label=pais, shape="ellipse", color="#28a745")
            net.add_edge(persona, pais)

        # Añadir nodo para organización
        if pd.notna(organizacion):
            net.add_node(organizacion, label=organizacion, shape="box", color="#ffc107")
            net.add_edge(persona, organizacion)

        # Si deseas añadir interacciones adicionales con el mail o teléfono, puedes hacerlo aquí.
        # Ejemplo: Agregar el correo electrónico y el teléfono al título del nodo
        if pd.notna(mail) or pd.notna(telefono):
            contact_info = f"Correo: {mail}<br>Teléfono: {telefono}"
            net.add_node(f"{persona}_contact", label="Contacto", shape="diamond", color="#6f42c1", title=contact_info)
            net.add_edge(persona, f"{persona}_contact")

    # Guardar grafo en archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html_path = tmp_file.name

    # Incrustar HTML en Streamlit
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        components.html(html_content, height=700, scrolling=True)

    os.remove(html_path)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'CONTACTOS.csv' en el repositorio.")
except Exception as e:
    st.error(f"⚠️ Error al procesar el archivo: {e}")
