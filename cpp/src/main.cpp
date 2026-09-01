#include "../include/entidades.h"
#include "../include/gestion.h"
#include "../include/nomina.h"
#include "../include/persistencia.h"
#include <iostream>
#include <limits>

using namespace std;

const string RUTA_FACULTADES = "data/facultades.txt";
// TODO: agregar rutas de los demas archivos de datos a medida que se implementen.

void menuFacultades(vector<Facultad>& facultades) {
    int opcion = -1;
    do {
        cout << "\n--- Menu Facultades ---\n";
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver\n";
        cout << "Opcion: ";
        cin >> opcion;

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

int main() {
    cout << "=====================================================\n";
    cout << " PITA - Programa Integrado de Transacciones Academicas\n";
    cout << " Universidad Popular del Cesar\n";
    cout << "=====================================================\n";

    vector<Facultad> facultades;

    // Requisito del taller: el usuario decide si cargar datos existentes.
    char respuesta;
    cout << "\nDesea cargar los datos existentes? (s/n): ";
    cin >> respuesta;
    if (respuesta == 's' || respuesta == 'S') {
        facultades = cargarFacultades(RUTA_FACULTADES);
        cout << "Datos cargados: " << facultades.size() << " facultad(es).\n";
    } else {
        cout << "Iniciando sin datos precargados.\n";
    }

    int opcionPrincipal = -1;
    do {
        cout << "\n===== MENU PRINCIPAL =====\n";
        cout << "1. Gestionar Facultades\n";
        cout << "2. Gestionar Programas       [TODO]\n";
        cout << "3. Gestionar Cursos          [TODO]\n";
        cout << "4. Gestionar Estudiantes     [TODO]\n";
        cout << "5. Gestionar Profesores      [TODO]\n";
        cout << "6. Gestionar Administrativos [TODO]\n";
        cout << "7. Simular nomina de un profesor (demo)\n";
        cout << "0. Guardar y salir\n";
        cout << "Opcion: ";
        cin >> opcionPrincipal;

        switch (opcionPrincipal) {
            case 1:
                menuFacultades(facultades);
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
                cout << "Datos guardados. Hasta luego.\n";
                break;
            default:
                cout << "Opcion no disponible todavia o invalida.\n";
        }
    } while (opcionPrincipal != 0);

    return 0;
}
