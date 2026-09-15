#include "../include/entidades.h"
#include "../include/gestion.h"
#include "../include/nomina.h"
#include "../include/persistencia.h"
#include "../include/interfaz.h"
#include "../include/generador.h"
#include <iostream>
#include <iomanip>
#include <chrono>

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
void consultarEstudianteFicha(const std::vector<Estudiante>& estudiantes, const std::vector<Curso>& cursos);
void consultarProfesorFicha(const std::vector<Profesor>& profesores);
void consultarCursoFicha(const std::vector<Curso>& cursos);

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
        cout << "1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n";
        cout << "6. Generar horarios academicos\n";
        cout << "7. Consultar horario de curso\n";
        cout << "0. Volver (o presione ENTER)\n";
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
            case 6:
                menuGeneracionHorarios(cursos, RUTA_CURSOS);
                pausar();
                break;
            case 7:
                consultarCursoFicha(cursos);
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
        cout << "9. Evaluacion ERRA masiva (Parcial 1)\n";
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
            case 9:
                evaluarErraMasivo(estudiantes);
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
        cout << "6. Ver desglose individual de nomina\n";
        cout << "7. Calcular nomina universitaria masiva\n";
        cout << "0. Volver (o presione ENTER)\n";
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
            case 7:
                calcularNominaMasiva(profesores);
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

void menuGestionAvanzada(
    vector<Facultad>& facultades,
    vector<Programa>& programas,
    vector<Curso>& cursos,
    vector<Estudiante>& estudiantes,
    vector<Profesor>& profesores,
    vector<Administrativo>& administrativos
) {
    int opcion = -1;
    do {
        limpiarPantalla();
        tituloSeccion("MODULOS DE GESTION CLASICA (CRUD)");
        cout << "1. Gestionar Facultades\n";
        cout << "2. Gestionar Programas\n";
        cout << "3. Gestionar Cursos\n";
        cout << "4. Gestionar Estudiantes\n";
        cout << "5. Gestionar Profesores\n";
        cout << "6. Gestionar Administrativos\n";
        cout << "0. Volver al menu principal (o presione ENTER)\n";
        separador();
        opcion = leerOpcionInmediata("Opcion: ");

        switch (opcion) {
            case 1: menuFacultades(facultades); break;
            case 2: menuProgramas(programas, facultades); break;
            case 3: menuCursos(cursos, programas); break;
            case 4: menuEstudiantes(estudiantes, programas, cursos); break;
            case 5: menuProfesores(profesores, programas); break;
            case 6: menuAdministrativos(administrativos, facultades); break;
            case 0: break;
            default: mensajeError("Opcion invalida."); pausar();
        }
    } while (opcion != 0);
}

void mostrarEstadisticasUniversitarias(
    const vector<Facultad>& fac,
    const vector<Programa>& prog,
    const vector<Curso>& cur,
    const vector<Estudiante>& est,
    const vector<Profesor>& prof
) {
    cout << "\n------------------------------------------------------------\n";
    cout << "                 ESTADISTICAS UNIVERSIDAD                   \n";
    cout << "------------------------------------------------------------\n";
    cout << left << setw(35) << "Facultades" << right << setw(15) << fac.size() << "\n";
    cout << left << setw(35) << "Programas academicos" << right << setw(15) << prog.size() << "\n";
    cout << left << setw(35) << "Estudiantes registrados" << right << setw(15) << est.size() << "\n";
    cout << left << setw(35) << "Profesores registrados" << right << setw(15) << prof.size() << "\n";
    cout << left << setw(35) << "Cursos / Asignaturas" << right << setw(15) << cur.size() << "\n";
    cout << "------------------------------------------------------------\n";
}

void consultarEstudianteFicha(vector<Estudiante>& estudiantes) {
    if (estudiantes.empty()) {
        mensajeAlerta("No hay estudiantes cargados en el sistema.");
        pausar();
        return;
    }
    int opcion = -1;
    do {
        limpiarPantalla();
        tituloSeccion("CONSULTA DE FICHA DE ESTUDIANTE");
        cout << "1. Buscar por identificacion\n";
        cout << "2. Mostrar estudiante aleatorio\n";
        cout << "3. Mostrar estudiante en riesgo ERRA\n";
        cout << "4. Mostrar estudiante sin riesgo ERRA\n";
        cout << "5. Volver (o presione ENTER)\n";
        separador();
        opcion = leerOpcionInmediata("Opcion: ");

        if (opcion == 1) {
            string id = leerPalabra("Ingrese identificacion del estudiante (o 'cancelar' para volver): ");
            if (!esCancelar(id) && !id.empty()) {
                consultarEstudiante(estudiantes, id);
            }
            pausar();
        } else if (opcion == 2) {
            int idx = rand() % estudiantes.size();
            string idEjemplo = estudiantes[idx].identificacion;
            mensajeInfo("Mostrando ficha del estudiante aleatorio (ID: " + idEjemplo + "):");
            consultarEstudiante(estudiantes, idEjemplo);
            pausar();
        } else if (opcion == 3) {
            string idEjemplo = "";
            for (const auto& est : estudiantes) {
                if (est.activo && estaEnRiesgoEbra(est)) {
                    idEjemplo = est.identificacion;
                    break;
                }
            }
            if (!idEjemplo.empty()) {
                mensajeInfo("Mostrando ficha de estudiante en riesgo ERRA (ID: " + idEjemplo + "):");
                consultarEstudiante(estudiantes, idEjemplo);
            } else {
                mensajeAlerta("No se encontro ningun estudiante en riesgo ERRA en memoria.");
            }
            pausar();
        } else if (opcion == 4) {
            string idEjemplo = "";
            for (const auto& est : estudiantes) {
                if (est.activo && !est.matriculas.empty() && !estaEnRiesgoEbra(est)) {
                    idEjemplo = est.identificacion;
                    break;
                }
            }
            if (!idEjemplo.empty()) {
                mensajeInfo("Mostrando ficha de estudiante sin riesgo ERRA (ID: " + idEjemplo + "):");
                consultarEstudiante(estudiantes, idEjemplo);
            } else {
                mensajeAlerta("No se encontro ningun estudiante con promedio satisfactorio en memoria.");
            }
            pausar();
        } else if (opcion == 5 || opcion == 0) {
            break;
        } else {
            mensajeError("Opcion invalida.");
            pausar();
        }
    } while (opcion != 5 && opcion != 0);
}

static void mostrarFichaCursoDetallada(const Curso& c) {
    cout << "\n=======================================================\n";
    cout << "FICHA DE ASIGNATURA - " << c.codigo << "\n";
    cout << "=======================================================\n";
    cout << "Asignatura    : " << c.nombre << "\n";
    cout << "Creditos      : " << c.creditos << "\n";
    cout << "Programa      : " << c.codigoPrograma << "\n";
    cout << "Profesor      : " << c.codigoProfesor << "\n";
    cout << "Dia           : " << (c.dia.empty() ? "(Sin horario)" : c.dia) << "\n";
    if (c.horaInicio > 0) {
        cout << "Horario       : " << c.horaInicio << ":00 a " << c.horaFin << ":00\n";
    } else {
        cout << "Horario       : (Sin horario)\n";
    }
    cout << "Aula/Salon    : " << (c.salon.empty() ? "(Sin salon)" : c.salon) << "\n";
    cout << "Estado        : " << (c.activo ? "Activo" : "Inactivo") << "\n";
    cout << "=======================================================\n";
}

static void listarCursosMuestra(const vector<Curso>& cursos, size_t maxCount = 10) {
    cout << "\n--- MUESTRA REPRESENTATIVA DE CURSOS (" << min(maxCount, cursos.size()) << " Asignaturas) ---\n";
    cout << left << setw(10) << "Codigo"
         << setw(33) << "Nombre Asignatura"
         << setw(10) << "Programa"
         << setw(12) << "Profesor"
         << setw(12) << "Dia"
         << setw(15) << "Horario"
         << setw(10) << "Salon" << "\n";
    cout << string(102, '-') << "\n";

    size_t muestra = min(maxCount, cursos.size());
    for (size_t i = 0; i < muestra; ++i) {
        const auto& c = cursos[i];
        string franja = (c.horaInicio > 0) ? (to_string(c.horaInicio) + ":00-" + to_string(c.horaFin) + ":00") : "Sin horario";
        string diaStr = c.dia.empty() ? "N/A" : c.dia;
        string salStr = c.salon.empty() ? "N/A" : c.salon;
        string nomStr = (c.nombre.size() > 31) ? c.nombre.substr(0, 29) + ".." : c.nombre;

        cout << left << setw(10) << c.codigo
             << setw(33) << nomStr
             << setw(10) << c.codigoPrograma
             << setw(12) << c.codigoProfesor
             << setw(12) << diaStr
             << setw(15) << franja
             << setw(10) << salStr << "\n";
    }
}

void consultarCursoFicha(const vector<Curso>& cursos) {
    if (cursos.empty()) {
        mensajeAlerta("No hay cursos registrados en el sistema.");
        pausar();
        return;
    }
    int opcion = -1;
    do {
        limpiarPantalla();
        tituloSeccion("CONSULTA DE CURSO / HORARIOS");
        cout << "1. Buscar por codigo\n";
        cout << "2. Mostrar curso aleatorio\n";
        cout << "3. Mostrar curso con horario\n";
        cout << "4. Listar cursos de ejemplo\n";
        cout << "5. Volver (o presione ENTER)\n";
        separador();
        opcion = leerOpcionInmediata("Opcion: ");

        if (opcion == 1) {
            string codigo = leerPalabra("Ingrese codigo del curso (o 'cancelar' para volver): ");
            if (!esCancelar(codigo) && !codigo.empty()) {
                bool encontrado = false;
                for (const auto& c : cursos) {
                    if (c.codigo == codigo) {
                        mostrarFichaCursoDetallada(c);
                        encontrado = true;
                        break;
                    }
                }
                if (!encontrado) {
                    mensajeAlerta("Curso con codigo " + codigo + " no encontrado.");
                }
            }
            pausar();
        } else if (opcion == 2) {
            int idx = rand() % cursos.size();
            mensajeInfo("Mostrando ficha de curso aleatorio (Codigo: " + cursos[idx].codigo + "):");
            mostrarFichaCursoDetallada(cursos[idx]);
            pausar();
        } else if (opcion == 3) {
            const Curso* cHorario = nullptr;
            for (const auto& c : cursos) {
                if (c.activo && c.horaInicio > 0) {
                    cHorario = &c;
                    break;
                }
            }
            if (cHorario) {
                mensajeInfo("Mostrando ficha de curso con horario programado (Codigo: " + cHorario->codigo + "):");
                mostrarFichaCursoDetallada(*cHorario);
            } else {
                mensajeAlerta("No se encontro ningun curso con horario asignado en memoria.");
            }
            pausar();
        } else if (opcion == 4) {
            listarCursosMuestra(cursos, 10);
            pausar();
        } else if (opcion == 5 || opcion == 0) {
            break;
        } else {
            mensajeError("Opcion invalida.");
            pausar();
        }
    } while (opcion != 5 && opcion != 0);
}

void consultarProfesorFicha(vector<Profesor>& profesores) {
    if (profesores.empty()) {
        mensajeAlerta("No hay profesores cargados en el sistema.");
        pausar();
        return;
    }
    int opcion = -1;
    do {
        limpiarPantalla();
        tituloSeccion("CONSULTA DE FICHA Y LIQUIDACION DE PROFESOR");
        cout << "1. Buscar por identificacion\n";
        cout << "2. Mostrar profesor de planta\n";
        cout << "3. Mostrar profesor ocasional\n";
        cout << "4. Mostrar profesor catedratico\n";
        cout << "5. Mostrar profesor aleatorio\n";
        cout << "6. Volver (o presione ENTER)\n";
        separador();
        opcion = leerOpcionInmediata("Opcion: ");

        if (opcion == 1) {
            string id = leerPalabra("Ingrese identificacion del profesor (o 'cancelar' para volver): ");
            if (!esCancelar(id) && !id.empty()) {
                consultarProfesor(profesores, id);
            }
            pausar();
        } else if (opcion == 2) {
            string idEjemplo = "";
            for (const auto& prof : profesores) {
                if (prof.activo && prof.tipoVinculacion == "Planta") {
                    idEjemplo = prof.identificacion;
                    break;
                }
            }
            if (!idEjemplo.empty()) {
                mensajeInfo("Mostrando ficha de profesor de Planta (ID: " + idEjemplo + "):");
                consultarProfesor(profesores, idEjemplo);
            } else {
                mensajeAlerta("No se encontro ningun profesor de Planta en memoria.");
            }
            pausar();
        } else if (opcion == 3) {
            string idEjemplo = "";
            for (const auto& prof : profesores) {
                if (prof.activo && prof.tipoVinculacion == "Ocasional") {
                    idEjemplo = prof.identificacion;
                    break;
                }
            }
            if (!idEjemplo.empty()) {
                mensajeInfo("Mostrando ficha de profesor Ocasional (ID: " + idEjemplo + "):");
                consultarProfesor(profesores, idEjemplo);
            } else {
                mensajeAlerta("No se encontro ningun profesor Ocasional en memoria.");
            }
            pausar();
        } else if (opcion == 4) {
            string idEjemplo = "";
            for (const auto& prof : profesores) {
                if (prof.activo && prof.tipoVinculacion == "Catedratico") {
                    idEjemplo = prof.identificacion;
                    break;
                }
            }
            if (!idEjemplo.empty()) {
                mensajeInfo("Mostrando ficha de profesor Catedratico (ID: " + idEjemplo + "):");
                consultarProfesor(profesores, idEjemplo);
            } else {
                mensajeAlerta("No se encontro ningun profesor Catedratico en memoria.");
            }
            pausar();
        } else if (opcion == 5) {
            int idx = rand() % profesores.size();
            string idEjemplo = profesores[idx].identificacion;
            mensajeInfo("Mostrando ficha de profesor aleatorio (ID: " + idEjemplo + "):");
            consultarProfesor(profesores, idEjemplo);
            pausar();
        } else if (opcion == 6 || opcion == 0) {
            break;
        } else {
            mensajeError("Opcion invalida.");
            pausar();
        }
    } while (opcion != 6 && opcion != 0);
}

void ejecutarProcesoCompleto(
    vector<Facultad>& facultades,
    vector<Programa>& programas,
    vector<Curso>& cursos,
    vector<Estudiante>& estudiantes,
    vector<Profesor>& profesores,
    const string& rutaFacultades,
    const string& rutaProgramas,
    const string& rutaCursos,
    const string& rutaEstudiantes,
    const string& rutaMatriculas,
    const string& rutaProfesores
) {
    limpiarPantalla();
    encabezadoPrincipal();
    tituloSeccion("EJECUCION DEL PROCESO COMPLETO (PARCIAL 1)");
    cout << "Este proceso ejecutara de forma integrada y secuencial:\n"
         << "  1. Generacion masiva (10 Fac, 150 Prog, 9k Prof, 7.5k Cur, 225k Est)\n"
         << "  2. Estadisticas consolidadas\n"
         << "  3. Asignacion de horarios libres de conflicto\n"
         << "  4. Calculo masivo de nomina\n"
         << "  5. Evaluacion de riesgo academico (ERRA)\n"
         << "  6. Guardado y persistencia en disco\n\n";

    if (leerSiNo("Desea iniciar la ejecucion del proceso completo? (s/n): ") != 's') {
        mensajeInfo("Operacion cancelada por el usuario.");
        return;
    }

    auto t0 = chrono::high_resolution_clock::now();

    // 1. Generacion
    tituloSeccion("1. GENERACION MASIVA DE ESTRUCTURA UNIVERSITARIA");
    generarDatosMasivos(facultades, programas, profesores, cursos, estudiantes);
    mensajeExito("Generacion masiva completada con exito.");

    // 2. Estadisticas
    tituloSeccion("2. ESTADISTICAS CONSOLIDADAS");
    mostrarEstadisticasUniversitarias(facultades, programas, cursos, estudiantes, profesores);

    // 3. Horarios
    tituloSeccion("3. GENERACION DE HORARIOS ACADEMICOS");
    int asignados = generarHorariosCursos(cursos);
    mensajeExito(to_string(asignados) + " materias con horario asignado (0 conflictos).");

    // 4. Nomina
    tituloSeccion("4. CALCULO DE NOMINA UNIVERSITARIA");
    calcularNominaMasiva(profesores);

    // 5. ERRA
    tituloSeccion("5. EVALUACION DE RIESGO ACADEMICO (ERRA)");
    evaluarErraMasivo(estudiantes);

    // 6. Persistencia
    tituloSeccion("6. GUARDADO Y PERSISTENCIA");
    guardarFacultades(facultades, rutaFacultades);
    guardarProgramas(programas, rutaProgramas);
    guardarProfesores(profesores, rutaProfesores);
    guardarCursos(cursos, rutaCursos);
    guardarEstudiantes(estudiantes, rutaEstudiantes, rutaMatriculas);
    mensajeExito("Archivos en carpeta data/ actualizados correctamente.");

    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double> dur = t1 - t0;

    separador();
    cout << Colores::GREEN << Colores::BOLD
         << ">>> PROCESO COMPLETO FINALIZADO EXITOSAMENTE EN "
         << fixed << setprecision(2) << dur.count() << " SEGUNDOS <<<\n"
         << Colores::RESET;
    separador();
}

int main() {
    habilitarColoresTerminal();
    limpiarPantalla();
    encabezadoPrincipal();

    vector<Facultad> facultades;
    vector<Programa> programas;
    vector<Curso> cursos;
    vector<Estudiante> estudiantes;
    vector<Profesor> profesores;
    vector<Administrativo> administrativos;

    char respuesta = leerSiNo("\nDesea cargar los datos existentes? (s/n): ");
    if (respuesta == 's') {
        cout << "\nCargando datos desde persistencia...\n";
        facultades = cargarFacultades(RUTA_FACULTADES);
        programas = cargarProgramas(RUTA_PROGRAMAS);
        cursos = cargarCursos(RUTA_CURSOS);
        estudiantes = cargarEstudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS);
        profesores = cargarProfesores(RUTA_PROFESORES);
        administrativos = cargarAdministrativos(RUTA_ADMINISTRATIVOS);
        mensajeExito("Datos cargados correctamente: " +
                     to_string(facultades.size()) + " facultades, " +
                     to_string(programas.size()) + " programas, " +
                     to_string(cursos.size()) + " cursos, " +
                     to_string(estudiantes.size()) + " estudiantes, " +
                     to_string(profesores.size()) + " profesores.");
    } else {
        mensajeInfo("Iniciando sin datos precargados.");
    }
    pausar();

    char opcionPrincipal = ' ';
    do {
        limpiarPantalla();
        encabezadoPrincipal();
        cout << Colores::CYAN << Colores::BOLD << "===== MENU PRINCIPAL - PARCIAL 1 =====\n" << Colores::RESET;
        cout << "1. Generar universidad (10 Fac, 150 Prog, 9k Prof, 7.5k Cur, 225k Est)\n";
        cout << "2. Ver estadisticas de la universidad\n";
        cout << "3. Calcular nomina universitaria masiva\n";
        cout << "4. Generar y verificar horarios academicos\n";
        cout << "5. Analizar riesgo academico (ERRA)\n";
        cout << "6. Consultar estudiante (Ficha y promedio)\n";
        cout << "7. Consultar profesor (Ficha y liquidacion)\n";
        cout << "8. Consultar curso (Ficha y horarios)\n";
        cout << "9. Ejecutar proceso completo (Flujo integrado Parcial 1)\n";
        cout << "A. Gestion avanzada / Modulos clasicos (CRUD)\n";
        cout << "R. Recargar datos desde archivo\n";
        cout << "0. Guardar y salir (o presione ENTER)\n";
        separador();
        opcionPrincipal = leerOpcionMenu("Seleccione una opcion: ");

        switch (opcionPrincipal) {
            case '1':
                menuGeneracionMasiva(
                    facultades, programas, cursos, estudiantes, profesores,
                    RUTA_FACULTADES, RUTA_PROGRAMAS, RUTA_CURSOS,
                    RUTA_ESTUDIANTES, RUTA_MATRICULAS, RUTA_PROFESORES
                );
                pausar();
                break;
            case '2':
                mostrarEstadisticasUniversitarias(facultades, programas, cursos, estudiantes, profesores);
                pausar();
                break;
            case '3':
                calcularNominaMasiva(profesores);
                pausar();
                break;
            case '4':
                menuGeneracionHorarios(cursos, RUTA_CURSOS);
                pausar();
                break;
            case '5':
                evaluarErraMasivo(estudiantes);
                pausar();
                break;
            case '6':
                consultarEstudianteFicha(estudiantes);
                break;
            case '7':
                consultarProfesorFicha(profesores);
                break;
            case '8':
                consultarCursoFicha(cursos);
                break;
            case '9':
                ejecutarProcesoCompleto(
                    facultades, programas, cursos, estudiantes, profesores,
                    RUTA_FACULTADES, RUTA_PROGRAMAS, RUTA_CURSOS,
                    RUTA_ESTUDIANTES, RUTA_MATRICULAS, RUTA_PROFESORES
                );
                pausar();
                break;
            case 'a':
                menuGestionAvanzada(facultades, programas, cursos, estudiantes, profesores, administrativos);
                break;
            case 'r':
                if (leerSiNo("Se perdera lo que no haya guardado. Continuar? (s/n): ") == 's') {
                    cout << "\nRecargando datos desde disco...\n";
                    facultades = cargarFacultades(RUTA_FACULTADES);
                    programas = cargarProgramas(RUTA_PROGRAMAS);
                    cursos = cargarCursos(RUTA_CURSOS);
                    estudiantes = cargarEstudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS);
                    profesores = cargarProfesores(RUTA_PROFESORES);
                    administrativos = cargarAdministrativos(RUTA_ADMINISTRATIVOS);
                    mensajeExito("Datos recargados desde archivo: " +
                                 to_string(facultades.size()) + " facultades, " +
                                 to_string(programas.size()) + " programas, " +
                                 to_string(cursos.size()) + " cursos, " +
                                 to_string(estudiantes.size()) + " estudiantes, " +
                                 to_string(profesores.size()) + " profesores.");
                } else {
                    mensajeInfo("Operacion cancelada.");
                }
                pausar();
                break;
            case '0':
                cout << "\nGuardando datos en disco...\n";
                guardarFacultades(facultades, RUTA_FACULTADES);
                guardarProgramas(programas, RUTA_PROGRAMAS);
                guardarCursos(cursos, RUTA_CURSOS);
                guardarEstudiantes(estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS);
                guardarProfesores(profesores, RUTA_PROFESORES);
                guardarAdministrativos(administrativos, RUTA_ADMINISTRATIVOS);
                mensajeExito("Todos los datos fueron guardados exitosamente. Hasta luego.");
                break;
            default:
                mensajeError("Opcion no disponible o invalida.");
                pausar();
        }
    } while (opcionPrincipal != '0');

    return 0;
}
