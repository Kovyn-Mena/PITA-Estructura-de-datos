#ifndef GESTION_H
#define GESTION_H

#include "entidades.h"
#include <vector>
#include <string>

// ===================== FACULTADES =====================
void crearFacultad(std::vector<Facultad>& facultades);
void listarFacultades(const std::vector<Facultad>& facultades);
Facultad* buscarFacultad(std::vector<Facultad>& facultades, const std::string& codigo);
void modificarFacultad(std::vector<Facultad>& facultades, const std::string& codigo);
void desactivarFacultad(std::vector<Facultad>& facultades, const std::string& codigo);
void eliminarFacultad(std::vector<Facultad>& facultades, const std::string& codigo);

// ===================== PROGRAMAS =====================
void crearPrograma(std::vector<Programa>& programas, std::vector<Facultad>& facultades);
void listarProgramas(const std::vector<Programa>& programas);
Programa* buscarPrograma(std::vector<Programa>& programas, const std::string& codigo);
void modificarPrograma(std::vector<Programa>& programas, const std::string& codigo);
void desactivarPrograma(std::vector<Programa>& programas, const std::string& codigo);
void eliminarPrograma(std::vector<Programa>& programas, const std::string& codigo);

// ===================== CURSOS =====================
void crearCurso(std::vector<Curso>& cursos, std::vector<Programa>& programas);
void listarCursos(const std::vector<Curso>& cursos);
Curso* buscarCurso(std::vector<Curso>& cursos, const std::string& codigo);
void modificarCurso(std::vector<Curso>& cursos, const std::string& codigo);
void desactivarCurso(std::vector<Curso>& cursos, const std::string& codigo);
void eliminarCurso(std::vector<Curso>& cursos, const std::string& codigo);

// ===================== ESTUDIANTES =====================
void crearEstudiante(std::vector<Estudiante>& estudiantes, std::vector<Programa>& programas);
void listarEstudiantes(const std::vector<Estudiante>& estudiantes);
Estudiante* buscarEstudiante(std::vector<Estudiante>& estudiantes, const std::string& id);
void modificarEstudiante(std::vector<Estudiante>& estudiantes, const std::string& id);
void desactivarEstudiante(std::vector<Estudiante>& estudiantes, const std::string& id);
void eliminarEstudiante(std::vector<Estudiante>& estudiantes, const std::string& id);

void matricularCurso(std::vector<Estudiante>& estudiantes, const std::string& id, std::vector<Curso>& cursos);
void cancelarCurso(std::vector<Estudiante>& estudiantes, const std::string& id);
float calcularPromedio(const Estudiante& e);
bool estaEnRiesgoEbra(const Estudiante& e); // promedio < 3.25
void consultarEstudiante(std::vector<Estudiante>& estudiantes, const std::string& id);

// ===================== PROFESORES =====================
void crearProfesor(std::vector<Profesor>& profesores, std::vector<Programa>& programas);
void listarProfesores(const std::vector<Profesor>& profesores);
Profesor* buscarProfesor(std::vector<Profesor>& profesores, const std::string& id);
void modificarProfesor(std::vector<Profesor>& profesores, const std::string& id);
void desactivarProfesor(std::vector<Profesor>& profesores, const std::string& id);
void eliminarProfesor(std::vector<Profesor>& profesores, const std::string& id);
void consultarProfesor(std::vector<Profesor>& profesores, const std::string& id); // desglose de nomina

// ===================== ADMINISTRATIVOS =====================
void crearAdministrativo(std::vector<Administrativo>& admins);
void listarAdministrativos(const std::vector<Administrativo>& admins);
Administrativo* buscarAdministrativo(std::vector<Administrativo>& admins, const std::string& id);
void modificarAdministrativo(std::vector<Administrativo>& admins, const std::string& id);
void desactivarAdministrativo(std::vector<Administrativo>& admins, const std::string& id);
void eliminarAdministrativo(std::vector<Administrativo>& admins, const std::string& id);

#endif
