# Importar las funciones de exportación en la parte superior
from calculadora import (
    calcular_cotizacion_pvc, 
    generar_excel_cotizacion, 
    generar_pdf_cotizacion
)

# ... (resto de tu código de app.py) ...

if st.button("🚀 Calcular Presupuesto", type="primary"):
    resultado = calcular_cotizacion_pvc(area, opcion_thermo)
    
    # ... (código existente de métricas y tabla) ...

    # Botones de Descarga en 2 columnas
    st.markdown("### 📥 Descargar Documento")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        bytes_excel = generar_excel_cotizacion(resultado, area)
        st.download_button(
            label="📊 Descargar Excel",
            data=bytes_excel,
            file_name=f"cotizacion_pvc_{area}m2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_dl2:
        bytes_pdf = generar_pdf_cotizacion(resultado, area)
        st.download_button(
            label="📄 Descargar PDF",
            data=bytes_pdf,
            file_name=f"cotizacion_pvc_{area}m2.pdf",
            mime="application/pdf",
            use_container_width=True
        )