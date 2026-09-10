#include "../include/entidades.h"
#include "../include/gestion.h"
#include "../include/nomina.h"
#include "../include/persistencia.h"
#include "../include/interfaz.h"
#include <iostream>

using namespace std;

const string RUTA_FACULTADES = "data/facultades.txt";
const string RUTA_PROGRAMAS = "data/programas.txt";
const string RUTA_CURSOS = "data/cursos.txt";
const string RUTA_ESTUDIANTES = "data/estudiantes.txt";
const string RUTA_MATRICULAS = "data/matriculas.txt";
const string RUTA_PROFESORES = "data/profesores.txt";
const string RUTA_ADMINISTRATIVOS = "data/administrativos.txt";

// NOTA DE DISEÑO (pantalla): cada menu limpia la pantalla ANTES de
// dibujarse, y hace pausar() DESPUES de cada accion (excepto "Volver").
// Asi el usuario siempre alcanza a leer el resultado de lo que hizo antes
// de que la pantalla se borre para mostrar el menu de nuevo.
//
// NOTA DE DISEÑO (confirmacion): las acciones irreversibles (Eliminar,
// que es borrado FISICO) piden confirmacion con leerSiNo() antes de
// ejecutarse. Si el usuario responde 'n', la operacion se cancela sin
// tocar los datos — asi siempre hay forma de "volver atras" antes de
// una accion que no se puede deshacer.

void menuFacultades(vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Facultades ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string codigo;
        switch (opcion) {
            case 1: crearFacultad(facultades); pausar(); break;
            case 2: listarFacultades(facultades); pausar(); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarFacultad(facultades, codigo);
                pausar();
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarFacultad(facultades, codigo);
                pausar();
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarFacultad(facultades, codigo);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 0: break; // "Volver" no necesita pausa
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

void menuProgramas(vector<Programa>& programas, vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Programas ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string codigo;
        switch (opcion) {
            case 1: crearPrograma(programas, facultades); pausar(); break;
            case 2: listarProgramas(programas); pausar(); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarPrograma(programas, codigo);
                pausar();
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarPrograma(programas, codigo);
                pausar();
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarPrograma(programas, codigo);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

void menuCursos(vector<Curso>& cursos, vector<Programa>& programas) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Cursos ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string codigo;
        switch (opcion) {
            case 1: crearCurso(cursos, programas); pausar(); break;
            case 2: listarCursos(cursos); pausar(); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarCurso(cursos, codigo);
                pausar();
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarCurso(cursos, codigo);
                pausar();
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarCurso(cursos, codigo);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

void menuEstudiantes(vector<Estudiante>& estudiantes, vector<Programa>& programas, vector<Curso>& cursos) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Estudiantes ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n";
        cout << "6. Matricular curso\n7. Cancelar curso\n8. Ver ficha (promedio + alerta EBRA)\n";
        cout << "0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string id;
        switch (opcion) {
            case 1: crearEstudiante(estudiantes, programas); pausar(); break;
            case 2: listarEstudiantes(estudiantes); pausar(); break;
            case 3:
                cout << "Identificacion a modificar: "; cin >> id;
                modificarEstudiante(estudiantes, id);
                pausar();
                break;
            case 4:
                cout << "Identificacion a desactivar: "; cin >> id;
                desactivarEstudiante(estudiantes, id);
                pausar();
                break;
            case 5:
                cout << "Identificacion a eliminar: "; cin >> id;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarEstudiante(estudiantes, id);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 6:
                cout << "Identificacion del estudiante: "; cin >> id;
                matricularCurso(estudiantes, id, cursos);
                pausar();
                break;
            case 7:
                cout << "Identificacion del estudiante: "; cin >> id;
                cancelarCurso(estudiantes, id);
                pausar();
                break;
            case 8:
                cout << "Identificacion del estudiante: "; cin >> id;
                consultarEstudiante(estudiantes, id);
                pausar();
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

void menuProfesores(vector<Profesor>& profesores, vector<Programa>& programas) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Profesores ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n";
        cout << "6. Ver desglose de nomina\n0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string id;
        switch (opcion) {
            case 1: crearProfesor(profesores, programas); pausar(); break;
            case 2: listarProfesores(profesores); pausar(); break;
            case 3:
                cout << "Identificacion a modificar: "; cin >> id;
                modificarProfesor(profesores, id);
                pausar();
                break;
            case 4:
                cout << "Identificacion a desactivar: "; cin >> id;
                desactivarProfesor(profesores, id);
                pausar();
                break;
            case 5:
                cout << "Identificacion a eliminar: "; cin >> id;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarProfesor(profesores, id);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 6:
                cout << "Identificacion del profesor: "; cin >> id;
                consultarProfesor(profesores, id);
                pausar();
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

void menuAdministrativos(vector<Administrativo>& admins, vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Administrativos ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n";
        cout << "6. Ver liquidacion de nomina\n0. Volver (o presione ENTER)\n";
        opcion = leerOpcionInmediata("Opcion: ");

        string id;
        switch (opcion) {
            case 1: crearAdministrativo(admins, facultades); pausar(); break;
            case 2: listarAdministrativos(admins); pausar(); break;
            case 3:
                cout << "Identificacion a modificar: "; cin >> id;
                modificarAdministrativo(admins, id);
                pausar();
                break;
            case 4:
                cout << "Identificacion a desactivar: "; cin >> id;
                desactivarAdministrativo(admins, id);
                pausar();
                break;
            case 5:
                cout << "Identificacion a eliminar: "; cin >> id;
                if (leerSiNo("Esta accion NO se puede deshacer. Confirma? (s/n): ") == 's') {
                    eliminarAdministrativo(admins, id);
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 6: {
                cout << "Identificacion del administrativo: "; cin >> id;
                Administrativo* a = buscarAdministrativo(admins, id);
                if (a) {
                    imprimirDesgloseNominaAdmin(*a);
                } else {
                    cout << "Administrativo no encontrado.\n";
                }
                pausar();
                break;
            }
            case 0: break;
            default: cout << "Opcion invalida.\n"; pausar();
        }
    } while (opcion != 0);
}

int main() {
    limpiarPantalla();
    cout << "=====================================================\n";
    cout << " PITA - Programa Integrado de Transacciones Academicas\n";
    cout << " Universidad Popular del Cesar\n";
    cout << "=====================================================\n";

    vector<Facultad> facultades;
    vector<Programa> programas;
    vector<Curso> cursos;
    vector<Estudiante> estudiantes;
    vector<Profesor> profesores;
    vector<Administrativo> administrativos;

    // Requisito del taller: el usuario decide si cargar datos existentes.
    // leerSiNo() detecta la respuesta con una sola tecla, sin esperar ENTER,
    // y no deja avanzar si se digita algo distinto de 's' o 'n'.
    // Si el usuario se equivoca aqui, no queda atrapado: en el menu
    // principal existe la opcion "Recargar datos desde archivo" (7) para
    // corregirlo sin tener que cerrar y volver a abrir el programa.
    char respuesta = leerSiNo("\nDesea cargar los datos existentes? (s/n): ");
    if (respuesta == 's') {
        facultades = cargarFacultades(RUTA_FACULTADES);
        programas = cargarProgramas(RUTA_PROGRAMAS);
        cursos = cargarCursos(RUTA_CURSOS);
        estudiantes = cargarEstudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS);
        profesores = cargarProfesores(RUTA_PROFESORES);
        administrativos = cargarAdministrativos(RUTA_ADMINISTRATIVOS);
        cout << "Datos cargados: " << facultades.size() << " facultad(es), "
             << programas.size() << " programa(s), " << cursos.size() << " curso(s), "
             << estudiantes.size() << " estudiante(s), " << profesores.size() << " profesor(es), "
             << administrativos.size() << " administrativo(s).\n";
    } else {
        cout << "Iniciando sin datos precargados.\n";
    }
    pausar();

    int opcionPrincipal = -1;
    do {
        limpiarPantalla();
        cout << "\n===== MENU PRINCIPAL =====\n";
        cout << "1. Gestionar Facultades\n";
        cout << "2. Gestionar Programas\n";
        cout << "3. Gestionar Cursos\n";
        cout << "4. Gestionar Estudiantes\n";
        cout << "5. Gestionar Profesores\n";
        cout << "6. Gestionar Administrativos\n";
        cout << "7. Recargar datos desde archivo\n";
        cout << "0. Guardar y salir (o presione ENTER)\n";
        opcionPrincipal = leerOpcionInmediata("Opcion: ");

        switch (opcionPrincipal) {
            case 1:
                menuFacultades(facultades);
                break;
            case 2:
                menuProgramas(programas, facultades);
                break;
            case 3:
                menuCursos(cursos, programas);
                break;
            case 4:
                menuEstudiantes(estudiantes, programas, cursos);
                break;
            case 5:
                menuProfesores(profesores, programas);
                break;
            case 6:
                menuAdministrativos(administrativos, facultades);
                break;
            case 7:
                // "Volver atras" ante un error al inicio: descarta lo que
                // haya en memoria (sin guardar) y recarga tal cual esta
                // en disco. Pide confirmacion porque SI se pierden cambios
                // no guardados.
                if (leerSiNo("Se perdera lo que no haya guardado. Continuar? (s/n): ") == 's') {
                    facultades = cargarFacultades(RUTA_FACULTADES);
                    programas = cargarProgramas(RUTA_PROGRAMAS);
                    cursos = cargarCursos(RUTA_CURSOS);
                    estudiantes = cargarEstudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS);
                    profesores = cargarProfesores(RUTA_PROFESORES);
                    administrativos = cargarAdministrativos(RUTA_ADMINISTRATIVOS);
                    cout << "Datos recargados desde archivo: " << facultades.size() << " facultad(es), "
                         << programas.size() << " programa(s), " << cursos.size() << " curso(s), "
                         << estudiantes.size() << " estudiante(s), " << profesores.size() << " profesor(es), "
                         << administrativos.size() << " administrativo(s).\n";
                } else {
                    cout << "Operacion cancelada.\n";
                }
                pausar();
                break;
            case 0:
                guardarFacultades(facultades, RUTA_FACULTADES);
                guardarProgramas(programas, RUTA_PROGRAMAS);
                guardarCursos(cursos, RUTA_CURSOS);
                guardarEstudiantes(estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS);
                guardarProfesores(profesores, RUTA_PROFESORES);
                guardarAdministrativos(administrativos, RUTA_ADMINISTRATIVOS);
                cout << "Datos guardados. Hasta luego.\n";
                break;
            default:
                cout << "Opcion no disponible todavia o invalida.\n";
                pausar();
        }
    } while (opcionPrincipal != 0);

    return 0;
}
