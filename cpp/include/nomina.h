#ifndef NOMINA_H
#define NOMINA_H

#include "entidades.h"

// Valor del punto salarial: PARAMETRO configurable, no debe quedar fijo en el codigo.
// Referencia historica: $20.895 COP para el ano 2024 (Decreto 1279 de 2002).
extern double VALOR_PUNTO;

// Puntos fijos por categoria del escalafon (Decreto 1279, Art. 8)
int puntosPorCategoria(const std::string& categoria);

// Calcula el total de puntos de un profesor (categoria + titulos + productividad)
int totalPuntos(const Profesor& p);

// Aplica el factor de proporcionalidad segun la dedicacion
// (Ej: catedra por horas se calcula proporcional a 18h = tiempo completo de catedra)
double factorProporcionalidad(const Profesor& p);

// Salario bruto = totalPuntos * VALOR_PUNTO * factorProporcionalidad
double calcularSalarioBruto(const Profesor& p);

// Deducciones de ley (simuladas, porcentajes estandar)
double calcularDescuentoSalud(double salarioBruto);    // 4%
double calcularDescuentoPension(double salarioBruto);  // 4%
double calcularSalarioNeto(const Profesor& p);

// Informativo (no se resta del neto, solo se muestra)
double calcularPrimaServicios(double salarioBruto);
double calcularCesantias(double salarioBruto);

// Imprime el desglose completo de nomina de un profesor (para el "aspecto estetico")
void imprimirDesgloseNomina(const Profesor& p);

#endif
