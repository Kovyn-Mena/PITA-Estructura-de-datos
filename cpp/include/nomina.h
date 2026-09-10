#ifndef NOMINA_H
#define NOMINA_H

#include "entidades.h"
#include <string>

// Parámetros vigentes 2026
extern double VALOR_PUNTO;
extern double SMMLV;

// ── Docentes ──
int puntosPorCategoria(const std::string& categoria);
int totalPuntos(const Profesor& p);
double factorProporcionalidad(const Profesor& p);
double factorOcasional(const Profesor& p);
double calcularSalarioBruto(const Profesor& p);
long long calcularBonificacionPosgrado(const Profesor& p);
double calcularTotalDevengado(const Profesor& p);
bool liquidacionDisponible(const Profesor& p);
std::string observacionNormativa(const Profesor& p);

// Descuentos empleado (redondeo a pesos enteros / PILA según Decreto 1990/2016)
long long calcularDescuentoSalud(double salarioBruto);
long long calcularDescuentoPension(double salarioBruto);
long long calcularDescuentoFSP(double salarioBruto);
long long calcularDescuentoEstampilla(double salarioBruto);
long long calcularRetencionFuente(double totalDevengado, long long salud, long long pension);
long long calcularTotalDeducciones(const Profesor& p);
double calcularSalarioNeto(const Profesor& p);

// Prestaciones sociales (provisión mensual)
double calcularPrimaServicios(double salarioBruto);
double calcularCesantias(double salarioBruto);
double calcularInteresesCesantias(double salarioBruto);
double calcularPrimaNavidad(double salarioBruto);
double calcularVacaciones(double salarioBruto);
double calcularPrimaVacaciones(double salarioBruto);
double calcularBonificacionServicios(double salarioBruto);
double calcularTotalPrestaciones(double salarioBruto);

// Aportes patronales UPC
struct AportesPatronales {
    long long pension;
    long long salud;
    long long arl;
    long long caja;
    long long total;
};

AportesPatronales calcularAportesPatronales(double salarioBruto);
double calcularCostoTotalEmpleador(const Profesor& p);
void imprimirDesgloseNomina(const Profesor& p);

// ── Administrativos ──
double salarioBaseAdministrativo(const std::string& categoria);
double calcularSalarioBrutoAdmin(const Administrativo& a);
long long calcularDescuentoSaludAdmin(double salarioBruto);
long long calcularDescuentoPensionAdmin(double salarioBruto);
long long calcularDescuentoFSPAdmin(double salarioBruto);
double calcularSalarioNetoAdmin(const Administrativo& a);
AportesPatronales calcularAportesPatronalesAdmin(double salarioBruto);
double calcularCostoTotalAdmin(const Administrativo& a);
void imprimirDesgloseNominaAdmin(const Administrativo& a);

#endif
