import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import streamlit.components.v1 as components # Importamos para usar st.components.v1.html

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
/* FONDO PRINCIPAL MODIFICADO A CAFÉ OSCURO PARA MÁXIMO CONTRASTE (Dark Espresso) */
.stApp {
    background-color: #2C201C; 
}

/* Estilo para las métricas (Tarjetas KPI): Cambiado a color café claro/latte para mejor contraste con el fondo oscuro y tema */
div[data-testid="stMetric"] {
    background-color: #F5E5C9; /* Color: Latte claro */
    border: 1px solid #c9b493;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.4); /* Sombra más oscura para fondo oscuro */
    text-align: center;
    transition: transform 0.2s ease-in-out;
}

div[data-testid="stMetric"]:hover {
    transform: scale(1.02);
    box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2); /* Sombra de brillo para destacar en fondo oscuro */
}

/* Títulos personalizados: Cambiado a BLANCO para máxima legibilidad en el fondo oscuro */
h1, h2, h3 {
    color: #FFFFFF; 
    font-family: 'Helvetica Neue', sans-serif;
}

/* Ajuste del color de las etiquetas de las métricas: Se mantienen oscuras para el contraste con el fondo BLANCO de la tarjeta KPI */
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

/* Texto del footer cambiado a gris claro para contraste en fondo oscuro */
.custom-footer {
    text-align: center; 
    color: #AAAAAA; 
    padding: 20px;
    border-top: 1px solid #444444; /* Línea divisoria oscura */
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
# 3. CARGA DE DATOS (Se mantienen para las otras pestañas de análisis)
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
tab1, tab_story, tab2, tab3 = st.tabs(["📊 Panorama General", "📖 El Viaje del Consumidor", "🧬 ADN del Consumidor", "🗺️ Mapa & Datos"])

# -----------------------------------------------------------------------------
# STORYTELLING TAB (NUEVA PESTAÑA)
# -----------------------------------------------------------------------------
with tab_story:
    st.header("📖 El Viaje de la Taza: Transformación del Consumo de Café en Honduras")
    st.markdown("""
    Esta es la historia de cómo la cultura cafetera, tradicionalmente ligada a la producción de exportación, 
    ha florecido internamente, creando un consumidor más sofisticado y apasionado en la última década.
    """)
    st.markdown("---")
    
    # CAPÍTULO 1: El Despertar del Consumo Interno
    st.markdown('<div class="story-chapter">', unsafe_allow_html=True)
    st.subheader("Capítulo 1: El Despertar (2014-2024)")
    st.markdown("""
    Históricamente, el café hondureño era un producto de exportación. Sin embargo, en la última década, 
    el consumo interno ha experimentado un **crecimiento exponencial**. 
    Este auge no es casualidad; es el resultado de una nueva apreciación por la calidad.
    """)

    # Gráfico de Trend
    fig_trend = px.area(df_oficial, x="Año", y="Consumo", 
                        title="📈 Crecimiento del Consumo Interno: +1850% en 10 años",
                        markers=True, color_discrete_sequence=['#A0522D'],
                        height=350)
    fig_trend.update_layout(plot_bgcolor="#3C2F2F", yaxis_gridcolor='#554444')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("""
    **El Dato Clave:** El volumen de café consumido dentro del país ha pasado de ser marginal a 
    una fuerza significativa en la economía local, impulsado por las nuevas generaciones.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # CAPÍTULO 2: El Nuevo Escenario
    st.markdown('<div class="story-chapter">', unsafe_allow_html=True)
    st.subheader("Capítulo 2: Del Hogar a la Cafetería ☕🏢")
    st.markdown("""
    La forma en que se consume el café ha cambiado drásticamente. El café "de olla" sigue siendo importante, 
    pero los nuevos centros de consumo han robado el protagonismo. 
    **Las cafeterías y los ambientes de oficina** son ahora los motores de la innovación.
    """)

    col_home, col_office = st.columns(2)
    
    if not df.empty and 'Contexto' in df.columns:
        conteo_contexto = df['Contexto'].value_counts().reset_index()
        conteo_contexto.columns = ['Contexto', 'Frecuencia']
        
        with col_home:
            # Gráfico de barras para contexto
            fig_context = px.bar(conteo_contexto, y='Contexto', x='Frecuencia', orientation='h',
                                 color='Frecuencia', color_continuous_scale='Agsunset',
                                 title="Distribución por Contexto")
            fig_context.update_layout(plot_bgcolor="#3C2F2F", yaxis_gridcolor='#554444')
            st.plotly_chart(fig_context, use_container_width=True)
            
        with col_office:
            # Gráfico de Pastel para preparación
            fig_prep = px.pie(df, names='Preparación', hole=0.5, 
                             color_discrete_sequence=['#D2691E', '#CD853F', '#F4A460', '#DEB887', '#556B2F'],
                             title="Métodos de Preparación Más Populares")
            st.plotly_chart(fig_prep, use_container_width=True)
            
    st.markdown("""
    **El Impacto:** El auge del café en la oficina (Diario/Semanal) y la popularidad de métodos como el 
    **Espresso** y el **Cold Brew** (Cafeterías) indican una profesionalización de la experiencia del café.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # CAPÍTULO 3: El Perfil del Nuevo Conocedor
    st.markdown('<div class="story-chapter">', unsafe_allow_html=True)
    st.subheader("Capítulo 3: El Conocedor Joven y la Variedad 🧠🌱")
    
    if not df.empty and all(col in df.columns for col in ['Variedad', 'Edad']):
        
        # Filtramos para mostrar solo los 5 más comunes para claridad en la historia
        top_varieties = df['Variedad'].value_counts().nlargest(5).index
        df_top_varieties = df[df['Variedad'].isin(top_varieties)]
        
        # Gráfico Boxplot para edad vs. variedad
        fig_age_variety = px.box(df_top_varieties, x="Variedad", y="Edad", color="Variedad",
                                 color_discrete_sequence=['#4B3621', '#A0522D', '#D2691E', '#CD853F', '#F4A460'],
                                 title="Edad Promedio por Variedad de Café Consumida")
        fig_age_variety.update_layout(plot_bgcolor="#3C2F2F", yaxis_gridcolor='#554444')
        st.plotly_chart(fig_age_variety, use_container_width=True)

        st.markdown(f"""
        **La Demografía:** La edad promedio del consumidor se mantiene en los **{edad_promedio} años**, 
        pero el consumo de variedades más finas como **Bourbon** y **Caturra** está concentrado 
        en rangos de edad más jóvenes (visualmente en el gráfico de caja, se puede inferir 
        que el rango intercuartílico es más bajo para estas variedades).
        
        El consumidor hondureño ya no pregunta solo por "café", sino por el origen (**Copán**, **Montecillos**) 
        y la variedad (**Pacas**, **Typica**), demostrando un profundo nivel de **Madurez del Mercado**.
        """)
    else:
        st.warning("Datos insuficientes para el análisis demográfico del Storytelling.")
        
    st.markdown('</div>', unsafe_allow_html=True)

with tab1:
    st.subheader("Dashboard de Power BI Integrado")
    
    
    # URL de Power BI proporcionada por el usuario (incrustada)
    power_bi_iframe = """
    <iframe title="proyecto" width="100%" height="600" 
            src="https://app.powerbi.com/view?r=eyJrIjoiMDdjNWU5MDctMTlmNC00MWJjLWIwNmYtNGMwMDM5NzQyNjUxIiwidCI6ImFmMmZkMTk2LTFkOWYtNDdiNC05MDY5LTM5MWE0NmY4MzYwMSIsImMiOjR9" 
            frameborder="0" allowFullScreen="true">
    </iframe>
    """
    
    # Usamos st.components.v1.html para incrustar el iframe
    components.html(power_bi_iframe, height=650, scrolling=True)

    # Texto narrativo destacado (Mantenemos el texto)
    st.info("""
    💡 **Insight (del análisis original):** El consumo interno ha crecido un **1,850% en la última década**, 
    impulsado fuertemente por el consumo en **Oficinas y Cafeterías**, rompiendo el mito de que 
    el hondureño solo toma café en casa.
    """)
    

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