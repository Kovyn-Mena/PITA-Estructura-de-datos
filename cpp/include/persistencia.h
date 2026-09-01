#ifndef PERSISTENCIA_H
#define PERSISTENCIA_H

#include "entidades.h"
#include <vector>
#include <string>

// Formato: texto plano delimitado por '|' (ver docs/formato_persistencia.md)
// Cada funcion Cargar/Guardar corresponde a un archivo en data/

void guardarFacultades(const std::vector<Facultad>& v, const std::string& ruta);
std::vector<Facultad> cargarFacultades(const std::string& ruta);

void guardarProgramas(const std::vector<Programa>& v, const std::string& ruta);
std::vector<Programa> cargarProgramas(const std::string& ruta);

void guardarCursos(const std::vector<Curso>& v, const std::string& ruta);
std::vector<Curso> cargarCursos(const std::string& ruta);

void guardarEstudiantes(const std::vector<Estudiante>& v, const std::string& rutaEst, const std::string& rutaMatriculas);
std::vector<Estudiante> cargarEstudiantes(const std::string& rutaEst, const std::string& rutaMatriculas);

void guardarProfesores(const std::vector<Profesor>& v, const std::string& ruta);
std::vector<Profesor> cargarProfesores(const std::string& ruta);

void guardarAdministrativos(const std::vector<Administrativo>& v, const std::string& ruta);
std::vector<Administrativo> cargarAdministrativos(const std::string& ruta);

// Utilidad interna: separa una linea por el delimitador '|'
std::vector<std::string> split(const std::string& linea, char delimitador);

#endif
