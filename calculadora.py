import math
import io
import pandas as pd

def calcular_cotizacion_pvc(area: float, opcion_thermo: str):
    # Precios unitarios
    PRECIO_LAMINA = 27000
    PRECIO_MOLDURA = 16000
    PRECIO_OMEGA = 4000
    PRECIO_VIGUETA = 4000
    PRECIO_TORNILLO_LENTEJA = 50   # Tornillo Avena / Lenteja
    PRECIO_TORNILLO_ESTRUCTURA = 150 # Tornillo Estructura / Concreto
    
    PRECIOS_THERMO = {
        "Ninguno": 0,
        "5mm": 3500,
        "8mm": 5000
    }
    PRECIO_CINTA = 12000

    # 1. Estructura y Perfiles
    cant_laminas_base = math.ceil(area / 1.75)
    perimetro_m = math.ceil(math.sqrt(area) * 4)
    cant_moldura_base = math.ceil(perimetro_m / 6)
    cant_omegas_base = math.ceil(area * 0.8)
    cant_viguetas_base = math.ceil(area * 0.4)

    cant_laminas_sug = math.ceil(cant_laminas_base * 1.12)
    cant_moldura_sug = math.ceil(cant_moldura_base * 1.15)
    cant_omegas_sug = math.ceil(cant_omegas_base * 1.08)
    cant_viguetas_sug = math.ceil(cant_viguetas_base * 1.08)

    # 2. Tornillería (Fórmula: Área * 18, repartido mitad y mitad)
    total_tornillos_base = math.ceil(area * 18)
    mitad_tornillos_base = math.ceil(total_tornillos_base / 2)  # área * 9

    cant_lenteja_base = mitad_tornillos_base
    cant_lenteja_sug = math.ceil(cant_lenteja_base * 1.10)  # +10% de margen

    cant_estructura_base = mitad_tornillos_base
    cant_estructura_sug = math.ceil(cant_estructura_base * 1.10)  # +10% de margen

    # 3. Lista de Items
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
            "Material": "Tornillo Lenteja / Avena",
            "Cant. Base": cant_lenteja_base,
            "Cant. Sugerida": cant_lenteja_sug,
            "P. Unitario": PRECIO_TORNILLO_LENTEJA,
            "Total Base": cant_lenteja_base * PRECIO_TORNILLO_LENTEJA,
            "Total Sugerido": cant_lenteja_sug * PRECIO_TORNILLO_LENTEJA
        },
        {
            "Material": "Tornillo Estructura / Concreto",
            "Cant. Base": cant_estructura_base,
            "Cant. Sugerida": cant_estructura_sug,
            "P. Unitario": PRECIO_TORNILLO_ESTRUCTURA,
            "Total Base": cant_estructura_base * PRECIO_TORNILLO_ESTRUCTURA,
            "Total Sugerido": cant_estructura_sug * PRECIO_TORNILLO_ESTRUCTURA
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