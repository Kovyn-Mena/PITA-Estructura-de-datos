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
// TODO: agregar rutas de los demas archivos de datos a medida que se implementen.

// NOTA DE DISEÑO (pantalla): cada menu limpia la pantalla ANTES de
// dibujarse, y hace pausar() DESPUES de cada accion (excepto "Volver").
// Asi el usuario siempre alcanza a leer el resultado de lo que hizo antes
// de que la pantalla se borre para mostrar el menu de nuevo.

void menuFacultades(vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        limpiarPantalla();
        cout << "\n--- Menu Facultades ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

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
                eliminarFacultad(facultades, codigo);
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
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

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
                eliminarPrograma(programas, codigo);
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
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

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
                eliminarCurso(cursos, codigo);
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
        cout << "0. Volver\nOpcion: ";
        opcion = leerOpcion();

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
                eliminarEstudiante(estudiantes, id);
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

    // Requisito del taller: el usuario decide si cargar datos existentes.
    // leerSiNo() detecta la respuesta con una sola tecla, sin esperar ENTER,
    // y no deja avanzar si se digita algo distinto de 's' o 'n'.
    char respuesta = leerSiNo("\nDesea cargar los datos existentes? (s/n): ");
    if (respuesta == 's') {
        facultades = cargarFacultades(RUTA_FACULTADES);
        programas = cargarProgramas(RUTA_PROGRAMAS);
        cursos = cargarCursos(RUTA_CURSOS);
        estudiantes = cargarEstudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS);
        cout << "Datos cargados: " << facultades.size() << " facultad(es), "
             << programas.size() << " programa(s), " << cursos.size() << " curso(s), "
             << estudiantes.size() << " estudiante(s).\n";
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
        cout << "5. Gestionar Profesores      [TODO]\n";
        cout << "6. Gestionar Administrativos [TODO]\n";
        cout << "7. Simular nomina de un profesor (demo)\n";
        cout << "0. Guardar y salir\n";
        cout << "Opcion: ";
        opcionPrincipal = leerOpcion();

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
            case 7: {
                // Profesor de ejemplo para demostrar el modulo de nomina
                // mientras se conecta con la gestion real de profesores.
                Profesor demo;
                demo.nombreCompleto = "Profesor de ejemplo";
                demo.tipoVinculacion = "Planta";
                demo.dedicacion = "TiempoCompleto";
                demo.categoriaEscalafon = "Asociado";
                demo.horasCatedraSemanales = 0;
                demo.adHonorem = false;
                demo.aniosExperiencia = 8;
                demo.puntosTitulos = 60;
                demo.puntosProductividad = 15;
                demo.activo = true;
                imprimirDesgloseNomina(demo);
                pausar();
                break;
            }
            case 0:
                guardarFacultades(facultades, RUTA_FACULTADES);
                guardarProgramas(programas, RUTA_PROGRAMAS);
                guardarCursos(cursos, RUTA_CURSOS);
                guardarEstudiantes(estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS);
                cout << "Datos guardados. Hasta luego.\n";
                break;
            default:
                cout << "Opcion no disponible todavia o invalida.\n";
                pausar();
        }
    } while (opcionPrincipal != 0);

    return 0;
}
