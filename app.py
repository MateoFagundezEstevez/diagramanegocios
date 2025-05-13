import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Red de Contactos por País u Organización", layout="wide")
st.title("🔗 Red de Contactos por País u Organización")

# Leer el archivo CONTACTOS.csv directamente
try:
    df = pd.read_csv("CONTACTOS.csv")
    st.success("✅ Archivo 'CONTACTOS.csv' cargado correctamente.")

    # Crear mapa mundi centrado en el mapa global
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="Stamen Terrain")

    # Crear un marcador de agrupación
    marker_cluster = MarkerCluster().add_to(m)

    # Definir colores para los países
    pais_colores = {
        "Uruguay": "#28a745",  # Verde
        "Colombia": "#007bff",  # Azul
        "Argentina": "#ffc107",  # Amarillo
        "Brasil": "#dc3545",  # Rojo
        # Añadir más países y colores si es necesario
    }

    # Asumir que tienes coordenadas aproximadas para los países
    pais_coordenadas = {
        "Uruguay": [-32.5228, -55.7658],
        "Colombia": [4.5709, -74.2973],
        "Argentina": [-38.4161, -63.6167],
        "Brasil": [-14.2350, -51.9253],
        # Añadir más países con sus coordenadas
    }

    # Crear un grafo en PyVis
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based(gravity=-50)

    for _, row in df.iterrows():
        titulo = row["TITULO"]
        persona = row["NOMBRE"]
        pais = row["PAIS DE INTERÉS"]
        organizacion = row["Empresa u organización"]
        mail = row["MAIL"]
        telefono = row["TELÉFONO"]

        # Asignar color basado en el país
        color_pais = pais_colores.get(pais, "#6c757d")  # Gris si el país no está en el diccionario

        # Crear un nodo para cada persona en el grafo de PyVis
        net.add_node(persona, label=persona, shape="dot", color=color_pais, title=f"{titulo} {persona} - {organizacion} ({pais})")

        # Agregar los contactos al mapa mundi
        if pais in pais_coordenadas:
            lat, lon = pais_coordenadas[pais]
            folium.Marker(
                location=[lat, lon],
                popup=f"{persona}<br>{organizacion}<br>{mail}<br>{telefono}",
                icon=folium.Icon(color=color_pais)
            ).add_to(marker_cluster)

        # Crear nodos para país y organización en el grafo
        if pd.notna(pais):
            net.add_node(pais, label=pais, shape="ellipse", color=color_pais)
            net.add_edge(persona, pais)

        if pd.notna(organizacion):
            net.add_node(organizacion, label=organizacion, shape="box", color="#ffc107")
            net.add_edge(persona, organizacion)

        # Agregar el correo electrónico y teléfono al título del nodo
        if pd.notna(mail) or pd.notna(telefono):
            contact_info = f"Correo: {mail}<br>Teléfono: {telefono}"
            net.add_node(f"{persona}_contact", label="Contacto", shape="diamond", color="#6f42c1", title=contact_info)
            net.add_edge(persona, f"{persona}_contact")

    # Guardar grafo de PyVis en archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html_path = tmp_file.name

    # Incrustar el mapa y el grafo en Streamlit
    st.subheader("🌍 Mapa Mundial de Contactos")
    folium_static(m)

    st.subheader("📊 Red de Contactos")
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        components.html(html_content, height=700, scrolling=True)

    os.remove(html_path)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'CONTACTOS.csv' en el repositorio.")
except Exception as e:
    st.error(f"⚠️ Error al procesar el archivo: {e}")
