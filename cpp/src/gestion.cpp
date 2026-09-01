#include "../include/gestion.h"
#include <iostream>
#include <limits>

using namespace std;

// =========================================================================
// FACULTADES — implementacion completa, usar como PATRON para las demas
// entidades (Programa, Curso, Estudiante, Profesor, Administrativo).
// =========================================================================

void crearFacultad(vector<Facultad>& facultades) {
    Facultad f;
    cout << "Codigo facultad: ";
    cin >> f.codigo;

    if (buscarFacultad(facultades, f.codigo) != nullptr) {
        cout << "Ya existe una facultad con ese codigo.\n";
        return;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nombre: ";
    getline(cin, f.nombre);
    cout << "Decano: ";
    getline(cin, f.decano);
    f.activo = true;

    facultades.push_back(f); // "inclusion" en la lista contenedora
    cout << "Facultad creada correctamente.\n";
}

void listarFacultades(const vector<Facultad>& facultades) {
    cout << "\n--- Facultades registradas ---\n";
    if (facultades.empty()) {
        cout << "(no hay facultades registradas)\n";
        return;
    }
    for (const auto& f : facultades) {
        cout << f.codigo << " | " << f.nombre << " | Decano: " << f.decano
             << " | " << (f.activo ? "Activa" : "Inactiva") << "\n";
    }
}

Facultad* buscarFacultad(vector<Facultad>& facultades, const string& codigo) {
    for (auto& f : facultades) {
        if (f.codigo == codigo) return &f;
    }
    return nullptr; // no encontrado
}

void modificarFacultad(vector<Facultad>& facultades, const string& codigo) {
    Facultad* f = buscarFacultad(facultades, codigo);
    if (!f) { cout << "Facultad no encontrada.\n"; return; }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nuevo nombre (" << f->nombre << "): ";
    getline(cin, f->nombre);
    cout << "Nuevo decano (" << f->decano << "): ";
    getline(cin, f->decano);
    cout << "Facultad modificada.\n";
}

void desactivarFacultad(vector<Facultad>& facultades, const string& codigo) {
    Facultad* f = buscarFacultad(facultades, codigo);
    if (!f) { cout << "Facultad no encontrada.\n"; return; }
    f->activo = false; // borrado LOGICO: se conserva el registro
    cout << "Facultad desactivada (borrado logico).\n";
}

void eliminarFacultad(vector<Facultad>& facultades, const string& codigo) {
    for (size_t i = 0; i < facultades.size(); i++) {
        if (facultades[i].codigo == codigo) {
            facultades.erase(facultades.begin() + i); // borrado FISICO
            cout << "Facultad eliminada permanentemente.\n";
            return;
        }
    }
    cout << "Facultad no encontrada.\n";
}

// =========================================================================
// PROGRAMAS, CURSOS, ESTUDIANTES, PROFESORES, ADMINISTRATIVOS
// TODO: replicar el mismo patron de Facultad (Dia 3-4 del cronograma).
// Los prototipos ya estan declarados en gestion.h.
// =========================================================================
