"""Nómina docente PITA.

Modelo corregido para distinguir los regímenes realmente aplicables:
- Docentes de PLANTA: Decreto 1279 de 2002 + valor del punto vigente 2026.
- Docentes OCASIONALES: Acuerdo UPC 027 de 2024, art. 24 (salario en SMMLV).
- Docentes CATEDRÁTICOS: Acuerdo UPC 027 de 2024, art. 23. El valor de la
  hora debe fijarse por resolución rectoral; no se inventa un valor 2026 si no
  está configurado expresamente.

Prestaciones sociales incluidas (normativa colombiana):
- Prima de servicios: art. 44 Decreto 1279/2002 → 30 días por año.
- Cesantías: art. 45 Decreto 1279/2002 → 30 días por año.
- Intereses a las cesantías: Ley 52/1975 → 12% anual (1% mensual) sobre
  las cesantías acumuladas.
- Prima de navidad: Decreto 1042/1978 art. 33 → 1 mes de sueldo por año.
- Vacaciones: Decreto 1279/2002 → 15 días hábiles remunerados por año;
  provisión mensual = bruto / 24.
- Prima de vacaciones: Decreto 1279/2002 art. 33 → 15 días por año
  (provisión mensual = bruto / 24).
- Bonificación por servicios prestados: Decreto 1279/2002 art. 39 →
  equivale a 2 meses de salario mensual; provisión = bruto * 2 / 12.

Aportes patronales (costo institucional de la UPC):
- Pensión patronal: 12% del salario bruto (Ley 100/1993, art. 20).
- Salud patronal: 8.5% del salario bruto (Ley 1122/2007, art. 10).
- ARL (riesgo I–II): 0.522% del salario bruto (Decreto 1295/1994).
- Caja de Compensación Familiar: 4% del salario bruto (Ley 21/1982).
Los aportes a seguridad social se redondean a pesos enteros (Decreto 1990/2016
y plataforma PILA).
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

# ── Tasas de aportes patronales (Decreto 1990/2016 → redondeo a pesos) ──────
TASA_PENSION_PATRONAL = 0.12       # Ley 100/1993 art. 20
TASA_SALUD_PATRONAL   = 0.085      # Ley 1122/2007 art. 10
TASA_ARL              = 0.00522    # Clase I-II, Decreto 1295/1994
TASA_CAJA_COMP        = 0.04       # Ley 21/1982

# ── Escala Salarial Oficial Empleados Públicos Administrativos ───────────────
# Basada en la estructura de cargos/niveles y decretos salariales del sector público:
# Nivel 1 (Asistencial/Auxiliar), Nivel 2 (Técnico/Secretarial),
# Nivel 3 (Profesional/Coordinador), Nivel 4 (Directivo/Asesor/Jefe de Oficina).
ESCALA_ADMINISTRATIVA_BASE = {
    "Nivel 1": 1950000.0,  # Asistencial / Auxiliares / Biblioteca
    "Nivel 2": 2800000.0,  # Técnico / Secretarios Académicos
    "Nivel 3": 3750000.0,  # Profesional Universitario / Coordinador
    "Nivel 4": 5050000.0,  # Asesor / Directivo / Jefe de Oficina
}


def salario_base_administrativo(categoria):
    """Obtiene el salario base según el nivel de la escala administrativa."""
    return ESCALA_ADMINISTRATIVA_BASE.get(categoria, 1950000.0)


def calcular_salario_bruto_admin(admin):
    """Calcula el salario bruto de un administrativo basado en la escala legal."""
    if hasattr(admin, "salario_base") and admin.salario_base > 0:
        return float(admin.salario_base)
    return salario_base_administrativo(getattr(admin, "categoria", "Nivel 1"))


def calcular_descuento_salud_admin(bruto):
    return round((bruto or 0.0) * 0.04)


def calcular_descuento_pension_admin(bruto):
    return round((bruto or 0.0) * 0.04)


def calcular_descuento_fsp_admin(bruto):
    b = bruto or 0.0
    if b >= (4.0 * SMMLV):
        return round(b * 0.01)
    return 0


def calcular_salario_neto_admin(admin):
    bruto = calcular_salario_bruto_admin(admin)
    return (bruto
            - calcular_descuento_salud_admin(bruto)
            - calcular_descuento_pension_admin(bruto)
            - calcular_descuento_fsp_admin(bruto))


def calcular_aportes_patronales_admin(bruto):
    b = bruto or 0.0
    pension = round(b * TASA_PENSION_PATRONAL)
    salud   = round(b * TASA_SALUD_PATRONAL)
    arl     = round(b * TASA_ARL)
    caja    = round(b * TASA_CAJA_COMP)
    return {
        "pension": pension,
        "salud":   salud,
        "arl":     arl,
        "caja":    caja,
        "total":   pension + salud + arl + caja,
    }


def calcular_costo_total_admin(admin):
    bruto = calcular_salario_bruto_admin(admin)
    return bruto + calcular_aportes_patronales_admin(bruto)["total"]


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


# ── Descuentos del empleado ──────────────────────────────────────────────────
# Los aportes a seguridad social se redondean a pesos enteros (Decreto 1990/2016).

def calcular_descuento_salud(salario_bruto):
    """4 % a cargo del empleado — Ley 100/1993, art. 204."""
    return round((salario_bruto or 0.0) * 0.04)


def calcular_descuento_pension(salario_bruto):
    """4 % a cargo del empleado — Ley 100/1993, art. 20."""
    return round((salario_bruto or 0.0) * 0.04)


def calcular_descuento_fsp(salario_bruto):
    """Fondo de Solidaridad Pensional (Ley 100/1993, Ley 797/2003).

    Aplica a salarios iguales o superiores a 4 SMMLV (1%).
    """
    b = salario_bruto or 0.0
    if b >= (4.0 * SMMLV):
        return round(b * 0.01)
    return 0


def calcular_salario_neto(profesor):
    bruto = calcular_salario_bruto(profesor)
    return (bruto
            - calcular_descuento_salud(bruto)
            - calcular_descuento_pension(bruto)
            - calcular_descuento_fsp(bruto))


# ── Prestaciones sociales (provisión mensual) ────────────────────────────────

def calcular_prima_servicios(salario_bruto):
    """Provisión mensual de la prima anual de servicios (30 días).

    Decreto 1279/2002 art. 44: prima anual equivalente a 1 mes de salario.
    Provisión mensual = salario / 12.
    """
    return (salario_bruto or 0.0) / 12.0


def calcular_cesantias(salario_bruto):
    """Provisión mensual de cesantías (1 mes por año).

    Decreto 1279/2002 art. 45 y Ley 50/1990: un mes de salario por año.
    Provisión mensual = salario / 12.
    """
    return (salario_bruto or 0.0) / 12.0


def calcular_intereses_cesantias(salario_bruto):
    """Provisión mensual de intereses sobre cesantías — Ley 52/1975.

    La Ley 52 ordena el 12% anual sobre el valor de las cesantías acumuladas,
    equivalente al 1% mensual. Interés mensual = cesantías_mensuales * 0.01
    = salario / 12 * 0.01 = salario / 1200.
    """
    return (salario_bruto or 0.0) / 1200.0


def calcular_prima_navidad(salario_bruto):
    """Provisión mensual de la prima de navidad (1 mes anual).

    Decreto 1042/1978, art. 33: todo servidor público tiene derecho a 1 mes
    de salario adicional en diciembre. Provisión mensual = salario / 12.
    """
    return (salario_bruto or 0.0) / 12.0


def calcular_vacaciones(salario_bruto):
    """Provisión mensual de vacaciones remuneradas.

    15 días hábiles remunerados por año. Aproximación estándar:
    provisión mensual = salario / 24.
    """
    return (salario_bruto or 0.0) / 24.0


def calcular_prima_vacaciones(salario_bruto):
    """Provisión mensual de la prima de vacaciones — Decreto 1279/2002 art. 33.

    Equivale a 15 días adicionales de salario al momento de las vacaciones.
    Provisión mensual = salario / 24.
    """
    return (salario_bruto or 0.0) / 24.0


def calcular_bonificacion_servicios(salario_bruto):
    """Provisión mensual de la bonificación por servicios prestados.

    Decreto 1279/2002, art. 39: equivale a 2 meses de salario mensual por año.
    Provisión mensual = salario * 2 / 12.
    """
    return (salario_bruto or 0.0) * 2.0 / 12.0


def calcular_total_prestaciones(salario_bruto):
    """Suma de todas las provisiones mensuales de prestaciones sociales."""
    return (calcular_prima_servicios(salario_bruto)
            + calcular_cesantias(salario_bruto)
            + calcular_intereses_cesantias(salario_bruto)
            + calcular_prima_navidad(salario_bruto)
            + calcular_vacaciones(salario_bruto)
            + calcular_prima_vacaciones(salario_bruto)
            + calcular_bonificacion_servicios(salario_bruto))


# ── Aportes patronales (costo de la institución) ─────────────────────────────
# Decreto 1990/2016: los aportes a seguridad social se redondean a pesos enteros.

def calcular_aportes_patronales(salario_bruto):
    """Retorna un dict con todos los aportes a cargo de la UPC.

    {
        'pension':  int,   # 12 %  Ley 100/1993 art. 20
        'salud':    int,   # 8.5 % Ley 1122/2007 art. 10
        'arl':      int,   # 0.522 % Clase I riesgo normal, Decreto 1295/1994
        'caja':     int,   # 4 %  Ley 21/1982
        'total':    int,   # suma de los anteriores
    }
    """
    b = salario_bruto or 0.0
    pension = round(b * TASA_PENSION_PATRONAL)
    salud   = round(b * TASA_SALUD_PATRONAL)
    arl     = round(b * TASA_ARL)
    caja    = round(b * TASA_CAJA_COMP)
    return {
        "pension": pension,
        "salud":   salud,
        "arl":     arl,
        "caja":    caja,
        "total":   pension + salud + arl + caja,
    }


def calcular_costo_total_empleador(profesor):
    """Costo directo UPC (Asignación Básica + Aportes Patronales).

    Es el total auditable directo reflejado en el desprendible oficial institucional:
    = Salario Bruto + Salud Patronal + Pensión Patronal + ARL + Caja Compensación.
    """
    bruto = calcular_salario_bruto(profesor)
    patronal = calcular_aportes_patronales(bruto)["total"]
    return bruto + patronal


def calcular_costo_con_prestaciones(profesor):
    """Costo total integral que incluye la provisión contable de prestaciones."""
    return calcular_costo_total_empleador(profesor) + calcular_total_prestaciones(calcular_salario_bruto(profesor))


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
        ap = calcular_aportes_patronales(bruto)
        print(f"Salario bruto          : ${bruto:,.0f}")
        print(f"(-) Salud empleado (4%): ${calcular_descuento_salud(bruto):,}")
        print(f"(-) Pensión empl. (4%) : ${calcular_descuento_pension(bruto):,}")
        print(f"Salario neto           : ${calcular_salario_neto(profesor):,.0f}")
        print("-- Prestaciones sociales (provisión mensual) --")
        print(f"Prima de servicios     : ${calcular_prima_servicios(bruto):,.0f}")
        print(f"Cesantías              : ${calcular_cesantias(bruto):,.0f}")
        print(f"Intereses cesantías    : ${calcular_intereses_cesantias(bruto):,.0f}")
        print(f"Prima de navidad       : ${calcular_prima_navidad(bruto):,.0f}")
        print(f"Vacaciones             : ${calcular_vacaciones(bruto):,.0f}")
        print(f"Prima de vacaciones    : ${calcular_prima_vacaciones(bruto):,.0f}")
        print(f"Bonif. servicios       : ${calcular_bonificacion_servicios(bruto):,.0f}")
        print("-- Aportes patronales (costo UPC) --")
        print(f"Pensión patronal (12%) : ${ap['pension']:,}")
        print(f"Salud patronal (8.5%)  : ${ap['salud']:,}")
        print(f"ARL (0.522%)           : ${ap['arl']:,}")
        print(f"Caja compensación (4%) : ${ap['caja']:,}")
        print(f"Total aportes patronal : ${ap['total']:,}")
        print(f"COSTO TOTAL EMPLEADOR  : ${calcular_costo_total_empleador(profesor):,.0f}")
    else:
        print("Salario                : NO LIQUIDADO (falta parámetro rectoral vigente)")
    print("------------------------------------------")
    print(observacion_normativa(profesor))
    print("===========================================")


