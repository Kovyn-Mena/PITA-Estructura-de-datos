#ifndef ENTIDADES_H
#define ENTIDADES_H

#include <string>
#include <vector>

// ---------- Estudiante ----------
struct Matricula {
    std::string codigoCurso;
    float nota;
};

struct Estudiante {
    std::string identificacion;
    std::string nombreCompleto;
    std::string codigoPrograma;
    std::string estado;      // Activo, Inactivo, Graduado
    bool activo;
    std::vector<Matricula> matriculas;
};

// ---------- Profesor ----------
struct Profesor {
    std::string identificacion;
    std::string nombreCompleto;
    std::string codigoPrograma;
    std::string tipoVinculacion;   // Planta, Ocasional, Catedratico
    std::string dedicacion;        // TiempoCompleto, MedioTiempo, HorasCatedra
    std::string categoriaEscalafon;// Auxiliar, Asistente, Asociado, Titular (si aplica)
    int horasCatedraSemanales;
    bool adHonorem;
    int aniosExperiencia;
    int puntosTitulos;
    int puntosProductividad;
    bool activo;
};

// ---------- Administrativo ----------
struct Administrativo {
    std::string identificacion;
    std::string nombreCompleto;
    std::string cargo;
    std::string categoria;
    std::string tipoContratacion;
    double salarioBase;
    bool activo;
};

// ---------- Curso ----------
struct Curso {
    std::string codigo;
    std::string nombre;
    int creditos;
    std::string codigoProfesor;
    std::string codigoPrograma;
    bool activo;
};

// ---------- Programa academico ----------
struct Programa {
    std::string codigo;
    std::string nombre;
    std::string nivel; // Tecnologico, Pregrado, Especializacion, Maestria
    std::string codigoFacultad;
    bool activo;
};

// ---------- Facultad ----------
struct Facultad {
    std::string codigo;
    std::string nombre;
    std::string decano;
    bool activo;
};

#endif
