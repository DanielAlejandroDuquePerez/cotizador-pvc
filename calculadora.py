import math

def calcular_cotizacion_pvc(area_m2: float, tipo_thermolon: str = "Ninguno") -> dict:
    """
    Calcula cantidades y valores financieros (Base y Sugerido) 
    aplicando los precios unitarios del almacén.
    """
    # Precios unitarios
    PRECIOS = {
        "lamina": 27000,
        "perimetro": 16000,
        "omega": 4000,
        "vigueta": 4000,
        "angulo": 3000,
        "tornillo_lenteja": 40,
        "tornillo_estructura": 40,
        "puntilla": 10000,
        "thermolon_5mm": 8000,
        "thermolon_8mm": 11000
    }

    # 1. Cantidades
    lam_base = math.ceil(area_m2 / 1.785)
    lam_sug = lam_base + 3

    per_base = math.ceil((area_m2 * 1.3) / 6)
    per_sug = per_base + (3 if area_m2 > 50 else 2)

    ome_base = math.ceil(area_m2 * 0.80)
    ome_sug = ome_base + 5

    vig_base = math.ceil(ome_base / 2)
    vig_sug = vig_base + 5

    ang_base = math.ceil((area_m2 * 1.3) / 2.44)
    ang_sug = ang_base + 5

    tornillos_totales = math.ceil(area_m2 * 18)
    t_est_base = math.ceil(tornillos_totales / 2)
    t_len_base = math.ceil(tornillos_totales / 2)

    pun_base = 2 if area_m2 > 50 else 1

    # Determinación del Thermolon
    if tipo_thermolon == "5mm":
        precio_thermo = PRECIOS["thermolon_5mm"]
        cant_thermo = area_m2
    elif tipo_thermolon == "8mm":
        precio_thermo = PRECIOS["thermolon_8mm"]
        cant_thermo = area_m2
    else:
        precio_thermo = 0
        cant_thermo = 0

    # Construcción de la tabla de ítems
    items = [
        {"Material": "Láminas de PVC", "Cant. Base": lam_base, "Cant. Sugerida": lam_sug, "P. Unitario": PRECIOS["lamina"], "Total Base": lam_base * PRECIOS["lamina"], "Total Sugerido": lam_sug * PRECIOS["lamina"]},
        {"Material": "Perímetro / Moldura (6m)", "Cant. Base": per_base, "Cant. Sugerida": per_sug, "P. Unitario": PRECIOS["perimetro"], "Total Base": per_base * PRECIOS["perimetro"], "Total Sugerido": per_sug * PRECIOS["perimetro"]},
        {"Material": "Omegas", "Cant. Base": ome_base, "Cant. Sugerida": ome_sug, "P. Unitario": PRECIOS["omega"], "Total Base": ome_base * PRECIOS["omega"], "Total Sugerido": ome_sug * PRECIOS["omega"]},
        {"Material": "Viguetas", "Cant. Base": vig_base, "Cant. Sugerida": vig_sug, "P. Unitario": PRECIOS["vigueta"], "Total Base": vig_base * PRECIOS["vigueta"], "Total Sugerido": vig_sug * PRECIOS["vigueta"]},
        {"Material": "Ángulos (2.44m)", "Cant. Base": ang_base, "Cant. Sugerida": ang_sug, "P. Unitario": PRECIOS["angulo"], "Total Base": ang_base * PRECIOS["angulo"], "Total Sugerido": ang_sug * PRECIOS["angulo"]},
        {"Material": f"Thermolon ({tipo_thermolon})", "Cant. Base": cant_thermo, "Cant. Sugerida": cant_thermo, "P. Unitario": precio_thermo, "Total Base": cant_thermo * precio_thermo, "Total Sugerido": cant_thermo * precio_thermo},
        {"Material": "Tornillo Estructura", "Cant. Base": t_est_base, "Cant. Sugerida": t_est_base, "P. Unitario": PRECIOS["tornillo_estructura"], "Total Base": t_est_base * PRECIOS["tornillo_estructura"], "Total Sugerido": t_est_base * PRECIOS["tornillo_estructura"]},
        {"Material": "Tornillo Lenteja Aguda", "Cant. Base": t_len_base, "Cant. Sugerida": t_len_base, "P. Unitario": PRECIOS["tornillo_lenteja"], "Total Base": t_len_base * PRECIOS["tornillo_lenteja"], "Total Sugerido": t_len_base * PRECIOS["tornillo_lenteja"]},
        {"Material": "Puntilla (Lbs)", "Cant. Base": pun_base, "Cant. Sugerida": pun_base, "P. Unitario": PRECIOS["puntilla"], "Total Base": pun_base * PRECIOS["puntilla"], "Total Sugerido": pun_base * PRECIOS["puntilla"]},
    ]

    # Cálculos globales
    gran_total_base = sum(item["Total Base"] for item in items)
    gran_total_sugerido = sum(item["Total Sugerido"] for item in items)

    return {
        "items": items,
        "total_base": gran_total_base,
        "total_sugerido": gran_total_sugerido
    }