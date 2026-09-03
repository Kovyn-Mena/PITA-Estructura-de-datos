"""Nómina docente PITA.

Modelo corregido para distinguir los regímenes realmente aplicables:
- Docentes de PLANTA: Decreto 1279 de 2002 + valor del punto vigente 2026.
- Docentes OCASIONALES: Acuerdo UPC 027 de 2024, art. 24 (salario en SMMLV).
- Docentes CATEDRÁTICOS: Acuerdo UPC 027 de 2024, art. 23. El valor de la
  hora debe fijarse por resolución rectoral; no se inventa un valor 2026 si no
  está configurado expresamente.

El programa sigue siendo académico/simulado: los puntos por títulos y
productividad almacenados se interpretan como puntos ya reconocidos. El modelo
actual no guarda suficiente detalle para reconstruir por sí solo la evaluación
CIARP de experiencia/productividad ni las bonificaciones de los arts. 25 y 26.
"""

ANIO_NOMINA = 2026
VALOR_PUNTO = 23924.0       # Decreto 318 de 2026, art. 2
SMMLV = 1750905.0           # Decreto 159 de 2026 (vigente transitoriamente)
PUNTOS_PREGRADO = 178       # Decreto 1279 de 2002, art. 7 (regla general)

PUNTOS_POR_CATEGORIA = {
    "Auxiliar": 37,
    "Asistente": 58,
    "Asociado": 74,
    "Titular": 96,
}

# Acuerdo UPC 027 de 2024, art. 24.
FACTORES_OCASIONAL_SMMLV = {
    ("Auxiliar", "TiempoCompleto"): 2.645,
    ("Auxiliar", "MedioTiempo"): 1.509,
    ("Asistente", "TiempoCompleto"): 3.125,
    ("Asistente", "MedioTiempo"): 1.749,
    ("Asociado", "TiempoCompleto"): 3.606,
    ("Asociado", "MedioTiempo"): 1.990,
    ("Titular", "TiempoCompleto"): 3.918,
    ("Titular", "MedioTiempo"): 2.146,
}

# Acuerdo 027/2024 art. 23 ordena que el Rector fije por resolución el valor
# de la hora cátedra. Se deja configurable para no presentar como vigente un
# valor antiguo o proyectado. Puede cargarse cuando se tenga la resolución.
VALOR_HORA_CATEDRA = None


def puntos_por_categoria(categoria):
    return PUNTOS_POR_CATEGORIA.get(categoria, 0)


def regimen_nomina(profesor):
    if profesor.ad_honorem:
        return "Ad-honorem"
    if profesor.tipo_vinculacion == "Planta":
        return "Decreto 1279/2002"
    if profesor.tipo_vinculacion == "Ocasional":
        return "Acuerdo UPC 027/2024"
    if profesor.tipo_vinculacion == "Catedratico":
        return "Acuerdo UPC 027/2024 — hora cátedra"
    return "No definido"


def total_puntos(profesor):
    """Puntos usados únicamente para docentes de planta.

    Incluye los 178 puntos del título profesional de pregrado (regla general),
    categoría y los puntos ya reconocidos que están guardados en el registro.
    No transforma años de experiencia en puntos automáticamente porque el art.
    9 exige tipo de experiencia y evaluación del órgano competente.
    """
    if profesor.tipo_vinculacion != "Planta":
        return 0
    return (PUNTOS_PREGRADO
            + puntos_por_categoria(profesor.categoria_escalafon)
            + profesor.puntos_titulos
            + profesor.puntos_productividad)


def factor_proporcionalidad(profesor):
    """Proporcionalidad del Decreto 1279, solo relevante para planta."""
    if profesor.dedicacion == "TiempoCompleto":
        return 1.0
    if profesor.dedicacion == "MedioTiempo":
        return 0.5
    return 1.0


def factor_ocasional(profesor):
    return FACTORES_OCASIONAL_SMMLV.get(
        (profesor.categoria_escalafon, profesor.dedicacion)
    )


def calcular_salario_bruto(profesor):
    if profesor.ad_honorem:
        return 0.0

    if profesor.tipo_vinculacion == "Planta":
        return total_puntos(profesor) * VALOR_PUNTO * factor_proporcionalidad(profesor)

    if profesor.tipo_vinculacion == "Ocasional":
        factor = factor_ocasional(profesor)
        return (factor * SMMLV) if factor is not None else 0.0

    if profesor.tipo_vinculacion == "Catedratico":
        # El campo actual almacena horas semanales, mientras el Acuerdo 027
        # habla de horas mensuales asignadas. Sin valor rectoral vigente ni
        # horas mensuales exactas no se debe fabricar una liquidación.
        if VALOR_HORA_CATEDRA is None:
            return 0.0
        horas_mensuales_estimadas = profesor.horas_catedra_semanales * 4.0
        return horas_mensuales_estimadas * VALOR_HORA_CATEDRA

    return 0.0


def liquidacion_disponible(profesor):
    if profesor.ad_honorem:
        return True
    if profesor.tipo_vinculacion == "Catedratico" and VALOR_HORA_CATEDRA is None:
        return False
    if profesor.tipo_vinculacion == "Ocasional" and factor_ocasional(profesor) is None:
        return False
    return True


def observacion_normativa(profesor):
    if profesor.ad_honorem:
        return "Ad-honorem: prestación del servicio sin remuneración (Acuerdo 027/2024)."
    if profesor.tipo_vinculacion == "Planta":
        return ("Planta: Decreto 1279/2002. Los años de experiencia no se convierten "
                "automáticamente en puntos porque el art. 9 exige valoración según el tipo "
                "de experiencia. Los puntos guardados se tratan como ya reconocidos.")
    if profesor.tipo_vinculacion == "Ocasional":
        return ("Ocasional: salario base según categoría y dedicación del art. 24 del "
                "Acuerdo UPC 027/2024. No se suman bonificaciones de posgrado o grupo "
                "de investigación porque esos datos no existen en el modelo actual.")
    if profesor.tipo_vinculacion == "Catedratico":
        if VALOR_HORA_CATEDRA is None:
            return ("Catedrático: el art. 23 del Acuerdo UPC 027/2024 exige usar el valor "
                    "de hora fijado por resolución rectoral. No se encontró/configuró aquí "
                    "un valor rectoral 2026, por eso PITA no inventa el salario.")
        return "Catedrático: liquidación por horas conforme al art. 23 del Acuerdo 027/2024."
    return "Régimen no definido."


def calcular_descuento_salud(salario_bruto):
    return (salario_bruto or 0.0) * 0.04


def calcular_descuento_pension(salario_bruto):
    return (salario_bruto or 0.0) * 0.04


def calcular_salario_neto(profesor):
    bruto = calcular_salario_bruto(profesor)
    return bruto - calcular_descuento_salud(bruto) - calcular_descuento_pension(bruto)


def calcular_prima_servicios(salario_bruto):
    """Provisión mensual informativa de una prima anual equivalente a 30 días.

    Para planta, el art. 44 del Decreto 1279 reconoce una prima anual de 30
    días; salario/12 es su provisión mensual simplificada, no el pago del mes.
    """
    return (salario_bruto or 0.0) / 12.0


def calcular_cesantias(salario_bruto):
    return (salario_bruto or 0.0) / 12.0


def imprimir_desglose_nomina(profesor):
    bruto = calcular_salario_bruto(profesor)
    print(f"\n===== Desglose de nómina: {profesor.nombre_completo} =====")
    print(f"Régimen               : {regimen_nomina(profesor)}")
    print(f"Tipo de vinculación   : {profesor.tipo_vinculacion}")
    print(f"Dedicación            : {profesor.dedicacion}")

    if profesor.tipo_vinculacion == "Planta":
        print(f"Pregrado base          : {PUNTOS_PREGRADO} puntos")
        print(f"Categoría escalafón    : {profesor.categoria_escalafon} "
              f"({puntos_por_categoria(profesor.categoria_escalafon)} puntos)")
        print(f"Puntos títulos extra   : {profesor.puntos_titulos}")
        print(f"Puntos productividad   : {profesor.puntos_productividad}")
        print(f"Total puntos           : {total_puntos(profesor)}")
        print(f"Valor punto 2026       : ${VALOR_PUNTO:,.2f}")
    elif profesor.tipo_vinculacion == "Ocasional":
        print(f"Factor SMMLV           : {factor_ocasional(profesor)}")
        print(f"SMMLV 2026             : ${SMMLV:,.2f}")
    elif profesor.tipo_vinculacion == "Catedratico":
        print(f"Horas semanales        : {profesor.horas_catedra_semanales}")
        print(f"Valor hora configurado : {VALOR_HORA_CATEDRA}")

    print("------------------------------------------")
    if liquidacion_disponible(profesor):
        print(f"Salario bruto          : ${bruto:,.2f}")
        print(f"(-) Salud (4%)         : ${calcular_descuento_salud(bruto):,.2f}")
        print(f"(-) Pensión (4%)       : ${calcular_descuento_pension(bruto):,.2f}")
        print(f"Salario neto           : ${calcular_salario_neto(profesor):,.2f}")
    else:
        print("Salario                : NO LIQUIDADO (falta parámetro rectoral vigente)")
    print("------------------------------------------")
    print(observacion_normativa(profesor))
    print("===========================================")
