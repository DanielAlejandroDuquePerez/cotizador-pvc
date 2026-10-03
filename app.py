import streamlit as st
import pandas as pd
from calculadora import calcular_cotizacion_pvc

st.set_page_config(
    page_title="Cotizador PVC", 
    page_icon="📐", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS con alto contraste para modo oscuro
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h2 {
        margin: 0;
        font-weight: 700;
        font-size: 1.4rem;
        color: #f8fafc;
    }
    .main-header p {
        margin: 4px 0 0 0;
        font-size: 0.85rem;
        color: #94a3b8;
    }

    /* Tarjetas de Métricas en Modo Oscuro de alto contraste */
    [data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #4ade80 !important;
        font-weight: 600 !important;
    }
    
    div.stButton > button:first-child {
        width: 100%;
        border-radius: 12px;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        background-color: #2563eb;
        color: white;
        border: none;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown("""
    <div class="main-header">
        <h2>📐 Cotizador Cielo Raso PVC</h2>
        <p>Calculadora de materiales y presupuestos</p>
    </div>
""", unsafe_allow_html=True)

# Entradas
with st.container():
    area = st.number_input("📏 Área a cubrir (m²):", min_value=0.1, value=56.0, step=0.5)
    opcion_thermo = st.selectbox("🌡️ Aislante Thermolon:", ["Ninguno", "5mm", "8mm"])

st.write("")

if st.button("🚀 Calcular Presupuesto", type="primary"):
    resultado = calcular_cotizacion_pvc(area, opcion_thermo)
    
    # Métricas principales
    st.markdown("### 💳 Resumen de Inversión")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Total Base", value=f"${resultado['total_base']:,.0f}")
    with c2:
        st.metric(
            label="Total Sugerido", 
            value=f"${resultado['total_sugerido']:,.0f}",
            delta="Con Adiciones"
        )

    st.write("")

    # Tabla con TODAS las columnas (Base y Sugeridas)
    with st.expander("📋 Ver Desglose Completo de Materiales", expanded=True):
        df = pd.DataFrame(resultado["items"])
        
        df_mostrar = df.copy()
        df_mostrar["P. Unitario"] = df_mostrar["P. Unitario"].apply(lambda x: f"${x:,.0f}")
        df_mostrar["Total Base"] = df_mostrar["Total Base"].apply(lambda x: f"${x:,.0f}")
        df_mostrar["Total Sugerido"] = df_mostrar["Total Sugerido"].apply(lambda x: f"${x:,.0f}")
        
        # Muestra todas las columnas del cálculo original
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

    # Texto para compartir
    resumen_texto = f"""*COTIZACIÓN CIELO RASO PVC ({area} m²)*
-----------------------------------
• Total Inversión Base: ${resultado['total_base']:,.0f} COP
• Total Con Adiciones (Sugerido): ${resultado['total_sugerido']:,.0f} COP
• Incluye Thermolon: {opcion_thermo}
-----------------------------------
*Generado automáticamente.*"""

    st.text_area("📱 Copiar resumen para enviar al cliente:", resumen_texto, height=140)