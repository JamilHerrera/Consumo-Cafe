import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Honduras Coffee Trends",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de colores "Coffee & Earth" (Discreta para gráficos como Pie, Sunburst)
COLOR_PALETTE = ['#4B3621', '#A0522D', '#D2691E', '#CD853F', '#F4A460', '#DEB887', '#556B2F']
# Paleta Continua (Plotly predefinida) para gráficos como Mapas de calor/Barras con gradiente
COLOR_CONTINUOUS = 'Sunsetdark' 

# -----------------------------------------------------------------------------
# 2. CONFIGURACIÓN DE ESTILOS Y RECURSOS
# -----------------------------------------------------------------------------
# CSS EMBEBIDO: Inyectamos el CSS directamente para evitar el error "file not found".
CUSTOM_CSS = """
/* FONDO PRINCIPAL MODIFICADO PARA MÁXIMO CONTRASTE Y TEMÁTICA DE CAFÉ */
.stApp {
    background-color: #FCF8F5; /* Nuevo color: Crema de Vainilla para mejor contraste */
}

/* Estilo para las métricas (Tarjetas KPI) */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.2s ease-in-out;
}

div[data-testid="stMetric"]:hover {
    transform: scale(1.02);
    box-shadow: 4px 4px 10px rgba(75, 54, 33, 0.1);
}

/* Títulos personalizados: Color más oscuro (#3C2F2F Deep Espresso) para mayor legibilidad */
h1, h2, h3 {
    color: #3C2F2F; 
    font-family: 'Helvetica Neue', sans-serif;
}

/* Ajuste del color de las etiquetas de las métricas: Oscurecido para asegurar contraste */
div[data-testid="stMetricLabel"] {
    color: #3C2F2F; 
    font-weight: bold;
}

/* Pestañas de Navegación (Tabs) */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #ffffff;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: #4a3b2a;
    border: 1px solid #e0e0e0;
    border-bottom: none;
}

.stTabs [aria-selected="true"] {
    background-color: #4a3b2a;
    color: white;
}

/* Footer */
footer {
    visibility: hidden;
}

.custom-footer {
    text-align: center; 
    color: #555; /* Oscurecido para mejor contraste */
    padding: 20px;
    border-top: 1px solid #e0e0e0;
    margin-top: 30px;
}
"""
st.markdown(f'<style>{CUSTOM_CSS}</style>', unsafe_allow_html=True)


def load_file_content(file_name):
    """Carga el contenido de un archivo externo de forma segura."""
    try:
        # Aseguramos la lectura con codificación UTF-8
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        # Capturamos cualquier otro error de lectura
        st.error(f"Error al leer el archivo {file_name}: {e}")
        return None

def load_js(file_name):
    js_content = load_file_content(file_name)
    if js_content:
        st.markdown(f'<script>{js_content}</script>', unsafe_allow_html=True)
    # No mostramos warning por JS, ya que a veces es opcional o solo para logging

# Cargamos el archivo JS (CSS ya está embebido)
load_js("script.js")

# -----------------------------------------------------------------------------
# 3. CARGA DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("consumo_cafe_honduras.csv")
        return df
    except FileNotFoundError:
        # Generar datos dummy si no se encuentra el archivo
        st.error("⚠️ Archivo 'consumo_cafe_honduras.csv' no encontrado. Usando datos de ejemplo para evitar fallas.")
        
        # Generación de 100 filas de datos dummy
        data = {
            "Variedad": (["Caturra", "Bourbon", "Pacas", "Lempira", "Typica"] * 20)[:100],
            "Preparación": (["Colado", "Espresso", "Cold brew", "Cappuccino", "De olla"] * 20)[:100],
            "Región": (["Copán", "Comayagua", "Agalta", "El Paraíso", "Montecillos"] * 20)[:100],
            "Contexto": (["Hogar", "Oficina", "Cafetería"] * 33 + ["Hogar"])[1:101],
            "Frecuencia": (["Diario", "Semanal", "Ocasional"] * 33 + ["Diario"])[1:101],
            "Edad": ([25, 30, 45, 22, 55, 60, 35, 28, 40, 50] * 10)[:100]
        }
        return pd.DataFrame(data)


df = load_data()

# Datos "Oficiales" (Hardcoded para el contexto macro)
df_oficial = pd.DataFrame({
    "Año": [2014, 2016, 2018, 2020, 2022, 2024],
    "Consumo": [20000, 80000, 150000, 250000, 320000, 390000]
})

# -----------------------------------------------------------------------------
# 4. ENCABEZADO (HERO SECTION)
# -----------------------------------------------------------------------------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("# ☕")
with col_title:
    st.title("Honduras Coffee Insights 2025")
    st.markdown("**Ciencia de Datos aplicada al consumo interno y cultura del café.**")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. DASHBOARD INTERACTIVO
# -----------------------------------------------------------------------------

# --- KPI ROW (FILA DE MÉTRICAS) ---
if not df.empty:
    total_encuestados = len(df)
    region_top = df['Región'].mode()[0] if 'Región' in df.columns else "N/A"
    metodo_top = df['Preparación'].mode()[0] if 'Preparación' in df.columns else "N/A"
    edad_promedio = int(df['Edad'].mean()) if 'Edad' in df.columns else 0
else:
    total_encuestados = 0
    region_top = "-"
    metodo_top = "-"
    edad_promedio = 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Muestra Analizada", f"{total_encuestados}", "Personas encuestadas")
kpi2.metric("Región Dominante", region_top, "Mayor participación")
kpi3.metric("Método Favorito", metodo_top, "Tendencia #1")
kpi4.metric("Edad Promedio", f"{edad_promedio} años", "Perfil del consumidor")

st.markdown("###") # Espacio

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3 = st.tabs(["📊 Panorama General", "🧬 ADN del Consumidor", "🗺️ Mapa & Datos"])

with tab1:
    # FILA 1: TENDENCIA MACRO vs DISTRIBUCIÓN
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Crecimiento Histórico del Consumo")
        fig_trend = px.area(df_oficial, x="Año", y="Consumo", 
                            title="Evolución en Quintales (Datos IHCAFE)",
                            markers=True, color_discrete_sequence=['#8B4513'])
        fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor='#e0e0e0')
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("Contexto de Consumo")
        if not df.empty and 'Contexto' in df.columns:
            fig_pie = px.pie(df, names='Contexto', hole=0.6, 
                             color_discrete_sequence=COLOR_PALETTE,
                             title="¿Dónde se toma café?")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay datos de contexto disponibles.")

    # FILA 2: TEXTO NARRATIVO DESTACADO
    st.info("""
    💡 **Insight:** El consumo interno ha crecido un **1,850% en la última década**, 
    impulsado fuertemente por el consumo en **Oficinas y Cafeterías**, rompiendo el mito de que 
    el hondureño solo toma café en casa.
    """)

    st.markdown("###")
    st.subheader("Detalle del Crecimiento Exponencial (2014-2024)")
    
    # Datos oficiales específicos para este gráfico
    años_g = [2014, 2020, 2024]
    consumo_g = [20000, 250000, 390000]

    fig_growth = go.Figure()

    fig_growth.add_trace(go.Scatter(
        x=años_g,
        y=consumo_g,
        mode="lines+markers",
        line=dict(color="#6b4226", width=3),
        marker=dict(size=10, color="#8b5e3c"),
        name="Consumo interno (quintales)"
    ))

    # Anotación del 1850%
    fig_growth.add_annotation(
        x=2024, y=390000,
        text="↑ +1850% en 10 años",
        showarrow=True,
        arrowhead=2,
        ax=-50, ay=-50,
        font=dict(color="green", size=14, family="Arial Black")
    )

    fig_growth.update_layout(
        title="Impacto del Auge Cafetero",
        xaxis_title="Año",
        yaxis_title="Quintales consumidos",
        template="plotly_white",
        height=450
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    

with tab2:
    st.subheader("Segmentación Avanzada del Consumidor")
    
    if not df.empty:
        # FILTROS DENTRO DE LA PESTAÑA
        c_filt1, c_filt2 = st.columns(2)
        with c_filt1:
            regiones_disponibles = df['Región'].unique() if 'Región' in df.columns else []
            filtro_region = st.multiselect("Filtrar Región:", regiones_disponibles, default=regiones_disponibles)
        with c_filt2:
            min_age = int(df['Edad'].min()) if 'Edad' in df.columns else 18
            max_age = int(df['Edad'].max()) if 'Edad' in df.columns else 90
            rango_edad = st.slider("Rango de Edad:", 18, 90, (min_age, max_age))
        
        # Filtrado de datos
        df_filtered = df[
            (df['Región'].isin(filtro_region)) & 
            (df['Edad'] >= rango_edad[0]) & 
            (df['Edad'] <= rango_edad[1])
        ]

        # GRÁFICO SUNBURST
        col_sun, col_bar = st.columns([1.5, 1])
        
        with col_sun:
            st.markdown("**Patrones de Consumo: Región ➡ Variedad ➡ Preparación**")
            if not df_filtered.empty and all(col in df.columns for col in ['Región', 'Variedad', 'Preparación']):
                fig_sun = px.sunburst(df_filtered, path=['Región', 'Variedad', 'Preparación'], 
                                        color_discrete_sequence=COLOR_PALETTE,
                                        height=500)
                st.plotly_chart(fig_sun, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para generar el gráfico radial.")

        with col_bar:
            st.markdown("**Frecuencia por Rango de Edad**")
            # Box plot para ver distribución
            if not df_filtered.empty and all(col in df.columns for col in ['Frecuencia', 'Edad']):
                fig_box = px.box(df_filtered, x="Frecuencia", y="Edad", color="Frecuencia",
                                    color_discrete_sequence=COLOR_PALETTE)
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.warning("No hay datos para el gráfico de caja.")
    else:
        st.error("No se han cargado datos para el análisis detallado.")

with tab3:
    col_map, col_raw = st.columns([1, 1])
    
    with col_map:
        st.subheader("Intensidad por Región")
        if not df.empty and 'Región' in df.columns:
            conteo_region = df['Región'].value_counts().reset_index()
            conteo_region.columns = ['Región', 'Encuestados']
            
            # El fix para el ValueError: se usa COLOR_CONTINUOUS
            fig_map = px.bar(conteo_region, y='Región', x='Encuestados', orientation='h',
                             color='Encuestados', 
                             color_continuous_scale=COLOR_CONTINUOUS, 
                             text='Encuestados')
            fig_map.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.write("Sin datos regionales.")
        
    with col_raw:
        st.subheader("Base de Datos Procesada")
        st.dataframe(df, height=300, hide_index=True)
        
        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Dataset Filtrado",
                data=csv,
                file_name='data_cafe_honduras.csv',
                mime='text/csv',
            )

# -----------------------------------------------------------------------------
# 6. FOOTER
# -----------------------------------------------------------------------------
st.markdown('<div class="custom-footer">Proyecto de Ciencias de Datos | Honduras 2025 | Datos fuente: Encuestas propias & IHCAFE</div>', unsafe_allow_html=True)