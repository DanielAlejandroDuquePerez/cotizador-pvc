import math
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def calcular_cotizacion_pvc(area: float, opcion_thermo: str = "Ninguno") -> dict:
    """Calcula la cantidad de materiales y costos para la instalación de cielo raso en PVC con precios actualizados."""
    # Precios unitarios actualizados según grabación
    PRECIO_LAMINA = 27000
    PRECIO_PERIMETRAL = 16000
    PRECIO_OMEGA = 4000
    PRECIO_VIGUETA = 4000
    PRECIO_ANGULO = 3000
    PRECIO_TORNILLO_LENTEJA = 40
    PRECIO_TORNILLO_ESTRUCTURA = 40
    PRECIO_PUNTILLA = 10000

    PRECIOS_THERMO = {
        "Ninguno": 0,
        "5mm": 8000,
        "8mm": 11000
    }
    PRECIO_CINTA = 12000

    # 1. Estructura y Perfiles
    cant_laminas_base = math.ceil(area / 1.75)
    perimetro_m = math.ceil(math.sqrt(area) * 4)
    cant_perimetral_base = math.ceil(perimetro_m / 6)
    cant_omegas_base = math.ceil(area * 0.8)
    cant_viguetas_base = math.ceil(area * 0.4)
    cant_angulos_base = math.ceil(perimetro_m / 6)
    cant_puntillas_base = math.ceil(area * 0.1)  # Libras o paquetes estimados según área

    # Cantidades sugeridas (con holgura y desperdicio)
    cant_laminas_sug = math.ceil(cant_laminas_base * 1.12)
    cant_perimetral_sug = math.ceil(cant_perimetral_base * 1.15)
    cant_omegas_sug = math.ceil(cant_omegas_base * 1.08)
    cant_viguetas_sug = math.ceil(cant_viguetas_base * 1.08)
    cant_angulos_sug = math.ceil(cant_angulos_base * 1.10)
    cant_puntillas_sug = math.ceil(cant_puntillas_base * 1.10)

    # 2. Tornillería (Fórmula: área * 18 repartido mitad y mitad)
    total_tornillos_base = math.ceil(area * 18)
    mitad_tornillos_base = math.ceil(total_tornillos_base / 2)

    cant_lenteja_base = mitad_tornillos_base
    cant_lenteja_sug = math.ceil(cant_lenteja_base * 1.10)

    cant_estructura_base = mitad_tornillos_base
    cant_estructura_sug = math.ceil(cant_estructura_base * 1.10)

    # 3. Lista de Items
    items = [
        {
            "Material": "Láminas de PVC",
            "Cant. Base": cant_laminas_base,
            "Cant. Sugerida": cant_laminas_sug,
            "P. Unitario": PRECIO_LAMINA,
            "Total Base": cant_laminas_base * PRECIO_LAMINA,
            "Total Sugerido": cant_laminas_sug * PRECIO_LAMINA,
        },
        {
            "Material": "Perimetral / Moldura (6m)",
            "Cant. Base": cant_perimetral_base,
            "Cant. Sugerida": cant_perimetral_sug,
            "P. Unitario": PRECIO_PERIMETRAL,
            "Total Base": cant_perimetral_base * PRECIO_PERIMETRAL,
            "Total Sugerido": cant_perimetral_sug * PRECIO_PERIMETRAL,
        },
        {
            "Material": "Omegas",
            "Cant. Base": cant_omegas_base,
            "Cant. Sugerida": cant_omegas_sug,
            "P. Unitario": PRECIO_OMEGA,
            "Total Base": cant_omegas_base * PRECIO_OMEGA,
            "Total Sugerido": cant_omegas_sug * PRECIO_OMEGA,
        },
        {
            "Material": "Viguetas",
            "Cant. Base": cant_viguetas_base,
            "Cant. Sugerida": cant_viguetas_sug,
            "P. Unitario": PRECIO_VIGUETA,
            "Total Base": cant_viguetas_base * PRECIO_VIGUETA,
            "Total Sugerido": cant_viguetas_sug * PRECIO_VIGUETA,
        },
        {
            "Material": "Ángulo",
            "Cant. Base": cant_angulos_base,
            "Cant. Sugerida": cant_angulos_sug,
            "P. Unitario": PRECIO_ANGULO,
            "Total Base": cant_angulos_base * PRECIO_ANGULO,
            "Total Sugerido": cant_angulos_sug * PRECIO_ANGULO,
        },
        {
            "Material": "Tornillo Lenteja Aguda",
            "Cant. Base": cant_lenteja_base,
            "Cant. Sugerida": cant_lenteja_sug,
            "P. Unitario": PRECIO_TORNILLO_LENTEJA,
            "Total Base": cant_lenteja_base * PRECIO_TORNILLO_LENTEJA,
            "Total Sugerido": cant_lenteja_sug * PRECIO_TORNILLO_LENTEJA,
        },
        {
            "Material": "Tornillo Estructura",
            "Cant. Base": cant_estructura_base,
            "Cant. Sugerida": cant_estructura_sug,
            "P. Unitario": PRECIO_TORNILLO_ESTRUCTURA,
            "Total Base": cant_estructura_base * PRECIO_TORNILLO_ESTRUCTURA,
            "Total Sugerido": cant_estructura_sug * PRECIO_TORNILLO_ESTRUCTURA,
        },
        {
            "Material": "Puntilla",
            "Cant. Base": cant_puntillas_base,
            "Cant. Sugerida": cant_puntillas_sug,
            "P. Unitario": PRECIO_PUNTILLA,
            "Total Base": cant_puntillas_base * PRECIO_PUNTILLA,
            "Total Sugerido": cant_puntillas_sug * PRECIO_PUNTILLA,
        },
    ]

    # Evaluación de Thermolon
    precio_thermo_m2 = PRECIOS_THERMO.get(opcion_thermo, 0)
    if precio_thermo_m2 > 0:
        cant_thermo_base = math.ceil(area)
        cant_thermo_sug = math.ceil(area * 1.05)

        items.append({
            "Material": f"Thermolon ({opcion_thermo})",
            "Cant. Base": cant_thermo_base,
            "Cant. Sugerida": cant_thermo_sug,
            "P. Unitario": precio_thermo_m2,
            "Total Base": cant_thermo_base * precio_thermo_m2,
            "Total Sugerido": cant_thermo_sug * precio_thermo_m2,
        })

        cant_cinta = math.ceil(area / 30)
        items.append({
            "Material": "Cinta para Thermolon (Rollo)",
            "Cant. Base": cant_cinta,
            "Cant. Sugerida": cant_cinta,
            "P. Unitario": PRECIO_CINTA,
            "Total Base": cant_cinta * PRECIO_CINTA,
            "Total Sugerido": cant_cinta * PRECIO_CINTA,
        })

    # Totales globales
    total_base = sum(item["Total Base"] for item in items)
    total_sugerido = sum(item["Total Sugerido"] for item in items)

    return {
        "items": items,
        "total_base": total_base,
        "total_sugerido": total_sugerido,
    }


def generar_excel_cotizacion(resultado: dict, area_m2: float) -> bytes:
    """Genera un archivo Excel (.xlsx) en memoria."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Cotización"

    ws.append(["COTIZACIÓN DE CIELO RASO EN PVC"])
    ws.append([f"Área a cubrir: {area_m2} m²"])
    ws.append([])
    ws.append(["Material", "Cant. Base", "Cant. Sugerida", "P. Unitario", "Total Base", "Total Sugerido"])

    for item in resultado["items"]:
        ws.append([
            item["Material"],
            item["Cant. Base"],
            item["Cant. Sugerida"],
            item["P. Unitario"],
            item["Total Base"],
            item["Total Sugerido"]
        ])

    ws.append([])
    ws.append(["TOTAL BASE", "", "", "", "", resultado["total_base"]])
    ws.append(["TOTAL CON ADICIONES", "", "", "", "", resultado["total_sugerido"]])

    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def generar_pdf_cotizacion(resultado: dict, area_m2: float) -> bytes:
    """Genera un archivo PDF ajustado en memoria."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor("#1e293b"))
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#64748b"))

    elements.append(Paragraph("<b>COTIZACIÓN CIELO RASO EN PVC</b>", title_style))
    elements.append(Paragraph(f"Área a cubrir: {area_m2} m²", subtitle_style))
    elements.append(Spacer(1, 12))

    data = [["Material", "Cant. Base", "Cant. Sug.", "P. Unitario", "Total Base", "Total Sug."]]
    for item in resultado["items"]:
        data.append([
            item["Material"],
            str(item["Cant. Base"]),
            str(item["Cant. Sugerida"]),
            f"${item['P. Unitario']:,}",
            f"${item['Total Base']:,}",
            f"${item['Total Sugerido']:,}"
        ])

    data.append(["TOTALES", "", "", "", f"${resultado['total_base']:,}", f"${resultado['total_sugerido']:,}"])

    t = Table(data, colWidths=[170, 55, 55, 70, 85, 85])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#f1f5f9")),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))

    elements.append(t)
    doc.build(elements)
    return buffer.getvalue()