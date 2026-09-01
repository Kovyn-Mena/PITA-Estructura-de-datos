"""Modelo salarial simulado, basado en el Decreto 1279 de 2002 y el
Acuerdo 027 de 2024 (UPC). Ver docs/formato_persistencia.md y el documento
de diseno para el detalle normativo."""

# Parametro configurable, NO hardcodear en la logica de calculo.
# Referencia historica: $20.895 COP para el ano 2024.
VALOR_PUNTO = 20895.0

PUNTOS_POR_CATEGORIA = {
    "Auxiliar": 37,
    "Asistente": 58,
    "Asociado": 74,
    "Titular": 96,
}


def puntos_por_categoria(categoria):
    return PUNTOS_POR_CATEGORIA.get(categoria, 0)


def total_puntos(profesor):
    return (puntos_por_categoria(profesor.categoria_escalafon)
            + profesor.puntos_titulos
            + profesor.puntos_productividad)


def factor_proporcionalidad(profesor):
    if profesor.dedicacion == "TiempoCompleto":
        return 1.0
    if profesor.dedicacion == "MedioTiempo":
        return 0.5
    if profesor.dedicacion == "HorasCatedra":
        return profesor.horas_catedra_semanales / 18.0
    return 1.0


def calcular_salario_bruto(profesor):
    if profesor.ad_honorem:
        return 0.0
    return total_puntos(profesor) * VALOR_PUNTO * factor_proporcionalidad(profesor)


def calcular_descuento_salud(salario_bruto):
    return salario_bruto * 0.04


def calcular_descuento_pension(salario_bruto):
    return salario_bruto * 0.04


def calcular_salario_neto(profesor):
    bruto = calcular_salario_bruto(profesor)
    return bruto - calcular_descuento_salud(bruto) - calcular_descuento_pension(bruto)


def calcular_prima_servicios(salario_bruto):
    return salario_bruto / 12.0


def calcular_cesantias(salario_bruto):
    return salario_bruto / 12.0


def imprimir_desglose_nomina(profesor):
    bruto = calcular_salario_bruto(profesor)
    print(f"\n===== Desglose de nomina: {profesor.nombre_completo} =====")
    print(f"Tipo de vinculacion   : {profesor.tipo_vinculacion}")
    print(f"Dedicacion            : {profesor.dedicacion}")
    print(f"Categoria escalafon   : {profesor.categoria_escalafon} "
          f"({puntos_por_categoria(profesor.categoria_escalafon)} puntos)")
    print(f"Puntos por titulos    : {profesor.puntos_titulos}")
    print(f"Puntos productividad  : {profesor.puntos_productividad}")
    print(f"Total puntos          : {total_puntos(profesor)}")
    print(f"Valor del punto       : ${VALOR_PUNTO:,.2f}")
    print(f"Factor proporcional   : {factor_proporcionalidad(profesor):.2f}")
    print("------------------------------------------")
    print(f"Salario bruto         : ${bruto:,.2f}")
    print(f"(-) Salud (4%)        : ${calcular_descuento_salud(bruto):,.2f}")
    print(f"(-) Pension (4%)      : ${calcular_descuento_pension(bruto):,.2f}")
    print(f"Salario neto          : ${calcular_salario_neto(profesor):,.2f}")
    print("------------------------------------------")
    print(f"Prima (informativo)   : ${calcular_prima_servicios(bruto):,.2f}")
    print(f"Cesantias (informativo): ${calcular_cesantias(bruto):,.2f}")
    print("===========================================")
