#ifndef GENERADOR_H
#define GENERADOR_H

#include "entidades.h"
#include <vector>
#include <string>

// Genera la estructura masiva de Parcial 1:
// - 10 facultades
// - 150 programas (15 por facultad)
// - 9.000 profesores (60 por programa)
// - 7.500 materias (50 por programa)
// - 225.000 estudiantes (1.500 por programa)
void generarDatosMasivos(
    std::vector<Facultad>& facultades,
    std::vector<Programa>& programas,
    std::vector<Profesor>& profesores,
    std::vector<Curso>& cursos,
    std::vector<Estudiante>& estudiantes
);

// Menu interactivo de confirmacion y guardado de generacion masiva
void menuGeneracionMasiva(
    std::vector<Facultad>& facultades,
    std::vector<Programa>& programas,
    std::vector<Curso>& cursos,
    std::vector<Estudiante>& estudiantes,
    std::vector<Profesor>& profesores,
    const std::string& rutaFacultades,
    const std::string& rutaProgramas,
    const std::string& rutaCursos,
    const std::string& rutaEstudiantes,
    const std::string& rutaMatriculas,
    const std::string& rutaProfesores
);

// Genera horarios libres de conflictos para una lista de asignaturas/cursos
int generarHorariosCursos(std::vector<Curso>& cursos);

// Menu interactivo para generar horarios y guardarlos en persistencia
void menuGeneracionHorarios(std::vector<Curso>& cursos, const std::string& rutaCursos);

// Consulta interactiva de horario por codigo de curso o muestra
void consultarHorarioCurso(const std::vector<Curso>& cursos);

// Evaluacion masiva de rendimiento academico (ERRA / EBRA: promedio < 3.25)
void evaluarErraMasivo(const std::vector<Estudiante>& estudiantes);

#endif
