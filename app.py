import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Consumo de café en Honduras", layout="wide")

# -------------------------------
# Cargar CSS y JS externos
# -------------------------------
with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("frontend/script.js") as f:
    st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# -------------------------------
# Encabezado narrativo
# -------------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.title("☕ El viaje del café en Honduras")
st.markdown("""
Este portal combina análisis interactivo en **Power BI** con narrativa cultural y datos oficiales
para entender cómo evoluciona el consumo de café en Honduras.
""")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Sección 1: Dashboard de Power BI
# -------------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📊 Dashboard interactivo (Power BI)")
powerbi_iframe = """
<iframe width="1000" height="600"
src="https://app.powerbi.com/view?r=eyJrIjoiMDdjNWU5MDctMTlmNC00MWJjLWIwNmYtNGMwMDM5NzQyNjUxIiwidCI6ImFmMmZkMTk2LTFkOWYtNDdiNC05MDY5LTM5MWE0NmY4MzYwMSIsImMiOjR9"
frameborder="0" allowFullScreen="true"></iframe>
"""
st.markdown(powerbi_iframe, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Sección 2: Datos oficiales
# -------------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📈 Consumo interno según IHCAFE")
df_oficial = pd.DataFrame({
    "Año": [2014, 2016, 2018, 2020, 2022, 2024],
    "Consumo_quintales": [20000, 80000, 150000, 250000, 320000, 390000]
})
fig = px.line(df_oficial, x="Año", y="Consumo_quintales", markers=True,
              title="Evolución del consumo interno de café en Honduras (quintales)",
              labels={"Consumo_quintales": "Quintales consumidos"})
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Sección 3: Narrativa cultural
# -------------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📖 Historia y hallazgos")
st.markdown("""
- En 2014, el consumo interno era de apenas **20 mil quintales**.  
- En 2024, alcanzó los **390 mil quintales**, impulsado por el auge de cafés especiales y cultura barista.  
- Las regiones como **Copán y Comayagua** lideran en intensidad y tradición.  
- Los jóvenes (18–34) prefieren métodos modernos como **cold brew y espresso**, especialmente en contextos urbanos.  
- Según la FAO, el café hondureño es clave en la transformación agroalimentaria sostenible.
""")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Sección 4: Exploración con dataset
# -------------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("🔍 Exploración personalizada con registros")
df = pd.read_csv("consumo_cafe_honduras.csv")

region = st.selectbox("Selecciona región", ["Todas"] + sorted(df["Región"].unique()))
edad_rango = st.slider("Rango de edad", 18, 65, (18, 35))

df_filtrado = df.copy()
if region != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Región"] == region]
df_filtrado = df_filtrado[(df_filtrado["Edad"] >= edad_rango[0]) & (df_filtrado["Edad"] <= edad_rango[1])]

fig2 = px.bar(df_filtrado, x="Preparación", color="Frecuencia",
              title="Preferencias de preparación por frecuencia de consumo")
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown('<div class="footer">© 2025 Proyecto Café Honduras</div>', unsafe_allow_html=True)
