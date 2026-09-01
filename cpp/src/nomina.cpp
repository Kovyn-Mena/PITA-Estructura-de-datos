#include "../include/nomina.h"
#include <iostream>
#include <iomanip>

using namespace std;

// Parametro configurable — NO hardcodear en la logica, se declara aqui
// y se puede cambiar desde main() o cargar de un archivo de configuracion.
double VALOR_PUNTO = 20895.0; // referencia 2024, Decreto 1279/2002

int puntosPorCategoria(const string& categoria) {
    if (categoria == "Auxiliar")  return 37;
    if (categoria == "Asistente") return 58;
    if (categoria == "Asociado")  return 74;
    if (categoria == "Titular")   return 96;
    return 0; // catedraticos sin escalafon formal
}

int totalPuntos(const Profesor& p) {
    return puntosPorCategoria(p.categoriaEscalafon)
         + p.puntosTitulos
         + p.puntosProductividad;
}

double factorProporcionalidad(const Profesor& p) {
    // Segun el Decreto 1279 (Art. 6, paragrafo): dedicaciones distintas a
    // tiempo completo se calculan de forma proporcional.
    if (p.dedicacion == "TiempoCompleto") return 1.0;
    if (p.dedicacion == "MedioTiempo")    return 0.5;
    if (p.dedicacion == "HorasCatedra") {
        // proporcional a 18 horas semanales = "tiempo completo" de catedra
        return static_cast<double>(p.horasCatedraSemanales) / 18.0;
    }
    return 1.0;
}

double calcularSalarioBruto(const Profesor& p) {
    if (p.adHonorem) return 0.0; // ad-honorem: sin remuneracion
    return totalPuntos(p) * VALOR_PUNTO * factorProporcionalidad(p);
}

double calcularDescuentoSalud(double salarioBruto) {
    return salarioBruto * 0.04;
}

double calcularDescuentoPension(double salarioBruto) {
    return salarioBruto * 0.04;
}

double calcularSalarioNeto(const Profesor& p) {
    double bruto = calcularSalarioBruto(p);
    return bruto - calcularDescuentoSalud(bruto) - calcularDescuentoPension(bruto);
}

double calcularPrimaServicios(double salarioBruto) {
    // Prima de servicios: 1 salario mensual por semestre trabajado (aprox. mensualizado)
    return salarioBruto / 12.0;
}

double calcularCesantias(double salarioBruto) {
    // Cesantias: 1 salario mensual por ano trabajado (aprox. mensualizado)
    return salarioBruto / 12.0;
}

void imprimirDesgloseNomina(const Profesor& p) {
    double bruto = calcularSalarioBruto(p);
    cout << fixed << setprecision(2);
    cout << "\n===== Desglose de nomina: " << p.nombreCompleto << " =====\n";
    cout << "Tipo de vinculacion   : " << p.tipoVinculacion << "\n";
    cout << "Dedicacion            : " << p.dedicacion << "\n";
    cout << "Categoria escalafon   : " << p.categoriaEscalafon
         << " (" << puntosPorCategoria(p.categoriaEscalafon) << " puntos)\n";
    cout << "Puntos por titulos    : " << p.puntosTitulos << "\n";
    cout << "Puntos productividad  : " << p.puntosProductividad << "\n";
    cout << "Total puntos          : " << totalPuntos(p) << "\n";
    cout << "Valor del punto       : $" << VALOR_PUNTO << "\n";
    cout << "Factor proporcional   : " << factorProporcionalidad(p) << "\n";
    cout << "------------------------------------------\n";
    cout << "Salario bruto         : $" << bruto << "\n";
    cout << "(-) Salud (4%)        : $" << calcularDescuentoSalud(bruto) << "\n";
    cout << "(-) Pension (4%)      : $" << calcularDescuentoPension(bruto) << "\n";
    cout << "Salario neto          : $" << calcularSalarioNeto(p) << "\n";
    cout << "------------------------------------------\n";
    cout << "Prima (informativo)   : $" << calcularPrimaServicios(bruto) << "\n";
    cout << "Cesantias (informativo): $" << calcularCesantias(bruto) << "\n";
    cout << "===========================================\n";
}
