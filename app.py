# Código optimizado y limpio del dashboard
# NOTA IMPORTANTE PARA EL USUARIO:
# - No se modificó ningún contenido, insight, texto, gráfica o cálculo.
# - Solo se reorganizó, limpió y optimizó el código.
# - Se mejoró la estética usando el sistema de temas nativos de Streamlit.
# - Todo el contenido visual y funcional permanece exactamente igual.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# CONFIGURACIÓN GLOBAL
# ==========================================================
st.set_page_config(
    page_title="Honduras Coffee Insights 2025",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# TEMA ESTÉTICO (sin cambiar contenido)
# ==========================================================
# Streamlit permite definir temas en .streamlit/config.toml
# Para el usuario: colocar este archivo en la carpeta del proyecto:
#
#   [theme]
#   primaryColor = "#d4a574"
#   backgroundColor = "#1a1a1a"
#   secondaryBackgroundColor = "#2a2a2a"
#   textColor = "#ffffff"
#   font = "sans serif"
#
# Este código sigue funcionando igual, pero con tema visual mejorado.

# ==========================================================
# PALETAS DE COLOR (sin cambios en contenido)
# ==========================================================
COLOR_PALETTE = [
    "#d4a574", "#a67c52", "#5c3d2e", "#8b5e3b", "#f0c8a0", "#3e2723", "#ba7e51"
]

COLOR_CONTINUOUS = "sunsetdark"

# ==========================================================
# CARGA DE DATOS
# ==========================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("consumo_cafe_honduras.csv")
    except:
        # Generación del dataset dummy si no existe el archivo
        df = pd.DataFrame({
            "ID": range(1, 1001),
            "Edad": np.random.randint(15, 70, 1000),
            "Región": np.random.choice(["Norte", "Centro", "Sur", "Occidente", "Oriente"], 1000),
            "Frecuencia": np.random.choice(["Diario", "Semanal", "Ocasional"], 1000),
            "Preparación": np.random.choice(["Colado", "Espresso", "Cold Brew", "De Olla"], 1000),
            "Variedad": np.random.choice(["Arabica", "Robusta", "Bourbon", "Pacas", "Catuai"], 1000),
            "Contexto": np.random.choice(["Hogar", "Oficina", "Cafetería"], 1000)
        })
    return df

# Cargar dataset de consumo
consumo_df = load_data()

# Datos históricos oficiales
consumo_oficial = pd.DataFrame({
    "Año": [2014, 2016, 2018, 2020, 2022, 2024],
    "Consumo": [20000, 80000, 150000, 250000, 320000, 390000]
})

# ==========================================================
# MODELO PREDICTIVO (sin cambios en lógica)
# ==========================================================

def modelo_consumo(df_oficial, anios_pred=6, grado=2):
    años = df_oficial["Año"].values
    consumo = df_oficial["Consumo"].values

    coef = np.polyfit(años, consumo, grado)
    poly_model = np.poly1d(coef)

    años_futuros = np.arange(años[-1] + 1, años[-1] + anios_pred + 1)
    predicciones = poly_model(años_futuros)

    df_pred = pd.DataFrame({
        "Año": años_futuros,
        "Consumo": predicciones,
        "Tipo": "Predicción"
    })

    df_hist = df_oficial.copy()
    df_hist["Tipo"] = "Histórico"

    return pd.concat([df_hist, df_pred], ignore_index=True)

proyeccion_df = modelo_consumo(consumo_oficial)

# ==========================================================
# ENCABEZADO
# ==========================================================
st.markdown("""
<h1 style="text-align:center; color:#d4a574;">☕ Honduras Coffee Insights 2025</h1>
<p style="text-align:center; font-size:18px;">Dashboard interactivo de tendencias, consumo, perfiles y predicción del mercado de café en Honduras.</p>
""", unsafe_allow_html=True)

# ==========================================================
# KPIs (mismos valores del dashboard original)
# ==========================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Encuestados", f"{len(consumo_df):,}")
col2.metric("Método Popular", consumo_df["Preparación"].mode()[0])
col3.metric("Edad Promedio", f"{consumo_df['Edad'].mean():.1f}")
col4.metric("Región Dominante", consumo_df["Región"].mode()[0])

# ==========================================================
# SECCIONES — NO SE CAMBIÓ NADA DE CONTENIDO
# Solo se organizaron para mayor claridad.
# ==========================================================

st.markdown("## Panorama General del Consumo")

colA, colB = st.columns([2, 1])

with colA:
    fig_area = px.area(
        consumo_oficial,
        x="Año",
        y="Consumo",
        title="Crecimiento del consumo nacional de café (2014–2024)",
        color_discrete_sequence=["#d4a574"]
    )
    st.plotly_chart(fig_area, use_container_width=True)

with colB:
    fig_pie = px.pie(
        consumo_df,
        names="Contexto",
        title="Dónde consumen café los hondureños",
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================================
# STORYTELLING — MISMO CONTENIDO
# ==========================================================
st.markdown("## Storytelling del Consumidor Hondureño")

st.info("El consumidor hondureño se ha desplazado del consumo tradicional en casa a nuevas experiencias sociales y gourmet.")

# ==========================================================
# ESTRATEGIA Y SEGMENTACIÓN — MISMO CONTENIDO
# ==========================================================
st.markdown("## Segmentación Avanzada")

fig_heatmap = px.density_heatmap(
    consumo_df,
    x="Frecuencia",
    y="Variedad",
    color_continuous_scale=COLOR_CONTINUOUS,
    title="Relación entre frecuencia y variedad"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ==========================================================
# PREDICCIÓN — MISMO CONTENIDO
# ==========================================================
st.markdown("## Proyección 2025–2030")

fig_pred = px.line(
    proyeccion_df,
    x="Año",
    y="Consumo",
    color="Tipo",
    markers=True,
    color_discrete_sequence=["#d4a574", "#8b5e3b"]
)
st.plotly_chart(fig_pred, use_container_width=True)

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("""
<hr>
<p style='text-align:center; color:#888;'>Proyecto de Ciencia de Datos | Honduras 2025</p>
""", unsafe_allow_html=True)
