#include "../include/persistencia.h"
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

vector<string> split(const string& linea, char delimitador) {
    vector<string> partes;
    stringstream ss(linea);
    string parte;
    while (getline(ss, parte, delimitador)) {
        partes.push_back(parte);
    }
    return partes;
}

// =========================================================================
// FACULTADES — patron completo de guardar/cargar. Formato en
// docs/formato_persistencia.md. Replicar para las demas entidades.
// =========================================================================

void guardarFacultades(const vector<Facultad>& v, const string& ruta) {
    ofstream archivo(ruta);
    if (!archivo.is_open()) {
        cout << "No se pudo abrir " << ruta << " para escritura.\n";
        return;
    }
    for (const auto& f : v) {
        archivo << f.codigo << "|" << f.nombre << "|" << f.decano << "|"
                << (f.activo ? 1 : 0) << "\n";
    }
    archivo.close();
}

vector<Facultad> cargarFacultades(const string& ruta) {
    vector<Facultad> resultado;
    ifstream archivo(ruta);
    if (!archivo.is_open()) {
        // No es un error: el archivo simplemente no existe aun.
        return resultado;
    }
    string linea;
    while (getline(archivo, linea)) {
        if (linea.empty()) continue;
        vector<string> campos = split(linea, '|');
        if (campos.size() < 4) continue; // linea corrupta, se ignora
        Facultad f;
        f.codigo = campos[0];
        f.nombre = campos[1];
        f.decano = campos[2];
        f.activo = (campos[3] == "1");
        resultado.push_back(f);
    }
    archivo.close();
    return resultado;
}

// =========================================================================
// PROGRAMAS
// =========================================================================

void guardarProgramas(const vector<Programa>& v, const string& ruta) {
    ofstream archivo(ruta);
    if (!archivo.is_open()) {
        cout << "No se pudo abrir " << ruta << " para escritura.\n";
        return;
    }
    for (const auto& p : v) {
        archivo << p.codigo << "|" << p.nombre << "|" << p.nivel << "|"
                << p.codigoFacultad << "|" << (p.activo ? 1 : 0) << "\n";
    }
    archivo.close();
}

vector<Programa> cargarProgramas(const string& ruta) {
    vector<Programa> resultado;
    ifstream archivo(ruta);
    if (!archivo.is_open()) return resultado;

    string linea;
    while (getline(archivo, linea)) {
        if (linea.empty()) continue;
        vector<string> campos = split(linea, '|');
        if (campos.size() < 5) continue;
        Programa p;
        p.codigo = campos[0];
        p.nombre = campos[1];
        p.nivel = campos[2];
        p.codigoFacultad = campos[3];
        p.activo = (campos[4] == "1");
        resultado.push_back(p);
    }
    archivo.close();
    return resultado;
}

// =========================================================================
// CURSOS
// =========================================================================

void guardarCursos(const vector<Curso>& v, const string& ruta) {
    ofstream archivo(ruta);
    if (!archivo.is_open()) {
        cout << "No se pudo abrir " << ruta << " para escritura.\n";
        return;
    }
    for (const auto& c : v) {
        archivo << c.codigo << "|" << c.nombre << "|" << c.creditos << "|"
                << c.codigoProfesor << "|" << c.codigoPrograma << "|"
                << (c.activo ? 1 : 0) << "\n";
    }
    archivo.close();
}

vector<Curso> cargarCursos(const string& ruta) {
    vector<Curso> resultado;
    ifstream archivo(ruta);
    if (!archivo.is_open()) return resultado;

    string linea;
    while (getline(archivo, linea)) {
        if (linea.empty()) continue;
        vector<string> campos = split(linea, '|');
        if (campos.size() < 6) continue;
        Curso c;
        c.codigo = campos[0];
        c.nombre = campos[1];
        c.creditos = stoi(campos[2]);
        c.codigoProfesor = campos[3];
        c.codigoPrograma = campos[4];
        c.activo = (campos[5] == "1");
        resultado.push_back(c);
    }
    archivo.close();
    return resultado;
}

// =========================================================================
// ESTUDIANTES — se guardan en DOS archivos: uno con los datos del
// estudiante, otro con la relacion estudiante-curso-nota (matriculas).
// Se separan para no repetir el nombre del estudiante en cada matricula.
// =========================================================================

void guardarEstudiantes(const vector<Estudiante>& v, const string& rutaEst, const string& rutaMatriculas) {
    ofstream archivoEst(rutaEst);
    if (!archivoEst.is_open()) {
        cout << "No se pudo abrir " << rutaEst << " para escritura.\n";
        return;
    }
    for (const auto& e : v) {
        archivoEst << e.identificacion << "|" << e.nombreCompleto << "|"
                   << e.codigoPrograma << "|" << e.estado << "|"
                   << (e.activo ? 1 : 0) << "\n";
    }
    archivoEst.close();

    ofstream archivoMat(rutaMatriculas);
    if (!archivoMat.is_open()) {
        cout << "No se pudo abrir " << rutaMatriculas << " para escritura.\n";
        return;
    }
    for (const auto& e : v) {
        for (const auto& m : e.matriculas) {
            archivoMat << e.identificacion << "|" << m.codigoCurso << "|" << m.nota << "\n";
        }
    }
    archivoMat.close();
}

vector<Estudiante> cargarEstudiantes(const string& rutaEst, const string& rutaMatriculas) {
    vector<Estudiante> resultado;
    ifstream archivoEst(rutaEst);
    if (!archivoEst.is_open()) return resultado;

    string linea;
    while (getline(archivoEst, linea)) {
        if (linea.empty()) continue;
        vector<string> campos = split(linea, '|');
        if (campos.size() < 5) continue;
        Estudiante e;
        e.identificacion = campos[0];
        e.nombreCompleto = campos[1];
        e.codigoPrograma = campos[2];
        e.estado = campos[3];
        e.activo = (campos[4] == "1");
        resultado.push_back(e);
    }
    archivoEst.close();

    // Segunda pasada: cargar matriculas y asociarlas al estudiante correcto
    ifstream archivoMat(rutaMatriculas);
    if (archivoMat.is_open()) {
        while (getline(archivoMat, linea)) {
            if (linea.empty()) continue;
            vector<string> campos = split(linea, '|');
            if (campos.size() < 3) continue;
            string idEstudiante = campos[0];
            Matricula m;
            m.codigoCurso = campos[1];
            m.nota = stof(campos[2]);

            for (auto& e : resultado) {
                if (e.identificacion == idEstudiante) {
                    e.matriculas.push_back(m);
                    break;
                }
            }
        }
        archivoMat.close();
    }

    return resultado;
}

// =========================================================================
// PROFESORES
// =========================================================================

void guardarProfesores(const vector<Profesor>& v, const string& ruta) {
    ofstream archivo(ruta);
    if (!archivo.is_open()) {
        cout << "No se pudo abrir " << ruta << " para escritura.\n";
        return;
    }
    for (const auto& p : v) {
        archivo << p.identificacion << "|" << p.nombreCompleto << "|"
                << p.codigoPrograma << "|" << p.tipoVinculacion << "|"
                << p.dedicacion << "|" << p.categoriaEscalafon << "|"
                << p.horasCatedraSemanales << "|" << (p.adHonorem ? 1 : 0) << "|"
                << p.aniosExperiencia << "|" << p.puntosTitulos << "|"
                << p.puntosProductividad << "|" << (p.activo ? 1 : 0) << "\n";
    }
    archivo.close();
}

vector<Profesor> cargarProfesores(const string& ruta) {
    vector<Profesor> resultado;
    ifstream archivo(ruta);
    if (!archivo.is_open()) return resultado;

    string linea;
    while (getline(archivo, linea)) {
        if (linea.empty()) continue;
        vector<string> campos = split(linea, '|');
        if (campos.size() < 12) continue;
        Profesor p;
        p.identificacion = campos[0];
        p.nombreCompleto = campos[1];
        p.codigoPrograma = campos[2];
        p.tipoVinculacion = campos[3];
        p.dedicacion = campos[4];
        p.categoriaEscalafon = campos[5];
        p.horasCatedraSemanales = stoi(campos[6]);
        p.adHonorem = (campos[7] == "1");
        p.aniosExperiencia = stoi(campos[8]);
        p.puntosTitulos = stoi(campos[9]);
        p.puntosProductividad = stoi(campos[10]);
        p.activo = (campos[11] == "1");
        resultado.push_back(p);
    }
    archivo.close();
    return resultado;
}

// =========================================================================
// TODO: implementar guardar/cargar para Administrativo, siguiendo el mismo patron.
// =========================================================================
