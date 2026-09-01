#include "../include/entidades.h"
#include "../include/gestion.h"
#include "../include/nomina.h"
#include "../include/persistencia.h"
#include <iostream>
#include <limits>

using namespace std;

const string RUTA_FACULTADES = "data/facultades.txt";
const string RUTA_PROGRAMAS = "data/programas.txt";
const string RUTA_CURSOS = "data/cursos.txt";
// TODO: agregar rutas de los demas archivos de datos a medida que se implementen.

// Lee un entero de forma segura: si el usuario escribe texto en vez de un
// numero, cin queda en estado de error y (sin este manejo) el programa
// entra en loop infinito. Se limpia el error y se descarta la linea mala.
int leerOpcion() {
    int valor;
    cin >> valor;
    if (cin.fail()) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        return -1; // valor invalido, no coincide con ningun caso del menu
    }
    return valor;
}

void menuFacultades(vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        cout << "\n--- Menu Facultades ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

        string codigo;
        switch (opcion) {
            case 1: crearFacultad(facultades); break;
            case 2: listarFacultades(facultades); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarFacultad(facultades, codigo);
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarFacultad(facultades, codigo);
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                eliminarFacultad(facultades, codigo);
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n";
        }
    } while (opcion != 0);
}

void menuProgramas(vector<Programa>& programas, vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        cout << "\n--- Menu Programas ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

        string codigo;
        switch (opcion) {
            case 1: crearPrograma(programas, facultades); break;
            case 2: listarProgramas(programas); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarPrograma(programas, codigo);
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarPrograma(programas, codigo);
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                eliminarPrograma(programas, codigo);
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n";
        }
    } while (opcion != 0);
}

void menuCursos(vector<Curso>& cursos, vector<Programa>& programas) {
    int opcion = -1;
    do {
        cout << "\n--- Menu Cursos ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        opcion = leerOpcion();

        string codigo;
        switch (opcion) {
            case 1: crearCurso(cursos, programas); break;
            case 2: listarCursos(cursos); break;
            case 3:
                cout << "Codigo a modificar: "; cin >> codigo;
                modificarCurso(cursos, codigo);
                break;
            case 4:
                cout << "Codigo a desactivar: "; cin >> codigo;
                desactivarCurso(cursos, codigo);
                break;
            case 5:
                cout << "Codigo a eliminar: "; cin >> codigo;
                eliminarCurso(cursos, codigo);
                break;
            case 0: break;
            default: cout << "Opcion invalida.\n";
        }
    } while (opcion != 0);
}

int main() {
    cout << "=====================================================\n";
    cout << " PITA - Programa Integrado de Transacciones Academicas\n";
    cout << " Universidad Popular del Cesar\n";
    cout << "=====================================================\n";

    vector<Facultad> facultades;
    vector<Programa> programas;
    vector<Curso> cursos;

    // Requisito del taller: el usuario decide si cargar datos existentes.
    char respuesta;
    cout << "\nDesea cargar los datos existentes? (s/n): ";
    cin >> respuesta;
    if (respuesta == 's' || respuesta == 'S') {
        facultades = cargarFacultades(RUTA_FACULTADES);
        programas = cargarProgramas(RUTA_PROGRAMAS);
        cursos = cargarCursos(RUTA_CURSOS);
        cout << "Datos cargados: " << facultades.size() << " facultad(es), "
             << programas.size() << " programa(s), " << cursos.size() << " curso(s).\n";
    } else {
        cout << "Iniciando sin datos precargados.\n";
    }

    int opcionPrincipal = -1;
    do {
        cout << "\n===== MENU PRINCIPAL =====\n";
        cout << "1. Gestionar Facultades\n";
        cout << "2. Gestionar Programas\n";
        cout << "3. Gestionar Cursos\n";
        cout << "4. Gestionar Estudiantes     [TODO]\n";
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
                break;
            }
            case 0:
                guardarFacultades(facultades, RUTA_FACULTADES);
                guardarProgramas(programas, RUTA_PROGRAMAS);
                guardarCursos(cursos, RUTA_CURSOS);
                cout << "Datos guardados. Hasta luego.\n";
                break;
            default:
                cout << "Opcion no disponible todavia o invalida.\n";
        }
    } while (opcionPrincipal != 0);

    return 0;
}
