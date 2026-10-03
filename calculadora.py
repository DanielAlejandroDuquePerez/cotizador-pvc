import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_excel_cotizacion(resultado: dict, area_m2: float) -> bytes:
    """Genera un archivo Excel (.xlsx) en memoria con el desglose de la cotización."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Cotización"

    # Encabezados
    ws.append(["COTIZACIÓN DE CIELO RASO EN PVC"])
    ws.append([f"Área a cubrir: {area_m2} m²"])
    ws.append([])
    ws.append(["Material", "Cant. Base", "Cant. Sugerida", "P. Unitario", "Total Base", "Total Sugerido"])

    # Filas de ítems
    for item in resultado["items"]:
        ws.append([
            item["Material"],
            item["Cant. Base"],
            item["Cant. Sugerida"],
            item["P. Unitario"],
            item["Total Base"],
            item["Total Sugerido"]
        ])

    # Totales
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

    # Construcción de la tabla
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