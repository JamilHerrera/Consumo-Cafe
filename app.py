import streamlit as st

st.set_page_config(page_title="Consumo de café en Honduras", layout="wide")

st.title("☕ Tendencias de consumo de café en Honduras")

st.markdown("""
Este dashboard interactivo muestra las tendencias de consumo de café en Honduras,
basado en variedades como **Caturra, Bourbon, Pacas, Lempira y Typica**, y métodos
de preparación tradicionales y modernos.
""")

# Aquí pegas el iframe de Power BI
powerbi_iframe = """
<iframe width="1000" height="600"
src="https://app.powerbi.com/groups/me/reports/660892a6-d9f0-4375-b1a7-7a16cd7f80d6/26513b8306c77008142e?experience=power-bi"
frameborder="0" allowFullScreen="true"></iframe>
"""

st.markdown(powerbi_iframe, unsafe_allow_html=True)

