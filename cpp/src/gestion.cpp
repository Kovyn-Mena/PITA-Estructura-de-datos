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
// PROGRAMAS — mismo patron que Facultad, con una validacion extra:
// un Programa pertenece a una Facultad, asi que se verifica que la
// facultad exista y este activa antes de crear el programa (integridad
// referencial basica, sin usar claves foraneas de base de datos real).
// =========================================================================

void crearPrograma(vector<Programa>& programas, vector<Facultad>& facultades) {
    Programa p;
    cout << "Codigo programa: ";
    cin >> p.codigo;

    if (buscarPrograma(programas, p.codigo) != nullptr) {
        cout << "Ya existe un programa con ese codigo.\n";
        return;
    }

    cout << "Codigo de la facultad a la que pertenece: ";
    cin >> p.codigoFacultad;
    Facultad* f = buscarFacultad(facultades, p.codigoFacultad);
    if (!f) {
        cout << "Esa facultad no existe. Cree primero la facultad.\n";
        return;
    }
    if (!f->activo) {
        cout << "Esa facultad esta inactiva, no se le pueden asociar programas.\n";
        return;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nombre del programa: ";
    getline(cin, p.nombre);
    cout << "Nivel (Tecnologico/Pregrado/Especializacion/Maestria): ";
    getline(cin, p.nivel);
    p.activo = true;

    programas.push_back(p);
    cout << "Programa creado correctamente.\n";
}

void listarProgramas(const vector<Programa>& programas) {
    cout << "\n--- Programas academicos registrados ---\n";
    if (programas.empty()) {
        cout << "(no hay programas registrados)\n";
        return;
    }
    for (const auto& p : programas) {
        cout << p.codigo << " | " << p.nombre << " | " << p.nivel
             << " | Facultad: " << p.codigoFacultad
             << " | " << (p.activo ? "Activo" : "Inactivo") << "\n";
    }
}

Programa* buscarPrograma(vector<Programa>& programas, const string& codigo) {
    for (auto& p : programas) {
        if (p.codigo == codigo) return &p;
    }
    return nullptr;
}

void modificarPrograma(vector<Programa>& programas, const string& codigo) {
    Programa* p = buscarPrograma(programas, codigo);
    if (!p) { cout << "Programa no encontrado.\n"; return; }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nuevo nombre (" << p->nombre << "): ";
    getline(cin, p->nombre);
    cout << "Nuevo nivel (" << p->nivel << "): ";
    getline(cin, p->nivel);
    cout << "Programa modificado.\n";
}

void desactivarPrograma(vector<Programa>& programas, const string& codigo) {
    Programa* p = buscarPrograma(programas, codigo);
    if (!p) { cout << "Programa no encontrado.\n"; return; }
    p->activo = false;
    cout << "Programa desactivado (borrado logico).\n";
}

void eliminarPrograma(vector<Programa>& programas, const string& codigo) {
    for (size_t i = 0; i < programas.size(); i++) {
        if (programas[i].codigo == codigo) {
            programas.erase(programas.begin() + i);
            cout << "Programa eliminado permanentemente.\n";
            return;
        }
    }
    cout << "Programa no encontrado.\n";
}

// =========================================================================
// CURSOS — mismo patron, validando que el Programa exista.
// codigoProfesor se guarda como texto libre por ahora (aun no existe el
// modulo de Profesores); se valida contra la lista real en el Dia 7.
// =========================================================================

void crearCurso(vector<Curso>& cursos, vector<Programa>& programas) {
    Curso c;
    cout << "Codigo curso: ";
    cin >> c.codigo;

    if (buscarCurso(cursos, c.codigo) != nullptr) {
        cout << "Ya existe un curso con ese codigo.\n";
        return;
    }

    cout << "Codigo del programa al que pertenece: ";
    cin >> c.codigoPrograma;
    Programa* p = buscarPrograma(programas, c.codigoPrograma);
    if (!p) {
        cout << "Ese programa no existe. Cree primero el programa.\n";
        return;
    }
    if (!p->activo) {
        cout << "Ese programa esta inactivo, no se le pueden asociar cursos.\n";
        return;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nombre del curso: ";
    getline(cin, c.nombre);
    cout << "Creditos: ";
    cin >> c.creditos;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Codigo del profesor (Enter si aun no se asigna): ";
    getline(cin, c.codigoProfesor);
    c.activo = true;

    cursos.push_back(c);
    cout << "Curso creado correctamente.\n";
}

void listarCursos(const vector<Curso>& cursos) {
    cout << "\n--- Cursos registrados ---\n";
    if (cursos.empty()) {
        cout << "(no hay cursos registrados)\n";
        return;
    }
    for (const auto& c : cursos) {
        cout << c.codigo << " | " << c.nombre << " | " << c.creditos << " creditos"
             << " | Programa: " << c.codigoPrograma
             << " | Profesor: " << (c.codigoProfesor.empty() ? "(sin asignar)" : c.codigoProfesor)
             << " | " << (c.activo ? "Activo" : "Inactivo") << "\n";
    }
}

Curso* buscarCurso(vector<Curso>& cursos, const string& codigo) {
    for (auto& c : cursos) {
        if (c.codigo == codigo) return &c;
    }
    return nullptr;
}

void modificarCurso(vector<Curso>& cursos, const string& codigo) {
    Curso* c = buscarCurso(cursos, codigo);
    if (!c) { cout << "Curso no encontrado.\n"; return; }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nuevo nombre (" << c->nombre << "): ";
    getline(cin, c->nombre);
    cout << "Nuevos creditos (" << c->creditos << "): ";
    cin >> c->creditos;
    cout << "Curso modificado.\n";
}

void desactivarCurso(vector<Curso>& cursos, const string& codigo) {
    Curso* c = buscarCurso(cursos, codigo);
    if (!c) { cout << "Curso no encontrado.\n"; return; }
    c->activo = false;
    cout << "Curso desactivado (borrado logico).\n";
}

void eliminarCurso(vector<Curso>& cursos, const string& codigo) {
    for (size_t i = 0; i < cursos.size(); i++) {
        if (cursos[i].codigo == codigo) {
            cursos.erase(cursos.begin() + i);
            cout << "Curso eliminado permanentemente.\n";
            return;
        }
    }
    cout << "Curso no encontrado.\n";
}

// =========================================================================
// ESTUDIANTES — mismo patron, mas dos operaciones propias del negocio
// academico: matricular/cancelar curso, y el calculo de promedio + EBRA.
// La lista de matriculas vive DENTRO de cada Estudiante (lista anidada).
// =========================================================================

void crearEstudiante(vector<Estudiante>& estudiantes, vector<Programa>& programas) {
    Estudiante e;
    cout << "Identificacion: ";
    cin >> e.identificacion;

    if (buscarEstudiante(estudiantes, e.identificacion) != nullptr) {
        cout << "Ya existe un estudiante con esa identificacion.\n";
        return;
    }

    cout << "Codigo del programa al que pertenece: ";
    cin >> e.codigoPrograma;
    Programa* p = buscarPrograma(programas, e.codigoPrograma);
    if (!p) {
        cout << "Ese programa no existe. Cree primero el programa.\n";
        return;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nombre completo: ";
    getline(cin, e.nombreCompleto);
    e.estado = "Activo";
    e.activo = true;
    // e.matriculas queda vacio; se llena con matricularCurso()

    estudiantes.push_back(e);
    cout << "Estudiante creado correctamente.\n";
}

void listarEstudiantes(const vector<Estudiante>& estudiantes) {
    cout << "\n--- Estudiantes registrados ---\n";
    if (estudiantes.empty()) {
        cout << "(no hay estudiantes registrados)\n";
        return;
    }
    for (const auto& e : estudiantes) {
        cout << e.identificacion << " | " << e.nombreCompleto
             << " | Programa: " << e.codigoPrograma
             << " | " << e.estado
             << " | " << (e.activo ? "Activo" : "Inactivo")
             << " | Cursos matriculados: " << e.matriculas.size() << "\n";
    }
}

Estudiante* buscarEstudiante(vector<Estudiante>& estudiantes, const string& id) {
    for (auto& e : estudiantes) {
        if (e.identificacion == id) return &e;
    }
    return nullptr;
}

void modificarEstudiante(vector<Estudiante>& estudiantes, const string& id) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Nuevo nombre (" << e->nombreCompleto << "): ";
    getline(cin, e->nombreCompleto);
    cout << "Estudiante modificado.\n";
}

void desactivarEstudiante(vector<Estudiante>& estudiantes, const string& id) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }
    e->activo = false;
    e->estado = "Inactivo";
    cout << "Estudiante desactivado (borrado logico).\n";
}

void eliminarEstudiante(vector<Estudiante>& estudiantes, const string& id) {
    for (size_t i = 0; i < estudiantes.size(); i++) {
        if (estudiantes[i].identificacion == id) {
            estudiantes.erase(estudiantes.begin() + i);
            cout << "Estudiante eliminado permanentemente.\n";
            return;
        }
    }
    cout << "Estudiante no encontrado.\n";
}

// ---- Matricula / cancelacion (operan sobre la lista anidada) ----

void matricularCurso(vector<Estudiante>& estudiantes, const string& id, vector<Curso>& cursos) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }

    string codigoCurso;
    cout << "Codigo del curso a matricular: ";
    cin >> codigoCurso;

    Curso* c = buscarCurso(cursos, codigoCurso);
    if (!c) { cout << "Ese curso no existe.\n"; return; }
    if (!c->activo) { cout << "Ese curso esta inactivo.\n"; return; }

    // Evitar doble matricula en el mismo curso
    for (const auto& m : e->matriculas) {
        if (m.codigoCurso == codigoCurso) {
            cout << "El estudiante ya esta matriculado en ese curso.\n";
            return;
        }
    }

    Matricula m;
    m.codigoCurso = codigoCurso;
    m.nota = 0.0f; // nota inicial, se actualiza despues (o se pide aqui mismo)
    cout << "Nota (0.0 si aun no tiene, se puede modificar despues): ";
    cin >> m.nota;

    e->matriculas.push_back(m);
    cout << "Matricula registrada correctamente.\n";
}

void cancelarCurso(vector<Estudiante>& estudiantes, const string& id) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }

    string codigoCurso;
    cout << "Codigo del curso a cancelar: ";
    cin >> codigoCurso;

    for (size_t i = 0; i < e->matriculas.size(); i++) {
        if (e->matriculas[i].codigoCurso == codigoCurso) {
            e->matriculas.erase(e->matriculas.begin() + i);
            cout << "Curso cancelado (retirado de la matricula).\n";
            return;
        }
    }
    cout << "El estudiante no esta matriculado en ese curso.\n";
}

// ---- Promedio y alerta EBRA ----

float calcularPromedio(const Estudiante& e) {
    if (e.matriculas.empty()) return 0.0f;
    float suma = 0.0f;
    for (const auto& m : e.matriculas) suma += m.nota;
    return suma / e.matriculas.size();
}

bool estaEnRiesgoEbra(const Estudiante& e) {
    // EBRA: riesgo de desercion academica, promedio por debajo de 3.25
    return calcularPromedio(e) < 3.25f;
}

void consultarEstudiante(vector<Estudiante>& estudiantes, const string& id) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }

    cout << "\n===== Ficha del estudiante =====\n";
    cout << "ID: " << e->identificacion << " | " << e->nombreCompleto << "\n";
    cout << "Programa: " << e->codigoPrograma << " | Estado: " << e->estado << "\n";
    cout << "Cursos matriculados:\n";
    if (e->matriculas.empty()) {
        cout << "  (ninguno)\n";
    } else {
        for (const auto& m : e->matriculas) {
            cout << "  " << m.codigoCurso << " -> nota: " << m.nota << "\n";
        }
    }
    cout << "Promedio acumulado: " << calcularPromedio(*e) << "\n";
    if (estaEnRiesgoEbra(*e)) {
        cout << "*** ALERTA EBRA: estudiante en riesgo de desercion academica"
             << " (promedio < 3.25) ***\n";
    }
    cout << "=================================\n";
}

// =========================================================================
// PROFESORES, ADMINISTRATIVOS
// TODO: replicar el mismo patron (Dia 7 del cronograma).
// Los prototipos ya estan declarados en gestion.h.
// =========================================================================
