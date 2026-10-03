import streamlit as st
import pandas as pd
from calculadora import calcular_cotizacion_pvc

st.set_page_config(page_title="Cotizador PVC", page_icon="🏗️", layout="wide")

st.title("🏗️ Cotizador de Cielo Raso en PVC con Precios")
st.write("Seleccione las opciones para generar la cotización detallada.")

col_input1, col_input2 = st.columns(2)

with col_input1:
    area = st.number_input("Área total a cubrir (m²):", min_value=0.1, value=56.0, step=0.5)

with col_input2:
    opcion_thermo = st.selectbox(
        "Incluir Aislante Thermolon:",
        ["Ninguno", "5mm", "8mm"]
    )

if st.button("Calcular Cotización", type="primary"):
    resultado = calcular_cotizacion_pvc(area, opcion_thermo)
    
    # Crear DataFrame
    df = pd.DataFrame(resultado["items"])
    
    # Formatear números a moneda ($)
    df_mostrar = df.copy()
    df_mostrar["P. Unitario"] = df_mostrar["P. Unitario"].apply(lambda x: f"${x:,.0f}")
    df_mostrar["Total Base"] = df_mostrar["Total Base"].apply(lambda x: f"${x:,.0f}")
    df_mostrar["Total Sugerido"] = df_mostrar["Total Sugerido"].apply(lambda x: f"${x:,.0f}")

    st.subheader(f"Desglose de Cotización para {area} m²")
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

    # Tarjetas de Totales Financieros
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("💰 Total Cotización Base", f"${resultado['total_base']:,.0f} COP")
    with c2:
        st.metric("🛡️ Total con Adiciones (Sugerido)", f"${resultado['total_sugerido']:,.0f} COP")