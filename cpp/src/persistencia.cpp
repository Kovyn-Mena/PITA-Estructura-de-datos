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
// TODO: implementar guardar/cargar para Programa, Curso, Estudiante
// (con matriculas), Profesor y Administrativo, siguiendo el mismo patron.
// =========================================================================
