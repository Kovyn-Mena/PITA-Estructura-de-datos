#include "../include/gestion.h"
#include "../include/interfaz.h"
#include "../include/nomina.h"
#include <iostream>
#include <limits>
#include <iomanip>

using namespace std;

// =========================================================================
// FACULTADES — implementacion completa, usar como PATRON para las demas
// entidades (Programa, Curso, Estudiante, Profesor, Administrativo).
//
// Nota de diseño: todos los campos de "codigo/identificacion" se leen con
// leerPalabra(), que YA deja el buffer de entrada limpio (sin '\n'
// pendiente), asi que los getline() que siguen funcionan bien a la
// primera. Ademas, escribir la palabra "cancelar" en ese campo aborta la
// creacion sin guardar nada — util si se entro al menu por error.
// =========================================================================

void crearFacultad(vector<Facultad>& facultades) {
    Facultad f;
    f.codigo = leerPalabra("Codigo facultad (o 'cancelar' para volver): ");
    if (esCancelar(f.codigo)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarFacultad(facultades, f.codigo) != nullptr) {
        cout << "Ya existe una facultad con ese codigo.\n";
        return;
    }

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
// facultad exista y este activa antes de crear el programa.
// =========================================================================

void crearPrograma(vector<Programa>& programas, vector<Facultad>& facultades) {
    Programa p;
    p.codigo = leerPalabra("Codigo programa (o 'cancelar' para volver): ");
    if (esCancelar(p.codigo)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarPrograma(programas, p.codigo) != nullptr) {
        cout << "Ya existe un programa con ese codigo.\n";
        return;
    }

    p.codigoFacultad = leerPalabra("Codigo de la facultad a la que pertenece: ");
    if (esCancelar(p.codigoFacultad)) { cout << "Operacion cancelada.\n"; return; }

    Facultad* f = buscarFacultad(facultades, p.codigoFacultad);
    if (!f) {
        cout << "Esa facultad no existe. Cree primero la facultad.\n";
        return;
    }
    if (!f->activo) {
        cout << "Esa facultad esta inactiva, no se le pueden asociar programas.\n";
        return;
    }

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
    c.codigo = leerPalabra("Codigo curso (o 'cancelar' para volver): ");
    if (esCancelar(c.codigo)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarCurso(cursos, c.codigo) != nullptr) {
        cout << "Ya existe un curso con ese codigo.\n";
        return;
    }

    c.codigoPrograma = leerPalabra("Codigo del programa al que pertenece: ");
    if (esCancelar(c.codigoPrograma)) { cout << "Operacion cancelada.\n"; return; }

    Programa* p = buscarPrograma(programas, c.codigoPrograma);
    if (!p) {
        cout << "Ese programa no existe. Cree primero el programa.\n";
        return;
    }
    if (!p->activo) {
        cout << "Ese programa esta inactivo, no se le pueden asociar cursos.\n";
        return;
    }

    cout << "Nombre del curso: ";
    getline(cin, c.nombre);
    cout << "Creditos: ";
    c.creditos = leerEntero();
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

    cout << "Nuevo nombre (" << c->nombre << "): ";
    getline(cin, c->nombre);
    cout << "Nuevos creditos (" << c->creditos << "): ";
    c->creditos = leerEntero();
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
    e.identificacion = leerPalabra("Identificacion (o 'cancelar' para volver): ");
    if (esCancelar(e.identificacion)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarEstudiante(estudiantes, e.identificacion) != nullptr) {
        cout << "Ya existe un estudiante con esa identificacion.\n";
        return;
    }

    e.codigoPrograma = leerPalabra("Codigo del programa al que pertenece: ");
    if (esCancelar(e.codigoPrograma)) { cout << "Operacion cancelada.\n"; return; }

    Programa* p = buscarPrograma(programas, e.codigoPrograma);
    if (!p) {
        cout << "Ese programa no existe. Cree primero el programa.\n";
        return;
    }

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

    string codigoCurso = leerPalabra("Codigo del curso a matricular (o 'cancelar' para volver): ");
    if (esCancelar(codigoCurso)) { cout << "Operacion cancelada.\n"; return; }

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
    cout << "Nota (0.0 si aun no tiene, se puede modificar despues): ";
    m.nota = static_cast<float>(leerEntero()); // nota simple, se puede volver float editable en modificar
    // Nota: si se quiere permitir decimales aqui mismo, se puede leer con
    // cin >> m.nota directamente (float), siguiendo el mismo cuidado de
    // limpiar el buffer despues. Se deja como mejora futura.

    e->matriculas.push_back(m);
    cout << "Matricula registrada correctamente.\n";
}

void cancelarCurso(vector<Estudiante>& estudiantes, const string& id) {
    Estudiante* e = buscarEstudiante(estudiantes, id);
    if (!e) { cout << "Estudiante no encontrado.\n"; return; }

    string codigoCurso = leerPalabra("Codigo del curso a cancelar (o 'cancelar' para volver sin retirar nada): ");
    if (esCancelar(codigoCurso)) { cout << "Operacion cancelada.\n"; return; }

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
    // EBRA: riesgo de desercion academica, promedio por debajo de 3.25.
    // Un estudiante SIN matriculas aun no tiene base para evaluarse,
    // asi que no se marca en riesgo (evita falsos positivos).
    if (e.matriculas.empty()) return false;
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
// PROFESORES — el campo tipoVinculacion/dedicacion/categoriaEscalafon se
// pide por MENU numerado (no texto libre), porque nomina.cpp compara estos
// valores con strings exactos ("Planta", "Asociado", etc.): un error de
// tedeo aqui daria un salario silenciosamente incorrecto. Con menu, eso
// no puede pasar.
// =========================================================================

static string seleccionarTipoVinculacion() {
    cout << "Tipo de vinculacion:\n  1. Planta\n  2. Ocasional\n  3. Catedratico\n";
    int op = leerOpcionInmediata("Opcion: ");
    if (op == 1) return "Planta";
    if (op == 2) return "Ocasional";
    return "Catedratico"; // cualquier otra tecla cae aqui como valor por defecto seguro
}

static string seleccionarDedicacion() {
    cout << "Dedicacion:\n  1. Tiempo completo\n  2. Medio tiempo\n";
    int op = leerOpcionInmediata("Opcion: ");
    return (op == 2) ? "MedioTiempo" : "TiempoCompleto";
}

static string seleccionarCategoriaEscalafon() {
    cout << "Categoria del escalafon:\n  1. Auxiliar\n  2. Asistente\n  3. Asociado\n  4. Titular\n";
    int op = leerOpcionInmediata("Opcion: ");
    switch (op) {
        case 1: return "Auxiliar";
        case 2: return "Asistente";
        case 3: return "Asociado";
        case 4: return "Titular";
        default: return "Auxiliar";
    }
}

void crearProfesor(vector<Profesor>& profesores, vector<Programa>& programas) {
    Profesor p;
    p.identificacion = leerPalabra("Identificacion (o 'cancelar' para volver): ");
    if (esCancelar(p.identificacion)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarProfesor(profesores, p.identificacion) != nullptr) {
        cout << "Ya existe un profesor con esa identificacion.\n";
        return;
    }

    p.codigoPrograma = leerPalabra("Codigo del programa al que pertenece: ");
    if (esCancelar(p.codigoPrograma)) { cout << "Operacion cancelada.\n"; return; }

    Programa* prog = buscarPrograma(programas, p.codigoPrograma);
    if (!prog) {
        cout << "Ese programa no existe. Cree primero el programa.\n";
        return;
    }

    cout << "Nombre completo: ";
    getline(cin, p.nombreCompleto);

    p.tipoVinculacion = seleccionarTipoVinculacion();

    if (p.tipoVinculacion == "Catedratico") {
        // Segun el Acuerdo 027/2024: catedra, maximo 18 horas semanales.
        do {
            cout << "Horas catedra semanales (maximo 18): ";
            p.horasCatedraSemanales = leerEntero();
            if (p.horasCatedraSemanales > 18) {
                cout << "El Acuerdo 027/2024 permite maximo 18 horas semanales. Intente de nuevo.\n";
            }
        } while (p.horasCatedraSemanales > 18 || p.horasCatedraSemanales <= 0);
        p.dedicacion = "HorasCatedra";
        p.categoriaEscalafon = ""; // los catedraticos no tienen escalafon formal en este modelo
        p.adHonorem = (leerSiNo("Es vinculacion ad-honorem, sin remuneracion? (s/n): ") == 's');
    } else {
        p.dedicacion = seleccionarDedicacion();
        p.categoriaEscalafon = seleccionarCategoriaEscalafon();
        p.horasCatedraSemanales = 0;
        p.adHonorem = false;
    }

    cout << "Anios de experiencia: ";
    p.aniosExperiencia = leerEntero();
    cout << "Puntos por titulos academicos: ";
    p.puntosTitulos = leerEntero();
    cout << "Puntos por productividad academica: ";
    p.puntosProductividad = leerEntero();
    p.activo = true;

    profesores.push_back(p);
    cout << "Profesor creado correctamente.\n";
}

void listarProfesores(const vector<Profesor>& profesores) {
    cout << "\n--- Profesores registrados ---\n";
    if (profesores.empty()) {
        cout << "(no hay profesores registrados)\n";
        return;
    }
    for (const auto& p : profesores) {
        cout << p.identificacion << " | " << p.nombreCompleto
             << " | Programa: " << p.codigoPrograma
             << " | " << p.tipoVinculacion << " (" << p.dedicacion << ")";
        if (!p.categoriaEscalafon.empty()) cout << " | Categoria: " << p.categoriaEscalafon;
        if (p.adHonorem) cout << " | AD-HONOREM";
        cout << " | " << (p.activo ? "Activo" : "Inactivo") << "\n";
    }
}

Profesor* buscarProfesor(vector<Profesor>& profesores, const string& id) {
    for (auto& p : profesores) {
        if (p.identificacion == id) return &p;
    }
    return nullptr;
}

void modificarProfesor(vector<Profesor>& profesores, const string& id) {
    Profesor* p = buscarProfesor(profesores, id);
    if (!p) { cout << "Profesor no encontrado.\n"; return; }

    cout << "Nuevo nombre (" << p->nombreCompleto << "): ";
    getline(cin, p->nombreCompleto);
    cout << "Nuevos anios de experiencia (" << p->aniosExperiencia << "): ";
    p->aniosExperiencia = leerEntero();
    cout << "Nuevos puntos por titulos (" << p->puntosTitulos << "): ";
    p->puntosTitulos = leerEntero();
    cout << "Nuevos puntos por productividad (" << p->puntosProductividad << "): ";
    p->puntosProductividad = leerEntero();
    cout << "Profesor modificado.\n";
}

void desactivarProfesor(vector<Profesor>& profesores, const string& id) {
    Profesor* p = buscarProfesor(profesores, id);
    if (!p) { cout << "Profesor no encontrado.\n"; return; }
    p->activo = false;
    cout << "Profesor desactivado (borrado logico).\n";
}

void eliminarProfesor(vector<Profesor>& profesores, const string& id) {
    for (size_t i = 0; i < profesores.size(); i++) {
        if (profesores[i].identificacion == id) {
            profesores.erase(profesores.begin() + i);
            cout << "Profesor eliminado permanentemente.\n";
            return;
        }
    }
    cout << "Profesor no encontrado.\n";
}

void consultarProfesor(vector<Profesor>& profesores, const string& id) {
    Profesor* p = buscarProfesor(profesores, id);
    if (!p) { cout << "Profesor no encontrado.\n"; return; }
    imprimirDesgloseNomina(*p); // definida en nomina.cpp
}

// =========================================================================
// ADMINISTRATIVOS — mismo patron que las demas entidades. La facultad es
// OPCIONAL (vacia = nivel central, ej. Rectoria); si se indica, se valida
// que exista. El tipo de contratacion se elige por menu numerado (igual
// que en Profesor) para no arriesgar el calculo del salario por un
// error de tipeo.
// =========================================================================

void crearAdministrativo(vector<Administrativo>& admins, vector<Facultad>& facultades) {
    Administrativo a;
    a.identificacion = leerPalabra("Identificacion (o 'cancelar' para volver): ");
    if (esCancelar(a.identificacion)) { cout << "Operacion cancelada.\n"; return; }

    if (buscarAdministrativo(admins, a.identificacion) != nullptr) {
        cout << "Ya existe un administrativo con esa identificacion.\n";
        return;
    }

    cout << "Nombre completo: ";
    getline(cin, a.nombreCompleto);

    cout << "Cargo (ej. Secretario Academico, Auxiliar Financiero): ";
    getline(cin, a.cargo);

    cout << "\nCategoria (Escala Salarial):\n";
    cout << "1. Nivel 1 (Asistencial/Auxiliar - $1.950.000)\n";
    cout << "2. Nivel 2 (Tecnico/Secretarial - $2.800.000)\n";
    cout << "3. Nivel 3 (Profesional/Coordinador - $3.750.000)\n";
    cout << "4. Nivel 4 (Directivo/Asesor/Jefe - $5.050.000)\n";
    cout << "Opcion: ";
    int catOp = leerEntero();
    switch (catOp) {
        case 2: a.categoria = "Nivel 2"; break;
        case 3: a.categoria = "Nivel 3"; break;
        case 4: a.categoria = "Nivel 4"; break;
        default: a.categoria = "Nivel 1"; break;
    }

    a.codigoFacultad = leerPalabra("Codigo de facultad (ENTER en blanco = nivel central): ");
    if (!a.codigoFacultad.empty()) {
        if (buscarFacultad(facultades, a.codigoFacultad) == nullptr) {
            cout << "Esa facultad no existe. Cree primero la facultad, o deje en blanco para nivel central.\n";
            return;
        }
    }

    cout << "\nTipo de contratacion:\n";
    cout << "1. Planta\n2. Provisional\n3. Contrato\n";
    cout << "Opcion: ";
    int tipoOpcion = leerEntero();
    switch (tipoOpcion) {
        case 1: a.tipoContratacion = "Planta"; break;
        case 2: a.tipoContratacion = "Provisional"; break;
        case 3: a.tipoContratacion = "Contrato"; break;
        default:
            cout << "Opcion de tipo de contratacion invalida.\n";
            return;
    }

    cout << "Salario base (0 para asignar segun escala legal " << a.categoria << "): ";
    double salInput = leerEntero();
    if (salInput <= 0) {
        salInput = salarioBaseAdministrativo(a.categoria);
    }
    a.salarioBase = salInput;

    a.activo = true;
    admins.push_back(a);
    cout << "Administrativo creado correctamente con salario base de $" << a.salarioBase << " COP.\n";
}

void listarAdministrativos(const vector<Administrativo>& admins) {
    cout << "\n--- Administrativos registrados ---\n";
    if (admins.empty()) {
        cout << "(no hay administrativos registrados)\n";
        return;
    }
    cout << fixed << setprecision(0);
    for (const auto& a : admins) {
        cout << a.identificacion << " | " << a.nombreCompleto << " | " << a.cargo
             << " | " << a.categoria << " | " << a.tipoContratacion
             << " | Facultad: " << (a.codigoFacultad.empty() ? "(nivel central)" : a.codigoFacultad)
             << " | Salario base: $" << a.salarioBase << " COP"
             << " | " << (a.activo ? "Activo" : "Inactivo") << "\n";
    }
}

Administrativo* buscarAdministrativo(vector<Administrativo>& admins, const string& id) {
    for (auto& a : admins) {
        if (a.identificacion == id) return &a;
    }
    return nullptr;
}

void modificarAdministrativo(vector<Administrativo>& admins, const string& id) {
    Administrativo* a = buscarAdministrativo(admins, id);
    if (!a) { cout << "Administrativo no encontrado.\n"; return; }

    cout << "Nuevo nombre (" << a->nombreCompleto << "): ";
    getline(cin, a->nombreCompleto);
    cout << "Nuevo cargo (" << a->cargo << "): ";
    getline(cin, a->cargo);
    cout << "Nuevo salario base (" << a->salarioBase << " COP - 0 para recalcular segun escala): ";
    double nuevoSal = leerEntero();
    if (nuevoSal <= 0) {
        a->salarioBase = salarioBaseAdministrativo(a->categoria);
    } else {
        a->salarioBase = nuevoSal;
    }
    cout << "Administrativo modificado con salario base de $" << a->salarioBase << " COP.\n";
}

void desactivarAdministrativo(vector<Administrativo>& admins, const string& id) {
    Administrativo* a = buscarAdministrativo(admins, id);
    if (!a) { cout << "Administrativo no encontrado.\n"; return; }
    a->activo = false;
    cout << "Administrativo desactivado (borrado logico).\n";
}

void eliminarAdministrativo(vector<Administrativo>& admins, const string& id) {
    for (size_t i = 0; i < admins.size(); i++) {
        if (admins[i].identificacion == id) {
            admins.erase(admins.begin() + i);
            cout << "Administrativo eliminado permanentemente.\n";
            return;
        }
    }
    cout << "Administrativo no encontrado.\n";
}
