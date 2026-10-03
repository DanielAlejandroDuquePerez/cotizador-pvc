import io
import math
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def calcular_cotizacion_pvc(area: float, opcion_thermo: str = "Ninguno") -> dict:
    """Calcula la cantidad de materiales y costos para la instalación de cielo raso en PVC."""
    # Precios unitarios base
    PRECIOS = {
        "laminas": 27000,
        "perimetro": 16000,
        "omegas": 4000,
        "viguetas": 4000,
        "thermolon_5mm": 3500,
        "thermolon_8mm": 5000,
    }

    # Cálculos base de cantidades
    cant_laminas = math.ceil(area / 1.75)
    cant_perimetro = math.ceil((math.sqrt(area) * 4) / 6)
    cant_omegas = math.ceil(area * 0.8)
    cant_viguetas = math.ceil(area * 0.4)

    # Cantidades sugeridas (con adición/desperdicio)
    sug_laminas = math.ceil(cant_laminas * 1.10)
    sug_perimetro = math.ceil(cant_perimetro * 1.10)
    sug_omegas = math.ceil(cant_omegas * 1.05)
    sug_viguetas = math.ceil(cant_viguetas * 1.05)

    items = [
        {
            "Material": "Láminas de PVC",
            "Cant. Base": cant_laminas,
            "Cant. Sugerida": sug_laminas,
            "P. Unitario": PRECIOS["laminas"],
            "Total Base": cant_laminas * PRECIOS["laminas"],
            "Total Sugerido": sug_laminas * PRECIOS["laminas"],
        },
        {
            "Material": "Perímetro / Moldura (6m)",
            "Cant. Base": cant_perimetro,
            "Cant. Sugerida": sug_perimetro,
            "P. Unitario": PRECIOS["perimetro"],
            "Total Base": cant_perimetro * PRECIOS["perimetro"],
            "Total Sugerido": sug_perimetro * PRECIOS["perimetro"],
        },
        {
            "Material": "Omegas",
            "Cant. Base": cant_omegas,
            "Cant. Sugerida": sug_omegas,
            "P. Unitario": PRECIOS["omegas"],
            "Total Base": cant_omegas * PRECIOS["omegas"],
            "Total Sugerido": sug_omegas * PRECIOS["omegas"],
        },
        {
            "Material": "Viguetas",
            "Cant. Base": cant_viguetas,
            "Cant. Sugerida": sug_viguetas,
            "P. Unitario": PRECIOS["viguetas"],
            "Total Base": cant_viguetas * PRECIOS["viguetas"],
            "Total Sugerido": sug_viguetas * PRECIOS["viguetas"],
        },
    ]

    # Evaluación de aislante Thermolon
    if opcion_thermo == "5mm":
        precio_t = PRECIOS["thermolon_5mm"]
        cant_t = math.ceil(area)
        items.append({
            "Material": "Thermolon 5mm",
            "Cant. Base": cant_t,
            "Cant. Sugerida": cant_t,
            "P. Unitario": precio_t,
            "Total Base": cant_t * precio_t,
            "Total Sugerido": cant_t * precio_t,
        })
    elif opcion_thermo == "8mm":
        precio_t = PRECIOS["thermolon_8mm"]
        cant_t = math.ceil(area)
        items.append({
            "Material": "Thermolon 8mm",
            "Cant. Base": cant_t,
            "Cant. Sugerida": cant_t,
            "P. Unitario": precio_t,
            "Total Base": cant_t * precio_t,
            "Total Sugerido": cant_t * precio_t,
        })

    total_base = sum(item["Total Base"] for item in items)
    total_sugerido = sum(item["Total Sugerido"] for item in items)

    return {
        "items": items,
        "total_base": total_base,
        "total_sugerido": total_sugerido,
    }


def generar_excel_cotizacion(resultado: dict, area_m2: float) -> bytes:
    """Genera un archivo Excel (.xlsx) en memoria con el desglose de la cotización."""
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
    """Genera un archivo PDF ajustado en memoria con el desglose de la cotización."""
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

    t = Table(data, colWidths=[180, 60, 60, 75, 80, 80])
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