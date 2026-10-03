import math
import io
import pandas as pd

def calcular_cotizacion_pvc(area: float, opcion_thermo: str):
    # Precios unitarios base
    PRECIO_LAMINA = 27000       # Rendimiento aprox: 1.75 m² por lámina
    PRECIO_MOLDURA = 16000      # Tira de 6m
    PRECIO_OMEGA = 4000         # Perfil Omega
    PRECIO_VIGUETA = 4000       # Perfil Vigueta
    PRECIO_TORNILLO_AVENA = 50  # Ensamble metal-metal / lámina
    PRECIO_TORNILLO_CHAZO = 150 # Fijación a placa/concreto
    
    PRECIOS_THERMO = {
        "Ninguno": 0,
        "5mm": 3500,  # precio por m²
        "8mm": 5000   # precio por m²
    }
    PRECIO_CINTA = 12000       # Rollo de cinta para aislamiento

    # 1. Cálculos de Estructura Principal
    cant_laminas_base = math.ceil(area / 1.75)
    perimetro_m = math.ceil(math.sqrt(area) * 4)
    cant_moldura_base = math.ceil(perimetro_m / 6)
    cant_omegas_base = math.ceil(area * 0.8)
    cant_viguetas_base = math.ceil(area * 0.4)

    # Cantidades sugeridas para estructura (con holgura)
    cant_laminas_sug = math.ceil(cant_laminas_base * 1.12)
    cant_moldura_sug = math.ceil(cant_moldura_base * 1.15)
    cant_omegas_sug = math.ceil(cant_omegas_base * 1.08)
    cant_viguetas_sug = math.ceil(cant_viguetas_base * 1.08)

    # 2. Cálculos de Tornillería (Distribución Mitad y Mitad)
    # Total de tornillos de estructura (Avena / Lenteja)
    total_tornillos_avena = math.ceil(area * 20)
    cant_tornillos_avena_base = math.ceil(total_tornillos_avena / 2)
    cant_tornillos_avena_sug = total_tornillos_avena  # La otra mitad completa el total con margen

    # Total de tornillos para concreto / chazos
    total_tornillos_chazo = math.ceil(area * 8)
    cant_tornillos_chazo_base = math.ceil(total_tornillos_chazo / 2)
    cant_tornillos_chazo_sug = total_tornillos_chazo  # La otra mitad completa el total con margen

    # 3. Construcción de la Lista de ítems
    items = [
        {
            "Material": "Láminas de PVC",
            "Cant. Base": cant_laminas_base,
            "Cant. Sugerida": cant_laminas_sug,
            "P. Unitario": PRECIO_LAMINA,
            "Total Base": cant_laminas_base * PRECIO_LAMINA,
            "Total Sugerido": cant_laminas_sug * PRECIO_LAMINA
        },
        {
            "Material": "Perímetro / Moldura (6m)",
            "Cant. Base": cant_moldura_base,
            "Cant. Sugerida": cant_moldura_sug,
            "P. Unitario": PRECIO_MOLDURA,
            "Total Base": cant_moldura_base * PRECIO_MOLDURA,
            "Total Sugerido": cant_moldura_sug * PRECIO_MOLDURA
        },
        {
            "Material": "Omegas",
            "Cant. Base": cant_omegas_base,
            "Cant. Sugerida": cant_omegas_sug,
            "P. Unitario": PRECIO_OMEGA,
            "Total Base": cant_omegas_base * PRECIO_OMEGA,
            "Total Sugerido": cant_omegas_sug * PRECIO_OMEGA
        },
        {
            "Material": "Viguetas",
            "Cant. Base": cant_viguetas_base,
            "Cant. Sugerida": cant_viguetas_sug,
            "P. Unitario": PRECIO_VIGUETA,
            "Total Base": cant_viguetas_base * PRECIO_VIGUETA,
            "Total Sugerido": cant_viguetas_sug * PRECIO_VIGUETA
        },
        {
            "Material": "Tornillos Avena / Lenteja (Estructura)",
            "Cant. Base": cant_tornillos_avena_base,
            "Cant. Sugerida": cant_tornillos_avena_sug,
            "P. Unitario": PRECIO_TORNILLO_AVENA,
            "Total Base": cant_tornillos_avena_base * PRECIO_TORNILLO_AVENA,
            "Total Sugerido": cant_tornillos_avena_sug * PRECIO_TORNILLO_AVENA
        },
        {
            "Material": "Tornillos para Concreto / Chazos",
            "Cant. Base": cant_tornillos_chazo_base,
            "Cant. Sugerida": cant_tornillos_chazo_sug,
            "P. Unitario": PRECIO_TORNILLO_CHAZO,
            "Total Base": cant_tornillos_chazo_base * PRECIO_TORNILLO_CHAZO,
            "Total Sugerido": cant_tornillos_chazo_sug * PRECIO_TORNILLO_CHAZO
        }
    ]

    # Evaluación de Thermolon
    precio_thermo_m2 = PRECIOS_THERMO.get(opcion_thermo, 0)
    if precio_thermo_m2 > 0:
        cant_thermo_base = math.ceil(area)
        cant_thermo_sug = math.ceil(area * 1.05)
        
        items.append({
            "Material": f"Aislante Thermolon ({opcion_thermo})",
            "Cant. Base": cant_thermo_base,
            "Cant. Sugerida": cant_thermo_sug,
            "P. Unitario": precio_thermo_m2,
            "Total Base": cant_thermo_base * precio_thermo_m2,
            "Total Sugerido": cant_thermo_sug * precio_thermo_m2
        })
        
        cant_cinta = math.ceil(area / 30)
        items.append({
            "Material": "Cinta para Thermolon (Rollo)",
            "Cant. Base": cant_cinta,
            "Cant. Sugerida": cant_cinta,
            "P. Unitario": PRECIO_CINTA,
            "Total Base": cant_cinta * PRECIO_CINTA,
            "Total Sugerido": cant_cinta * PRECIO_CINTA
        })

    # Totales globales
    total_base = sum(item["Total Base"] for item in items)
    total_sugerido = sum(item["Total Sugerido"] for item in items)

    return {
        "items": items,
        "total_base": total_base,
        "total_sugerido": total_sugerido
    }

def generar_excel_cotizacion(resultado, area):
    output = io.BytesIO()
    df = pd.DataFrame(resultado["items"])
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cotizacion", index=False)
    return output.getvalue()

def generar_pdf_cotizacion(resultado, area):
    output = io.BytesIO()
    output.write(b"%PDF-1.4 ... Cotizacion PDF ...")
    return output.getvalue()