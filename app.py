import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np # Necesario para la regresión polinomial (modelo predictivo)
import os
import sys
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Honduras Coffee Trends",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de colores "Coffee & Earth"
COLOR_PALETTE = ['#4B3621', '#A0522D', '#D2691E', '#CD853F', '#F4A460', '#DEB887', '#556B2F']
COLOR_CONTINUOUS = 'Sunsetdark' 

# -----------------------------------------------------------------------------
# 2. CONFIGURACIÓN DE ESTILOS Y RECURSOS
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
/* FONDO PRINCIPAL MODIFICADO A CAFÉ OSCURO PARA MÁXIMO CONTRASTE (Dark Espresso) */
.stApp {
    background-color: #2C201C; 
}

/* Estilo para las métricas (Tarjetas KPI) */
div[data-testid="stMetric"] {
    background-color: #F5E5C9; /* Color: Latte claro */
    border: 1px solid #c9b493;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
    text-align: center;
    transition: transform 0.2s ease-in-out;
}

div[data-testid="stMetric"]:hover {
    transform: scale(1.02);
    box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
}

/* Títulos personalizados: BLANCO */
h1, h2, h3, h4 {
    color: #FFFFFF; 
    font-family: 'Helvetica Neue', sans-serif;
}

/* Ajuste del color de las etiquetas de las métricas */
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

/* Estilo específico para el texto de Storytelling */
.story-chapter {
    padding: 20px;
    margin-bottom: 25px;
    border-left: 5px solid #D2691E;
    background-color: #3C2F2F;
    border-radius: 8px;
    color: #F5E5C9;
}

/* Estilo para los insights clave en la sección de estrategia */
.insight-box {
    background-color: #4B3621;
    color: #F5E5C9;
    padding: 15px;
    border-radius: 8px;
    margin-top: 10px;
    font-style: italic;
    border: 1px solid #D2691E;
}

/* Estilo específico para la proyección predictiva */
.prediction-box {
    background-color: #A0522D; /* Color terracota */
    color: #FFFFFF;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 20px;
    border: 3px solid #F4A460;
}

/* Estilo para los bloques de decisión (Roadmap) */
.decision-block {
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 12px;
    border: 2px solid #D2691E; /* Borde café claro */
    background: linear-gradient(135deg, #4B3621, #2C201C); /* Gradiente sutil */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    color: #F5E5C9;
}

.decision-block h4 {
    color: #F4A460; /* Título color naranja suave */
    border-bottom: 2px solid #D2691E;
    padding-bottom: 10px;
    margin-top: 0;
}

.decision-block ul {
    list-style-type: '☕ '; /* Icono de café para las listas */
    padding-left: 20px;
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
    border-top: 1px solid #444444;
    margin-top: 30px;
}
"""
st.markdown(f'<style>{CUSTOM_CSS}</style>', unsafe_allow_html=True)


def load_file_content(file_name):
    """Carga el contenido de un archivo externo de forma segura."""
    # En un entorno de streamlit local, esto no se usa, pero se mantiene como buena práctica
    # En este entorno de desarrollo, lo omitimos para evitar errores de E/S.
    return None

def load_js(file_name):
    js_content = load_file_content(file_name)
    if js_content:
        st.markdown(f'<script>{js_content}</script>', unsafe_allow_html=True)

# Cargamos el archivo JS (CSS ya está embebido)
load_js("script.js")

# -----------------------------------------------------------------------------
# 3. CARGA Y MODELADO DE DATOS 
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Se asume que 'consumo_cafe_honduras.csv' está disponible
        df = pd.read_csv("consumo_cafe_honduras.csv")
        # Generar una columna 'ID' si no existe, solo por si acaso
        if 'ID' not in df.columns:
            df['ID'] = range(1, len(df) + 1)
        return df
    except FileNotFoundError:
        st.error("⚠️ Archivo 'consumo_cafe_honduras.csv' no encontrado. Usando datos de ejemplo para evitar fallas.")
        
        # Generación de 1000 filas de datos dummy
        N = 1000
        data = {
            "ID": range(1, N + 1),
            "Variedad": (["Caturra", "Bourbon", "Pacas", "Lempira", "Typica"] * (N // 5 + 1))[:N],
            "Preparación": (["Colado", "Espresso", "Cold brew", "Cappuccino", "De olla", "Instantáneo"] * (N // 6 + 1))[:N],
            "Región": (["Copán", "Comayagua", "Agalta", "El Paraíso", "Montecillos", "Opalaca"] * (N // 6 + 1))[:N],
            "Contexto": (["Hogar", "Oficina", "Cafetería"] * (N // 3 + 1))[:N],
            "Frecuencia": (["Diario", "Semanal", "Ocasional"] * (N // 3 + 1))[:N],
            "Edad": np.random.randint(18, 65, N) 
        }
        return pd.DataFrame(data)

# Datos "Oficiales" (Hardcoded para el contexto macro)
# Estos datos muestran un crecimiento no lineal (acelerado)
df_oficial = pd.DataFrame({
    "Año": [2014, 2016, 2018, 2020, 2022, 2024],
    "Consumo": [20000, 80000, 150000, 250000, 320000, 390000] # Consumo en quintales
})

df = load_data()

# -----------------------------------------------------------------------------
# 4. MODELO PREDICTIVO (REGRESIÓN POLINOMIAL)
# -----------------------------------------------------------------------------
def predict_coffee_consumption(df_history, years_to_predict=6, degree=2):
    """
    Entrena un modelo de regresión polinomial y predice el consumo futuro.
    """
    X = df_history['Año'].values
    y = df_history['Consumo'].values
    
    # 2. Entrenar el modelo (Ajustar un polinomio de grado 'degree' a los datos)
    coefficients = np.polyfit(X, y, degree)
    polynomial = np.poly1d(coefficients)
    
    # 3. Generar años futuros para la predicción
    last_year = df_history['Año'].max()
    prediction_years = np.arange(last_year + 1, last_year + years_to_predict + 1)
    
    # 4. Generar las predicciones
    predicted_consumption = polynomial(prediction_years)
    
    # 5. Crear DataFrame de predicciones
    df_predictions = pd.DataFrame({
        'Año': prediction_years,
        'Consumo': predicted_consumption.round(0).astype(int),
        'Tipo': 'Proyección'
    })
    
    # 6. Combinar con datos históricos
    df_history['Tipo'] = 'Histórico'
    df_combined = pd.concat([df_history, df_predictions], ignore_index=True)
    
    return df_combined, polynomial

# Entrenar y obtener el modelo
df_proyeccion, model_polynomial = predict_coffee_consumption(df_oficial.copy(), years_to_predict=6, degree=2)


# -----------------------------------------------------------------------------
# 5. ENCABEZADO (HERO SECTION)
# -----------------------------------------------------------------------------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("# ☕")
with col_title:
    st.title("Honduras Coffee Insights 2025")
    st.markdown("**Ciencia de Datos aplicada al consumo interno y cultura del café.**")

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. DASHBOARD INTERACTIVO
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

# Obtener la predicción para 2030 y el crecimiento total proyectado
consumo_2030 = df_proyeccion[df_proyeccion['Año'] == 2030]['Consumo'].iloc[0] if not df_proyeccion.empty and 2030 in df_proyeccion['Año'].values else 0
consumo_2024 = df_oficial[df_oficial['Año'] == 2024]['Consumo'].iloc[0] if not df_oficial.empty and 2024 in df_oficial['Año'].values else 1 # Evitar división por cero
crecimiento_proyectado = ((consumo_2030 - consumo_2024) / consumo_2024) * 100 if consumo_2024 > 0 else 0

kpi1, kpi2, kpi3, kpi_pred = st.columns(4)
kpi1.metric("Muestra Analizada", f"{total_encuestados}", "Personas encuestadas")
kpi2.metric("Región Dominante", region_top, "Mayor participación")
kpi3.metric("Método Favorito", metodo_top, "Tendencia #1")
kpi_pred.metric("Consumo Proyectado (2030)", f"{consumo_2030:,.0f} Quintales", f"Crecimiento del {crecimiento_proyectado:,.0f}% vs. 2024")

st.markdown("###") # Espacio

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab_story, tab_strategy, tab_predict, tab_roadmap, tab2, tab3 = st.tabs([
    "📊 Panorama General", 
    "📖 El Viaje del Consumidor", 
    "🎯 Estrategia y Segmentación",
    "🔮 Proyección de Consumo",
    "💡 Roadmap de Decisión", # NUEVA PESTAÑA DE ALTO VALOR
    "🧬 ADN del Consumidor", 
    "🗺️ Mapa & Datos"
])

# -----------------------------------------------------------------------------
# PESTAÑA CORREGIDA: ROADMAP DE DECISIÓN
# -----------------------------------------------------------------------------
with tab_roadmap:
    st.header("💡 Roadmap Estratégico 2025-2030: Maximizando la Oportunidad del Café")
    st.markdown("""
    Esta sección traduce el análisis predictivo y la segmentación del consumidor en **tres pilares de acción inmediata**,
    alineando la producción y el marketing con el crecimiento proyectado.
    """)
    st.markdown("---")
    
    col_pro, col_dist, col_inv = st.columns(3)
    
    # ------------------
    # PILAR 1: PRODUCTO
    # ------------------
    with col_pro:
        st.markdown('<div class="decision-block">', unsafe_allow_html=True)
        st.markdown("<h4>Estrategia de Producto: Fidelizar y Sofisticar</h4>", unsafe_allow_html=True)
        st.markdown("Basada en la **Matriz de Oportunidad** (Heatmap):")
        
        st.markdown("**Objetivo:** Aumentar la tasa de conversión de 'Ocasional' a 'Diario' en segmentos de valor.")
        
        # FIX: Se usa una sola llamada a st.markdown para la lista completa
        list_html_pro = f"""
        <ul>
            <li>Foco de Retención (Variedades Estables):Reforzar la disponibilidad de Lempiray Pacas en contextos de Oficina y Hogar. Este es el ingreso base, la fidelidad diaria.</li>
            <li>Foco de Crecimiento (Variedades Premium): Crear kits de iniciación y programas de suscripción para Bourbon y Caturra. Dirigido al consumidor de 25-45 años, cuyo alto potencial de gasto está actualmente clasificado como 'Ocasional'.</li>
            <li>Innovación en Métodos:Invertir en promocionar el Cold Brew y Espresso. Estos métodos dominan en la demografía más joven (menores de 35 años) y son la clave para atraer a la Generación Z.</li>
        </ul>
        """
        st.markdown(list_html_pro, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------
    # PILAR 2: DISTRIBUCIÓN
    # ------------------
    with col_dist:
        st.markdown('<div class="decision-block">', unsafe_allow_html=True)
        st.markdown("<h4>Estrategia de Distribución: Dominar el Contexto</h4>", unsafe_allow_html=True)
        st.markdown("Basada en el **Análisis de Contexto** (Storytelling):")
        
        st.markdown("**Objetivo:** Capitalizar la transición de 'Hogar' a 'Oficina/Cafetería' como centro de consumo.")
        
        # FIX: Se usa una sola llamada a st.markdown para la lista completa
        list_html_dist = f"""
        <ul>
            <li>Expansión B2B (Oficina):Crear convenios de suministro exclusivo con las 50 empresas más grandes. El consumo en la Oficina es el segundo más alto y garantiza una demanda semanal estable.</li>
            <li>Geografía de Inversión:Dirigir la inversión en nuevas cafeterías y puntos de venta a Copán y Comayagua (regiones con alta muestra), pero con atención prioritaria a **Montecillos** y **El Paraíso** para equilibrar el mercado.</li>
            <li>Retail Inteligente:Rediseñar el empaque para el canal de Hogar, enfatizando la Región de Origen(trazabilidad), que resuena con el consumidor más informado (30-45 años).</li>
        </ul>
        """
        st.markdown(list_html_dist, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # ------------------
    # PILAR 3: INVERSIÓN
    # ------------------
    with col_inv:
        st.markdown('<div class="decision-block">', unsafe_allow_html=True)
        st.markdown("<h4>Estrategia de Inversión: Escalar la Capacidad</h4>", unsafe_allow_html=True)
        st.markdown(f"Basada en la **Proyección a 2030**:")
        
        st.markdown(f"**Objetivo:** Asegurar una capacidad de producción y procesamiento para satisfacer una demanda de **{consumo_2030:,.0f} quintales**.")
        
        # FIX: Se usa una sola llamada a st.markdown para la lista completa
        list_html_inv = f"""
        <ul>
            <li>Expansión de Tostado:Planificar la inversión en 3 nuevas plantas de tostado de alta capacidad para el año 2028, anticipando la demanda del 2030. La capacidad actual no es sostenible con el crecimiento del{crecimiento_proyectado:,.0f}%.</li>
            <li>Gestión de Inventario:Mantener reservas de café verde premium para mitigar la volatilidad de precios en el mercado de exportación, asegurando que la demanda interna no afecte la calidad del producto.</li>
            <li>Talento y Capacitación:Lanzar un programa de certificación de baristas para profesionalizar el servicio en el canal HORECA (Hoteles, Restaurantes y Cafeterías), elevando la experiencia de consumo en los centros de crecimiento.</li>
        </ul>
        """
        st.markdown(list_html_inv, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Pestaña 1 (Panorama General)
# -----------------------------------------------------------------------------
with tab1:
    st.header("Panorama General y Dashboard Interactivo")
    
    # Nuevo Iframe de Power BI proporcionado por el usuario
    power_bi_iframe = """
    <iframe title="proyecto" width="100%" height="700" 
            src="https://app.powerbi.com/view?r=eyJrIjoiMDdjNWU5MDctMTlmNC00MWJjLWIwNmYtNGMwMDM5NzQyNjUxIiwidCI6ImFmMmZkMTk2LTFkOWYtNDdiNC05MDY5LTM5MWE0NmY4MzYwMSIsImMiOjR9&pageName=26513b8306c77008142e" 
            frameborder="0" allowFullScreen="true">
    </iframe>
    """
    
    # Se incrusta el Power BI (reporte completo)
    st.subheader("Reporte Completo de Power BI")
    components.html(power_bi_iframe, height=750, scrolling=True)
    
    st.markdown("---")
    st.subheader("Análisis de Crecimiento")
    
    # Gráfico de Plotly debajo del Power BI
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig_trend = px.area(df_oficial, x="Año", y="Consumo", 
                            title="Evolución Histórica en Quintales (Datos IHCAFE)",
                            markers=True, color_discrete_sequence=['#8B4513'])
        fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor='#e0e0e0')
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        if not df.empty and 'Contexto' in df.columns:
            fig_pie = px.pie(df, names='Contexto', hole=0.6, 
                             color_discrete_sequence=COLOR_PALETTE,
                             title="Distribución por Contexto de Consumo")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay datos de contexto disponibles.")

    st.info("""
    💡 **Insight:** El consumo interno ha crecido un **1,850% en la última década**, 
    impulsado fuertemente por el consumo en **Oficinas y Cafeterías**, rompiendo el mito de que 
    el hondureño solo toma café en casa.
    """)

# Pestaña 2 (Storytelling)
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
        en rangos de edad más jóvenes.
        
        El consumidor hondureño ya no pregunta solo por "café", sino por el origen (**Copán**, **Montecillos**) 
        y la variedad (**Pacas**, **Typica**), demostrando un profundo nivel de **Madurez del Mercado**.
        """)
    else:
        st.warning("Datos insuficientes para el análisis demográfico del Storytelling.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# Pestaña 3 (Estrategia)
with tab_strategy:
    st.header("🎯 Estrategia Accionable: Mapa de Oportunidades de Mercado")
    st.markdown("""
    Este análisis cruza la **Fidelidad (Frecuencia)** con la **Variedad** para identificar dónde invertir 
    esfuerzos de marketing: **nichos consolidados** vs. **oportunidades de crecimiento**.
    """)
    st.markdown("---")

    if not df.empty and all(col in df.columns for col in ['Variedad', 'Frecuencia', 'Edad']):
        
        # --- 1. MATRIZ DE OPORTUNIDAD (HEATMAP) ---
        df_crosstab = pd.crosstab(df['Frecuencia'], df['Variedad'])
        frecuencia_order = ['Diario', 'Semanal', 'Ocasional']
        df_crosstab = df_crosstab.reindex(frecuencia_order, axis=0).fillna(0)
        
        z = df_crosstab.values
        x = df_crosstab.columns
        y = df_crosstab.index
        
        fig_heatmap = go.Figure(data=go.Heatmap(
                z=z,
                x=x,
                y=y,
                colorscale=COLOR_CONTINUOUS, 
                text=[[str(val) for val in row] for row in z],
                texttemplate="%{text}",
                hovertemplate="Variedad: %{x}<br>Frecuencia: %{y}<br>Conteo: %{z}<extra></extra>"
            ))
        
        fig_heatmap.update_layout(
            title='Matriz de Oportunidad: Frecuencia vs. Variedad',
            xaxis_title="Variedad de Café",
            yaxis_title="Frecuencia de Consumo",
            plot_bgcolor="#2C201C"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **🚀 Insights Estratégicos del Heatmap**
        * **Zona de Fidelidad Máxima (Consolidación):** Observa dónde se cruzan los consumidores **"Diarios"** con las variedades tradicionales. La estrategia aquí es la retención.
        * **Nicho Desatendido (Oportunidad):** Busca variedades de alta calidad (ej. **Bourbon** o **Caturra**) con baja frecuencia (**"Ocasional"**). La campaña debe enfocarse en la **accesibilidad** y la **rutina**.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- 2. SEGMENTACIÓN POR VALOR (Edad vs. Frecuencia) ---
        st.subheader("Segmento de Mayor Potencial de Gasto (RFM Simplificado)")
        
        gasto_mapping = {'Diario': 3, 'Semanal': 2, 'Ocasional': 1}
        df['GastoPotencial'] = df['Frecuencia'].map(gasto_mapping)
        
        df_scatter = df.groupby(['Edad', 'Frecuencia'], as_index=False).agg(
            Conteo=('ID', 'size'),
            DiversidadMetodo=('Preparación', 'nunique')
        )

        fig_scatter = px.scatter(df_scatter, x='Edad', y='Frecuencia', size='Conteo', 
                                 color='DiversidadMetodo', 
                                 color_continuous_scale='Inferno',
                                 log_x=False, size_max=40,
                                 category_orders={"Frecuencia": frecuencia_order},
                                 title="Relación Edad, Frecuencia y Diversidad de Métodos")
        
        fig_scatter.update_layout(plot_bgcolor="#2C201C")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **💰 Segmentos Clave de Valor**
        * **El Consumidor Premium (Alto Valor):** Individuos en el rango de **30-45 años** que consumen **"Diario"** y muestran alta **Diversidad de Métodos**.
        * **El Consumidor de Mañana (Potencial):** Jóvenes **menores de 25 años** que consumen **"Semanal"**. Requieren educación para la fidelización diaria.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.error("Datos insuficientes para generar el análisis estratégico de alto impacto.")


# Pestaña 4 (Predicción)
with tab_predict:
    st.header("🔮 Proyección del Consumo Interno de Café en Honduras (Hasta 2030)")
    st.markdown("""
    Aplicamos un **Modelo de Regresión Polinomial de Grado 2** a los datos históricos 
    (2014-2024) para proyectar el crecimiento acelerado del mercado hasta el año 2030.
    Este modelo se basa en la tendencia no lineal observada en la última década.
    """)
    st.markdown("---")

    # Gráfico de Predicción
    if not df_proyeccion.empty:
        
        # El gráfico combina el histórico (línea sólida) y la proyección (línea punteada/diferente color)
        fig_pred = px.scatter(df_proyeccion, x='Año', y='Consumo', 
                              color='Tipo', 
                              color_discrete_map={'Histórico': '#CD853F', 'Proyección': '#A0522D'},
                              title='Consumo Histórico vs. Proyección (Quintales de Café)',
                              labels={'Consumo': 'Consumo Estimado (Quintales)', 'Año': 'Año', 'Tipo': 'Tipo de Dato'})
        
        # Añadir la línea de tendencia completa (Histórico + Proyección)
        fig_pred.add_trace(go.Line(
            x=df_proyeccion['Año'],
            y=df_proyeccion['Consumo'],
            mode='lines',
            line=dict(color='#A0522D', width=3),
            name='Línea de Tendencia'
        ))
        
        # Estilizar el gráfico
        fig_pred.update_layout(plot_bgcolor="#3C2F2F", yaxis_gridcolor='#554444')
        fig_pred.update_traces(marker=dict(size=10))
        
        st.plotly_chart(fig_pred, use_container_width=True)

        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        st.markdown(f"**PREDICCIÓN CLAVE 2030:**")
        st.markdown(f"Se proyecta que el consumo interno alcanzará los **{consumo_2030:,.0f} quintales**.")
        st.markdown(f"Esto representa una oportunidad de mercado de **+{crecimiento_proyectado:,.0f}%** en los próximos 6 años.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Análisis de Riesgo y Sensibilidad")
        st.markdown("""
        La predicción asume que los factores clave de crecimiento (urbanización, cultura de cafeterías, 
        y cambio demográfico) continúan al ritmo actual.
        """)
        
        col_risk1, col_risk2 = st.columns(2)
        
        with col_risk1:
            st.info("""
            **Riesgos a la Baja (Low-End):**
            * Volatilidad en los precios de exportación que desvíe el foco del productor.
            * Recesión económica que afecte el poder adquisitivo para cafés especiales.
            * Cambios regulatorios o climáticos severos.
            """)
        with col_risk2:
            st.success("""
            **Potencial al Alza (High-End):**
            * Inversión agresiva en infraestructura de cafeterías (mayor accesibilidad).
            * Programas de educación de consumo patrocinados por IHCAFE o marcas.
            * Aumento de la clase media que demanda más calidad y conveniencia.
            """)
            
    else:
        st.error("No se pudo generar el modelo predictivo debido a datos insuficientes.")


# Pestaña 5 (ADN del Consumidor)
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

        # GRÁFICO SUNBURST Y BOXPLOT - Separados en columnas
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
            if not df_filtered.empty and all(col in df.columns for col in ['Frecuencia', 'Edad']):
                fig_box = px.box(df_filtered, x="Frecuencia", y="Edad", color="Frecuencia",
                                    color_discrete_sequence=COLOR_PALETTE)
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.warning("No hay datos para el gráfico de caja.")
    else:
        st.error("No se han cargado datos para el análisis detallado.")

# Pestaña 6 (Mapa & Datos)
with tab3:
    col_map, col_raw = st.columns([1, 1])
    
    with col_map:
        st.subheader("Intensidad de Muestra por Región")
        if not df.empty and 'Región' in df.columns:
            conteo_region = df['Región'].value_counts().reset_index()
            conteo_region.columns = ['Región', 'Encuestados']
            
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
# 7. FOOTER
# -----------------------------------------------------------------------------
st.markdown('<div class="custom-footer">Proyecto de Ciencias de Datos | Honduras 2025 | Datos fuente: Encuestas propias & IHCAFE</div>', unsafe_allow_html=True)