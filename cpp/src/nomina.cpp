#include "../include/nomina.h"
#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

// Parámetros vigentes 2026.
double VALOR_PUNTO = 23924.0;       // Decreto 318 de 2026, art. 2
double SMMLV = 1750905.0;           // Decreto 159 de 2026
static const int PUNTOS_PREGRADO = 178; // Decreto 1279/2002, art. 7
static const double VALOR_HORA_CATEDRA = 0.0; // Pendiente resolución rectoral

// Tasas de aportes patronales (Decreto 1990/2016 → redondeo a pesos enteros)
static const double TASA_PENSION_PATRONAL = 0.12;    // Ley 100/1993 art. 20
static const double TASA_SALUD_PATRONAL   = 0.085;   // Ley 1122/2007 art. 10
static const double TASA_ARL              = 0.00522; // Decreto 1295/1994
static const double TASA_CAJA_COMP        = 0.04;    // Ley 21/1982

int puntosPorCategoria(const string& categoria) {
    if (categoria == "Auxiliar")  return 37;
    if (categoria == "Asistente") return 58;
    if (categoria == "Asociado")  return 74;
    if (categoria == "Titular")   return 96;
    return 0;
}

int totalPuntos(const Profesor& p) {
    if (p.tipoVinculacion != "Planta") return 0;
    return PUNTOS_PREGRADO
         + puntosPorCategoria(p.categoriaEscalafon)
         + p.puntosTitulos
         + p.puntosProductividad;
}

double factorProporcionalidad(const Profesor& p) {
    if (p.dedicacion == "TiempoCompleto") return 1.0;
    if (p.dedicacion == "MedioTiempo")    return 0.5;
    return 1.0;
}

double factorOcasional(const Profesor& p) {
    if (p.categoriaEscalafon == "Auxiliar" && p.dedicacion == "TiempoCompleto") return 2.645;
    if (p.categoriaEscalafon == "Auxiliar" && p.dedicacion == "MedioTiempo")    return 1.509;
    if (p.categoriaEscalafon == "Asistente" && p.dedicacion == "TiempoCompleto") return 3.125;
    if (p.categoriaEscalafon == "Asistente" && p.dedicacion == "MedioTiempo")    return 1.749;
    if (p.categoriaEscalafon == "Asociado" && p.dedicacion == "TiempoCompleto") return 3.606;
    if (p.categoriaEscalafon == "Asociado" && p.dedicacion == "MedioTiempo")    return 1.990;
    if (p.categoriaEscalafon == "Titular" && p.dedicacion == "TiempoCompleto") return 3.918;
    if (p.categoriaEscalafon == "Titular" && p.dedicacion == "MedioTiempo")    return 2.146;
    return 0.0;
}

static const double TASA_ESTAMPILLA = 0.002;

double factorBonificacionPosgrado(const string& posgrado) {
    if (posgrado == "Especializacion") return 0.10;
    if (posgrado == "Maestria")        return 0.45;
    if (posgrado == "Doctorado")       return 0.90;
    return 0.0;
}

double calcularSalarioBruto(const Profesor& p) {
    if (p.adHonorem) return 0.0;

    if (p.tipoVinculacion == "Planta") {
        return llround(totalPuntos(p) * VALOR_PUNTO * factorProporcionalidad(p));
    }

    if (p.tipoVinculacion == "Ocasional") {
        return llround(factorOcasional(p) * SMMLV);
    }

    if (p.tipoVinculacion == "Catedratico") {
        if (VALOR_HORA_CATEDRA <= 0.0) return 0.0;
        double horasMensualesEstimadas = p.horasCatedraSemanales * 4.0;
        return llround(horasMensualesEstimadas * VALOR_HORA_CATEDRA);
    }

    return 0.0;
}

long long calcularBonificacionPosgrado(const Profesor& p) {
    if (p.adHonorem || p.tipoVinculacion == "Planta") return 0;
    double factor = factorBonificacionPosgrado(p.posgrado);
    if (factor <= 0.0) return 0;
    if (p.tipoVinculacion == "Catedratico") {
        double horas = p.horasCatedraSemanales * 4.0;
        return llround((factor * SMMLV) * (horas / 40.0));
    }
    return llround(factor * SMMLV);
}

double calcularTotalDevengado(const Profesor& p) {
    return calcularSalarioBruto(p) + calcularBonificacionPosgrado(p);
}

bool liquidacionDisponible(const Profesor& p) {
    if (p.adHonorem) return true;
    if (p.tipoVinculacion == "Catedratico" && VALOR_HORA_CATEDRA <= 0.0) return false;
    if (p.tipoVinculacion == "Ocasional" && factorOcasional(p) <= 0.0) return false;
    return true;
}

string observacionNormativa(const Profesor& p) {
    if (p.adHonorem) return "Ad-honorem: sin remuneracion (Acuerdo 027/2024).";
    if (p.tipoVinculacion == "Planta") return "Planta: Decreto 1279/2002.";
    if (p.tipoVinculacion == "Ocasional") {
        string det = p.posgrado.empty() ? "" : " con bonificacion por " + p.posgrado + " (Acuerdo 027/2024)";
        return "Ocasional: Acuerdo UPC 027/2024, art. 24" + det + ".";
    }
    if (p.tipoVinculacion == "Catedratico") {
        if (VALOR_HORA_CATEDRA <= 0.0)
            return "Catedratico: pendiente resolucion rectoral vigente de valor hora (Acuerdo 027/2024).";
        return "Catedratico: liquidacion por horas Acuerdo 027/2024.";
    }
    return "Regimen no definido.";
}

long long calcularDescuentoSalud(double salarioBruto) {
    return llround((salarioBruto * 0.04) / 100.0) * 100;
}

long long calcularDescuentoPension(double salarioBruto) {
    return llround((salarioBruto * 0.04) / 100.0) * 100;
}

long long calcularDescuentoFSP(double salarioBruto) {
    if (salarioBruto >= (4.0 * SMMLV)) {
        return llround((salarioBruto * 0.01) / 100.0) * 100;
    }
    return 0;
}

long long calcularDescuentoEstampilla(double salarioBruto) {
    return llround(salarioBruto * TASA_ESTAMPILLA);
}

long long calcularRetencionFuente(double totalDevengado, long long salud, long long pension) {
    double baseGravable = (totalDevengado - salud - pension) * 0.75;
    double umbral = 4975000.0; // Umbral de 95 UVT (2026)
    if (baseGravable > umbral) {
        double impuesto = (baseGravable - umbral) * 0.19;
        return llround(impuesto / 1000.0) * 1000;
    }
    return 0;
}

long long calcularTotalDeducciones(const Profesor& p) {
    double bruto = calcularSalarioBruto(p);
    double devengado = calcularTotalDevengado(p);
    long long salud = calcularDescuentoSalud(bruto);
    long long pension = calcularDescuentoPension(bruto);
    long long fsp = calcularDescuentoFSP(bruto);
    long long estampilla = calcularDescuentoEstampilla(bruto);
    long long retencion = calcularRetencionFuente(devengado, salud, pension);
    return salud + pension + fsp + estampilla + retencion;
}

double calcularSalarioNeto(const Profesor& p) {
    return calcularTotalDevengado(p) - calcularTotalDeducciones(p);
}

double calcularPrimaServicios(double salarioBruto) {
    return salarioBruto / 12.0; // Decreto 1279/2002 art. 44 (1 mes / año)
}

double calcularCesantias(double salarioBruto) {
    return salarioBruto / 12.0; // Decreto 1279/2002 art. 45 y Ley 50/1990
}

double calcularInteresesCesantias(double salarioBruto) {
    return salarioBruto / 1200.0; // Ley 52/1975 (1% mensual)
}

double calcularPrimaNavidad(double salarioBruto) {
    return salarioBruto / 12.0; // Decreto 1042/1978 art. 33
}

double calcularVacaciones(double salarioBruto) {
    return salarioBruto / 24.0; // 15 días hábiles al año
}

double calcularPrimaVacaciones(double salarioBruto) {
    return salarioBruto / 24.0; // Decreto 1279/2002 art. 33
}

double calcularBonificacionServicios(double salarioBruto) {
    return salarioBruto * 2.0 / 12.0; // Decreto 1279/2002 art. 39
}

double calcularTotalPrestaciones(double salarioBruto) {
    return calcularPrimaServicios(salarioBruto)
         + calcularCesantias(salarioBruto)
         + calcularInteresesCesantias(salarioBruto)
         + calcularPrimaNavidad(salarioBruto)
         + calcularVacaciones(salarioBruto)
         + calcularPrimaVacaciones(salarioBruto)
         + calcularBonificacionServicios(salarioBruto);
}

AportesPatronales calcularAportesPatronales(double salarioBruto) {
    AportesPatronales ap;
    ap.pension = llround(salarioBruto * TASA_PENSION_PATRONAL);
    ap.salud   = llround(salarioBruto * TASA_SALUD_PATRONAL);
    ap.arl     = llround(salarioBruto * TASA_ARL);
    ap.caja    = llround(salarioBruto * TASA_CAJA_COMP);
    ap.total   = ap.pension + ap.salud + ap.arl + ap.caja;
    return ap;
}

double calcularCostoTotalEmpleador(const Profesor& p) {
    double bruto = calcularSalarioBruto(p);
    return bruto + calcularAportesPatronales(bruto).total;
}

void imprimirDesgloseNomina(const Profesor& p) {
    cout << fixed << setprecision(0);
    cout << "\n=================================================================\n";
    cout << "      DESPRENDIBLE OFICIAL DE PAGO DE NOMINA DOCENTE (UPC)       \n";
    cout << "=================================================================\n";
    cout << "Docente               : " << p.nombreCompleto << " (ID: " << p.identificacion << ")\n";
    cout << "Modalidad / Regimen   : " << p.tipoVinculacion << " (" << observacionNormativa(p) << ")\n";
    cout << "Dedicacion            : " << p.dedicacion << "\n";
    if (!p.posgrado.empty()) {
        cout << "Cualificacion Postg.  : " << p.posgrado << "\n";
    }

    if (!liquidacionDisponible(p)) {
        cout << "\n[!] SALARIO NO LIQUIDADO: Falta resolucion rectoral de hora catedra.\n";
        cout << "=================================================================\n";
        return;
    }

    double bruto = calcularSalarioBruto(p);
    long long bonifPosg = calcularBonificacionPosgrado(p);
    double devengado = calcularTotalDevengado(p);

    long long salud = calcularDescuentoSalud(bruto);
    long long pension = calcularDescuentoPension(bruto);
    long long fsp = calcularDescuentoFSP(bruto);
    long long estampilla = calcularDescuentoEstampilla(bruto);
    long long retencion = calcularRetencionFuente(devengado, salud, pension);
    long long totalDed = salud + pension + fsp + estampilla + retencion;
    double neto = devengado - totalDed;
    AportesPatronales ap = calcularAportesPatronales(bruto);

    cout << "\n--- DEVENGADOS Y ASIGNACIONES (+) ---\n";
    cout << "SUELDO (Basico)       : $" << bruto << " COP\n";
    if (bonifPosg > 0) {
        cout << "BONIF. CUALIF. POSTG. : $" << bonifPosg << " COP (Acuerdo UPC 027/2024)\n";
    }
    cout << "Total Devengados      : $" << devengado << " COP\n";

    cout << "\n--- DEDUCIDOS (-) [Total Deducciones: -$" << totalDed << " COP] ---\n";
    cout << "DESCUENTO ESTAMPILLA  : -$" << estampilla << " COP (0.2% Pro-UPC)\n";
    if (retencion > 0) {
        cout << "RETENCION EN LA FUENTE: -$" << retencion << " COP (Art. 383 E.T.)\n";
    }
    cout << "APORTE PENSION EMPL.  : -$" << pension << " COP (4% base sueldo, PILA)\n";
    cout << "APORTE SALUD EMPLEADO : -$" << salud << " COP (4% base sueldo, PILA)\n";
    if (fsp > 0) {
        cout << "FONDO SOLIDARIDAD PENS: -$" << fsp << " COP (1% IBC >= 4 SMMLV)\n";
    }
    cout << "Total Deducidos       : -$" << totalDed << " COP\n";

    cout << "\n--- APORTES PATRONALES (COSTO INSTITUCIONAL UPC) ---\n";
    cout << "Pension Patronal (12%): $" << ap.pension << " COP\n";
    cout << "Salud Patronal (8.5%) : $" << ap.salud << " COP\n";
    cout << "ARL (0.522%)          : $" << ap.arl << " COP\n";
    cout << "Caja Compensacion (4%): $" << ap.caja << " COP\n";
    cout << "Costo Total Empleador : $" << calcularCostoTotalEmpleador(p) << " COP\n";

    cout << "\n=================================================================\n";
    cout << ">>> NETO A PAGAR DOCENTE: $" << neto << " COP <<<\n";
    cout << "=================================================================\n";
}

// ── Administrativos ──

double salarioBaseAdministrativo(const string& categoria) {
    if (categoria == "Nivel 2") return 2800000.0;
    if (categoria == "Nivel 3") return 3750000.0;
    if (categoria == "Nivel 4") return 5050000.0;
    return 1950000.0; // Nivel 1 por defecto
}

double calcularSalarioBrutoAdmin(const Administrativo& a) {
    if (a.salarioBase > 0) return a.salarioBase;
    return salarioBaseAdministrativo(a.categoria);
}

long long calcularDescuentoSaludAdmin(double salarioBruto) {
    return llround(salarioBruto * 0.04);
}

long long calcularDescuentoPensionAdmin(double salarioBruto) {
    return llround(salarioBruto * 0.04);
}

long long calcularDescuentoFSPAdmin(double salarioBruto) {
    if (salarioBruto >= (4.0 * SMMLV)) {
        return llround(salarioBruto * 0.01);
    }
    return 0;
}

double calcularSalarioNetoAdmin(const Administrativo& a) {
    double bruto = calcularSalarioBrutoAdmin(a);
    return bruto - calcularDescuentoSaludAdmin(bruto)
                 - calcularDescuentoPensionAdmin(bruto)
                 - calcularDescuentoFSPAdmin(bruto);
}

AportesPatronales calcularAportesPatronalesAdmin(double salarioBruto) {
    return calcularAportesPatronales(salarioBruto);
}

double calcularCostoTotalAdmin(const Administrativo& a) {
    double bruto = calcularSalarioBrutoAdmin(a);
    return bruto + calcularAportesPatronalesAdmin(bruto).total;
}

void imprimirDesgloseNominaAdmin(const Administrativo& a) {
    cout << fixed << setprecision(0);
    cout << "\n=================================================================\n";
    cout << "    DESPRENDIBLE OFICIAL DE PAGO PERSONAL ADMINISTRATIVO (UPC)   \n";
    cout << "=================================================================\n";
    cout << "Funcionario           : " << a.nombreCompleto << " (ID: " << a.identificacion << ")\n";
    cout << "Cargo / Nivel         : " << a.cargo << " (" << a.categoria << ")\n";
    cout << "Tipo de Contratacion  : " << a.tipoContratacion << "\n";
    cout << "Adscrito a            : " << (a.codigoFacultad.empty() ? "Nivel Central" : a.codigoFacultad) << "\n";

    double bruto = calcularSalarioBrutoAdmin(a);
    long long salud = calcularDescuentoSaludAdmin(bruto);
    long long pension = calcularDescuentoPensionAdmin(bruto);
    long long fsp = calcularDescuentoFSPAdmin(bruto);
    long long totalDed = salud + pension + fsp;
    double neto = bruto - totalDed;
    AportesPatronales ap = calcularAportesPatronalesAdmin(bruto);
    double costoUpc = bruto + ap.total;

    cout << "\n--- DEVENGADOS Y ASIGNACIONES (+) ---\n";
    cout << "Asignacion Salarial   : $" << bruto << " COP (" << a.categoria << " - Decretos Salariales 2026)\n";

    cout << "\n--- DEDUCCIONES OBLIGATORIAS DE LEY (-) [Total: -$" << totalDed << " COP] ---\n";
    cout << "IBC Seguridad Social  : $" << bruto << " COP\n";
    cout << "(-) Salud (4%)        : -$" << salud << " COP\n";
    cout << "(-) Pension (4%)      : -$" << pension << " COP\n";
    if (fsp > 0) {
        cout << "(-) FSP (1%)          : -$" << fsp << " COP (salario >= 4 SMMLV)\n";
    } else {
        cout << "    FSP (1%)          : $0 COP (no supera 4 SMMLV)\n";
    }

    cout << "\n--- COSTO TOTAL EMPLEADOR (UPC) [Total: $" << costoUpc << " COP] ---\n";
    cout << "Asignacion Basica     : $" << bruto << " COP\n";
    cout << "Salud Patronal (8.5%) : $" << ap.salud << " COP\n";
    cout << "Pension Patronal (12%): $" << ap.pension << " COP\n";
    cout << "ARL (0.522%)          : $" << ap.arl << " COP\n";
    cout << "Caja Compensacion (4%): $" << ap.caja << " COP\n";

    cout << "\n=================================================================\n";
    cout << ">>> NETO A PAGAR FUNCIONARIO: $" << neto << " COP <<<\n";
    cout << "=================================================================\n";
}
