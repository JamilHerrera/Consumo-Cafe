import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Consumo de café en Honduras", layout="wide")

# Título y descripción
st.title("☕ Tendencias de consumo de café en Honduras")
st.markdown("""
Explora cómo evoluciona el consumo de café en Honduras según **edad, región, variedad y contexto**.
Este sitio combina un **dashboard de Power BI** con visualizaciones interactivas adicionales en Python.
""")

# --- Sección 1: Dashboard de Power BI incrustado ---
st.subheader("📊 Dashboard interactivo (Power BI)")
powerbi_iframe = """
<iframe width="1000" height="600"
src="https://app.powerbi.com/groups/be8910f5-22ae-4f33-995d-57cf24739b95/reports/660892a6-d9f0-4375-b1a7-7a16cd7f80d6/26513b8306c77008142e?experience=power-bi"
frameborder="0" allowFullScreen="true"></iframe>
"""
st.markdown(powerbi_iframe, unsafe_allow_html=True)

# --- Sección 2: Dataset en Python ---
st.subheader("📈 Exploración adicional con Python")

# Cargar dataset (ejemplo: consumo_cafe_honduras.csv)
# Reemplaza con tu archivo real
df = pd.DataFrame({
    "Edad": [22, 30, 45, 28, 35, 50, 40, 23],
    "Region": ["Copán", "Comayagua", "Montecillos", "Copán", "El Paraíso", "Comayagua", "Agalta", "Opalaca"],
    "Variedad": ["Caturra", "Bourbon", "Pacas", "Typica", "Lempira", "Caturra", "Bourbon", "Pacas"],
    "Consumo_mensual": [12, 15, 20, 10, 18, 22, 16, 14]
})

# Filtros interactivos
region = st.selectbox("Selecciona región", ["Todas"] + sorted(df["Region"].unique()))
edad_rango = st.slider("Rango de edad", 18, 60, (18, 40))

# Aplicar filtros
df_filtrado = df.copy()
if region != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Region"] == region]
df_filtrado = df_filtrado[(df_filtrado["Edad"] >= edad_rango[0]) & (df_filtrado["Edad"] <= edad_rango[1])]

# Gráfico dinámico
fig = px.bar(df_filtrado, x="Variedad", y="Consumo_mensual", color="Region",
             title="Consumo mensual por variedad y región")
st.plotly_chart(fig, use_container_width=True)

# --- Sección 3: Insights narrativos ---
st.subheader("📖 Insights")
st.markdown("""
- Los consumidores jóvenes (18–30) tienden a preferir métodos modernos como **espresso y cold brew**.  
- En regiones tradicionales como **Copán y Comayagua**, variedades como **Caturra y Bourbon** siguen dominando.  
- El consumo mensual promedio se mantiene entre **12 y 20 tazas**, con picos en contextos de oficina.  
""")
