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

# Acuerdo UPC 027 de 2024: Bonificación económica mensual por cualificación en postgrado
FACTORES_BONIFICACION_POSGRADO = {
    "Especializacion": 0.10,
    "Maestria": 0.45,
    "Doctorado": 0.90,
}

# Estampilla Pro-Universidad Popular del Cesar (0.2% sobre salario básico)
TASA_ESTAMPILLA = 0.002

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


def redondear_pesos(valor):
    """Redondeo aritmético estándar al peso entero más cercano."""
    return round((valor or 0.0) + 1e-6)


def calcular_salario_bruto(profesor):
    if profesor.ad_honorem:
        return 0.0

    if profesor.tipo_vinculacion == "Planta":
        return redondear_pesos(total_puntos(profesor) * VALOR_PUNTO * factor_proporcionalidad(profesor))

    if profesor.tipo_vinculacion == "Ocasional":
        factor = factor_ocasional(profesor)
        return redondear_pesos(factor * SMMLV) if factor is not None else 0.0

    if profesor.tipo_vinculacion == "Catedratico":
        if VALOR_HORA_CATEDRA is None:
            return 0.0
        horas_mensuales_estimadas = profesor.horas_catedra_semanales * 4.0
        return redondear_pesos(horas_mensuales_estimadas * VALOR_HORA_CATEDRA)

    return 0.0


def calcular_bonificacion_posgrado(profesor):
    """Bonificación mensual adicional por cualificación en postgrado.

    Acuerdo UPC 027 de 2024 (Especialización: 0.10 SMMLV, Maestría: 0.45 SMMLV,
    Doctorado: 0.90 SMMLV).
    Aplica a docentes ocasionales y catedráticos. No constituye factor salarial
    para la liquidación de prestaciones sociales ni parafiscales.
    """
    if getattr(profesor, "ad_honorem", False) or profesor.tipo_vinculacion == "Planta":
        return 0.0
    posgrado = getattr(profesor, "posgrado", "")
    factor = FACTORES_BONIFICACION_POSGRADO.get(posgrado, 0.0)
    if factor <= 0.0:
        return 0.0
    if profesor.tipo_vinculacion == "Catedratico":
        horas = getattr(profesor, "horas_catedra_semanales", 0) * 4.0
        return redondear_pesos((factor * SMMLV) * (horas / 40.0))
    return redondear_pesos(factor * SMMLV)


def calcular_total_devengado(profesor):
    """Total devengado mensual = Salario básico + Bonificación por postgrado."""
    return calcular_salario_bruto(profesor) + calcular_bonificacion_posgrado(profesor)


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
        posg = getattr(profesor, "posgrado", "")
        det_posg = f" con bonificación por {posg} (Acuerdo 027/2024)" if posg else ""
        return (f"Ocasional: salario base según categoría y dedicación del art. 24 del "
                f"Acuerdo UPC 027/2024{det_posg}.")
    if profesor.tipo_vinculacion == "Catedratico":
        if VALOR_HORA_CATEDRA is None:
            return ("Catedrático: el art. 23 del Acuerdo UPC 027/2024 exige usar el valor "
                    "de hora fijado por resolución rectoral. No se encontró/configuró aquí "
                    "un valor rectoral 2026, por eso PITA no inventa el salario.")
        return "Catedrático: liquidación por horas conforme al art. 23 del Acuerdo 027/2024."
    return "Régimen no definido."


# ── Descuentos del empleado ──────────────────────────────────────────────────
# Conforme a la plataforma PILA y Decreto 1990/2016, los aportes a seguridad social
# se aproximan al múltiplo de 100 más cercano.

def calcular_descuento_salud(salario_bruto):
    """4 % a cargo del empleado — Ley 100/1993 art. 204 (redondeo a centena PILA)."""
    b = salario_bruto or 0.0
    return round(((b * 0.04) / 100.0) + 1e-6) * 100


def calcular_descuento_pension(salario_bruto):
    """4 % a cargo del empleado — Ley 100/1993 art. 20 (redondeo a centena PILA)."""
    b = salario_bruto or 0.0
    return round(((b * 0.04) / 100.0) + 1e-6) * 100


def calcular_descuento_fsp(salario_bruto):
    """Fondo de Solidaridad Pensional (Ley 100/1993, Ley 797/2003).

    Aplica si el salario básico (IBC) es >= 4 SMMLV (1%).
    """
    b = salario_bruto or 0.0
    if b >= (4.0 * SMMLV):
        return round(((b * 0.01) / 100.0) + 1e-6) * 100
    return 0


def calcular_descuento_estampilla(salario_bruto):
    """Descuento Estampilla Pro-UPC (0.2% sobre salario básico)."""
    return redondear_pesos((salario_bruto or 0.0) * TASA_ESTAMPILLA)


def calcular_retencion_fuente(total_devengado, salud, pension):
    """Retención en la fuente por salarios (Art. 383 Estatuto Tributario).

    Renta de trabajo con deducción del 25% exenta legal (Art. 206 num. 10 E.T.).
    Aplica el 19% sobre el excedente del umbral de 95 UVT (~$4.975.000),
    redondeado al múltiplo de 1.000 más cercano (norma DIAN).
    """
    base_gravable = ((total_devengado or 0.0) - salud - pension) * 0.75
    umbral = 4975000.0  # Umbral de 95 UVT en 2026
    if base_gravable > umbral:
        impuesto = (base_gravable - umbral) * 0.19
        return round((impuesto / 1000.0) + 1e-6) * 1000
    return 0


def calcular_total_deducciones(profesor):
    """Suma de todas las deducciones de nómina del docente."""
    bruto = calcular_salario_bruto(profesor)
    devengado = calcular_total_devengado(profesor)
    salud = calcular_descuento_salud(bruto)
    pension = calcular_descuento_pension(bruto)
    fsp = calcular_descuento_fsp(bruto)
    estampilla = calcular_descuento_estampilla(bruto)
    retencion = calcular_retencion_fuente(devengado, salud, pension)
    return salud + pension + fsp + estampilla + retencion


def calcular_salario_neto(profesor):
    return calcular_total_devengado(profesor) - calcular_total_deducciones(profesor)


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
    bonif_posg = calcular_bonificacion_posgrado(profesor)
    devengado = calcular_total_devengado(profesor)

    salud = calcular_descuento_salud(bruto)
    pension = calcular_descuento_pension(bruto)
    fsp = calcular_descuento_fsp(bruto)
    estampilla = calcular_descuento_estampilla(bruto)
    retencion = calcular_retencion_fuente(devengado, salud, pension)
    total_ded = salud + pension + fsp + estampilla + retencion
    neto = devengado - total_ded

    print(f"\n=================================================================")
    print(f"      DESPRENDIBLE OFICIAL DE PAGO DE NOMINA DOCENTE (UPC)       ")
    print(f"=================================================================")
    print(f"Docente               : {profesor.nombre_completo} (ID: {profesor.identificacion})")
    print(f"Modalidad / Régimen   : {profesor.tipo_vinculacion} ({regimen_nomina(profesor)})")
    print(f"Dedicación            : {profesor.dedicacion}")
    if getattr(profesor, "posgrado", ""):
        print(f"Cualificación Postg.  : {profesor.posgrado}")

    if not liquidacion_disponible(profesor):
        print("\n[!] SALARIO NO LIQUIDADO: Falta resolución rectoral de hora cátedra.")
        print("=================================================================")
        return

    print("\n--- DEVENGADOS Y ASIGNACIONES (+) ---")
    print(f"SUELDO (Básico)       : ${bruto:,.0f} COP")
    if bonif_posg > 0:
        print(f"BONIF. CUALIF. POSTG. : ${bonif_posg:,.0f} COP (Acuerdo UPC 027/2024)")
    print(f"Total Devengados      : ${devengado:,.0f} COP")

    print(f"\n--- DEDUCIDOS (-) [Total Deducciones: ${total_ded:,.0f} COP] ---")
    print(f"DESCUENTO ESTAMPILLA  : -${estampilla:,.0f} COP (0.2% Pro-UPC)")
    if retencion > 0:
        print(f"RETENCION EN LA FUENTE: -${retencion:,.0f} COP (Art. 383 E.T.)")
    print(f"APORTE PENSION EMPL.  : -${pension:,.0f} COP (4% base sueldo, PILA)")
    print(f"APORTE SALUD EMPLEADO : -${salud:,.0f} COP (4% base sueldo, PILA)")
    if fsp > 0:
        print(f"FONDO SOLIDARIDAD PENS: -${fsp:,.0f} COP (1% IBC >= 4 SMMLV)")
    print(f"Total Deducidos       : -${total_ded:,.0f} COP")

    ap = calcular_aportes_patronales(bruto)
    print("\n--- APORTES PATRONALES (COSTO INSTITUCIONAL UPC) ---")
    print(f"Pensión patronal (12%): ${ap['pension']:,} COP")
    print(f"Salud patronal (8.5%) : ${ap['salud']:,} COP")
    print(f"ARL (0.522%)          : ${ap['arl']:,} COP")
    print(f"Caja compensación (4%): ${ap['caja']:,} COP")
    print(f"Costo Total Empleador : ${calcular_costo_total_empleador(profesor):,.0f} COP")

    print("\n=================================================================")
    print(f">>> NETO A PAGAR DOCENTE: ${neto:,.0f} COP <<<")
    print("=================================================================")
    print(observacion_normativa(profesor))
    print("=================================================================")


def imprimir_desglose_nomina_admin(admin):
    """Genera e imprime en consola el desprendible oficial de nómina del personal administrativo."""
    bruto = calcular_salario_bruto_admin(admin)
    salud = calcular_descuento_salud_admin(bruto)
    pension = calcular_descuento_pension_admin(bruto)
    fsp = calcular_descuento_fsp_admin(bruto)
    total_ded = salud + pension + fsp
    neto = bruto - total_ded
    ap = calcular_aportes_patronales_admin(bruto)
    costo_upc = bruto + ap["total"]

    print(f"\n=================================================================")
    print(f"    DESPRENDIBLE OFICIAL DE PAGO PERSONAL ADMINISTRATIVO (UPC)   ")
    print(f"=================================================================")
    print(f"Funcionario           : {admin.nombre_completo} (ID: {admin.identificacion})")
    print(f"Cargo / Nivel         : {admin.cargo} ({admin.categoria})")
    print(f"Tipo de Contratación  : {admin.tipo_contratacion}")
    fac = admin.codigo_facultad if admin.codigo_facultad else "Nivel Central"
    print(f"Adscrito a            : {fac}")

    print(f"\n--- DEVENGADOS Y ASIGNACIONES (+) ---")
    print(f"Asignación Salarial   : ${bruto:,.0f} COP ({admin.categoria} - Decretos Salariales 2026)")

    print(f"\n--- DEDUCCIONES OBLIGATORIAS DE LEY (-) [Total: -${total_ded:,.0f} COP] ---")
    print(f"IBC Seguridad Social  : ${bruto:,.0f} COP")
    print(f"(-) Salud (4%)        : -${salud:,.0f} COP")
    print(f"(-) Pensión (4%)      : -${pension:,.0f} COP")
    if fsp > 0:
        print(f"(-) FSP (1%)          : -${fsp:,.0f} COP (salario >= 4 SMMLV)")
    else:
        print(f"    FSP (1%)          : $0 COP (no supera 4 SMMLV)")

    print(f"\n--- COSTO TOTAL EMPLEADOR (UPC) [Total: ${costo_upc:,.0f} COP] ---")
    print(f"Asignación Básica     : ${bruto:,.0f} COP")
    print(f"Salud Patronal (8.5%) : ${ap['salud']:,} COP")
    print(f"Pensión Patronal (12%): ${ap['pension']:,} COP")
    print(f"ARL (0.522%)          : ${ap['arl']:,} COP")
    print(f"Caja Compensación (4%): ${ap['caja']:,} COP")

    print(f"\n=================================================================")
    print(f">>> NETO A PAGAR FUNCIONARIO: ${neto:,.0f} COP <<<")
    print(f"=================================================================")


