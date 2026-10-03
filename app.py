import streamlit as st
import pandas as pd
from calculadora import calcular_cotizacion_pvc

# Configuración de página enfocada en respuesta móvil
st.set_page_config(
    page_title="Cotizador PVC", 
    page_icon="📐", 
    layout="centered", # Centrado se adapta mejor a pantallas de celulares
    initial_sidebar_state="collapsed"
)

# Estilos CSS inyectados para estética Mobile-First
st.markdown("""
    <style>
    /* Estructura general y márgenes móviles */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Encabezado elegante */
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

    /* Targetas de métricas clave (Fondo oscuro adaptado al tema con alto contraste) */
    [data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* Forzar visibilidad y legibilidad de textos en las métricas */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important; /* Gris claro legible para el título */
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #38bdf8 !important; /* Azul celeste vibrante para la cifra principal */
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #4ade80 !important; /* Verde claro para el texto delta */
        font-weight: 600 !important;
    }
    
    /* Botón principal táctil */
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
    
    /* Ocultar elementos predeterminados */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Encabezado visual
st.markdown("""
    <div class="main-header">
        <h2>📐 Cotizador Cielo Raso PVC</h2>
        <p>Calculadora de materiales y presupuestos</p>
    </div>
""", unsafe_allow_html=True)

# Controles de Entrada (Optimizados para toques con el pulgar)
with st.container():
    area = st.number_input(
        "📏 Área a cubrir (m²):", 
        min_value=0.1, 
        value=56.0, 
        step=0.5
    )
    
    opcion_thermo = st.selectbox(
        "🌡️ Aislante Thermolon:",
        ["Ninguno", "5mm", "8mm"]
    )

st.write("") # Espaciador táctil

if st.button("🚀 Calcular Presupuesto", type="primary"):
    resultado = calcular_cotizacion_pvc(area, opcion_thermo)
    
    # 1. Totales Principales arriba (Visibilidad instantánea)
    st.markdown("### 💳 Resumen de Inversión")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            label="Total Base", 
            value=f"${resultado['total_base']:,.0f}"
        )
    with c2:
        st.metric(
            label="Total Sugerido", 
            value=f"${resultado['total_sugerido']:,.0f}",
            delta="Con reserva"
        )

    st.write("")

    # 2. Desglose desplegable (Para no saturar la pantalla móvil)
    with st.expander("📋 Ver Desglose Detallado de Materiales", expanded=True):
        df = pd.DataFrame(resultado["items"])
        
        # Formato de valores monetarios
        df_mostrar = df.copy()
        df_mostrar["P. Unitario"] = df_mostrar["P. Unitario"].apply(lambda x: f"${x:,.0f}")
        df_mostrar["Total Base"] = df_mostrar["Total Base"].apply(lambda x: f"${x:,.0f}")
        df_mostrar["Total Sugerido"] = df_mostrar["Total Sugerido"].apply(lambda x: f"${x:,.0f}")
        
        # Selector de columnas simplificado para celulares
        columnas_movil = ["Material", "Cant. Base", "Total Base"]
        st.dataframe(
            df_mostrar[columnas_movil], 
            use_container_width=True, 
            hide_index=True
        )

    # 3. Acciones rápidas (Generar texto limpio para compartir)
    resumen_texto = f"""*COTIZACIÓN CIELO RASO PVC ({area} m²)*
-----------------------------------
• Total Inversión Base: ${resultado['total_base']:,.0f} COP
• Total con Margen Sugerido: ${resultado['total_sugerido']:,.0f} COP
• Incluye Thermolon: {opcion_thermo}
-----------------------------------
*Generado automáticamente.*"""

    st.text_area("📱 Copiar resumen para enviar al cliente:", resumen_texto, height=130)