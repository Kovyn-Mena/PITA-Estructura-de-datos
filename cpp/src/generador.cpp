#include "../include/generador.h"
#include "../include/gestion.h"
#include "../include/persistencia.h"
#include "../include/interfaz.h"
#include <iostream>
#include <chrono>
#include <random>
#include <iomanip>
#include <sstream>
#include <unordered_map>
#include <algorithm>

using namespace std;

namespace {

const vector<string> NOMBRES = {
    "Carlos", "Juan", "Maria", "Laura", "Andres", "Valentina", "Diego", "Ana", "Luis", "Sofia",
    "Jorge", "Camila", "Mateo", "Mariana", "Gabriel", "Isabella", "Felipe", "Daniela", "Alejandro", "Paula",
    "David", "Natalia", "Sebastian", "Lucia", "Julian", "Catalina", "Camilo", "Andrea", "Esteban", "Carolina",
    "Santiago", "Sara", "Manuel", "Gabriela", "Ricardo", "Vanessa", "Fernando", "Diana", "Oscar", "Adriana"
};

const vector<string> APELLIDOS = {
    "Perez", "Rodriguez", "Gomez", "Fernandez", "Sanchez", "Torres", "Castro", "Diaz", "Vargas", "Martinez",
    "Rojas", "Morales", "Ortiz", "Gutierrez", "Navarro", "Alvarez", "Mendoza", "Castillo", "Jimenez", "Vasquez",
    "Romero", "Herrera", "Medina", "Aguilar", "Pena", "Silva", "Suarez", "Cabrera", "Rios", "Reyes",
    "Salazar", "Delgado", "Guerrero", "Cortes", "Cardona", "Mejia", "Bautista", "Valencia", "Ochoa", "Velez"
};

const vector<string> PREFIJOS_CURSO = {
    "Fundamentos de", "Introduccion a", "Metodos de", "Sistemas de", "Analisis de",
    "Diseno de", "Taller de", "Seminario de", "Laboratorio de", "Teoria de",
    "Practica de", "Modelos de", "Optimizacion de", "Evaluacion de", "Tecnologia de",
    "Estructura de", "Principios de", "Desarrollo de", "Investigacion en", "Gestion de"
};

const vector<string> SUFIJOS_ROMANOS = {
    "I", "II", "III", "IV", "V", "Avanzado", "Aplicado", "Integral"
};

struct FacultadDef {
    string codigo;
    string nombre;
    string decano;
};

struct ProgramaPlantilla {
    string nombre;
    string nivel;
};

const vector<FacultadDef> FACULTADES_DEF = {
    {"FING", "Facultad de Ingenierias y Tecnologias", "Armando Luis Cotes de Armas"},
    {"FACE", "Facultad de Ciencias Administrativas Contables y Economicas", "Carmen Alicia Perez"},
    {"FCS", "Facultad de Ciencias de la Salud", "Roberto Gomez Fernandez"},
    {"FDCP", "Facultad de Derecho Ciencias Politicas y Sociales", "Alvaro Enrique Rodriguez"},
    {"FBA", "Facultad de Bellas Artes", "Marta Cecilia Gutierrez"},
    {"FED", "Facultad de Educacion", "Luis Eduardo Martinez"},
    {"FCB", "Facultad de Ciencias Basicas", "Gloria Ines Mendoza"},
    {"FAGRO", "Facultad de Ciencias Agropecuarias y Ambientales", "Carlos Alberto Morales"},
    {"FHUM", "Facultad de Humanidades y Ciencias Sociales", "Patricia Elena Castillo"},
    {"FMED", "Facultad de Medicina", "Hernando Jose Alvarez"}
};

// 15 programas por cada una de las 10 facultades (total: 150)
const vector<vector<ProgramaPlantilla>> PROGRAMAS_POR_FACULTAD = {
    // 0: FING
    {
        {"Ingenieria de Sistemas", "Pregrado"},
        {"Ingenieria Electronica", "Pregrado"},
        {"Ingenieria Ambiental y Sanitaria", "Pregrado"},
        {"Ingenieria Agroindustrial", "Pregrado"},
        {"Ingenieria Civil", "Pregrado"},
        {"Ingenieria Mecanica", "Pregrado"},
        {"Ingenieria Industrial", "Pregrado"},
        {"Ingenieria Quimica", "Pregrado"},
        {"Ingenieria Biomedica", "Pregrado"},
        {"Ingenieria de Telecomunicaciones", "Pregrado"},
        {"Ingenieria de Alimentos", "Pregrado"},
        {"Ingenieria Mecatronica", "Pregrado"},
        {"Tecnologia en Desarrollo de Software", "Tecnologico"},
        {"Tecnologia en Redes y Seguridad", "Tecnologico"},
        {"Tecnologia en Automatizacion Industrial", "Tecnologico"}
    },
    // 1: FACE
    {
        {"Administracion de Empresas", "Pregrado"},
        {"Administracion de Empresas Turisticas y Hoteleras", "Pregrado"},
        {"Comercio Internacional", "Pregrado"},
        {"Contaduria Publica", "Pregrado"},
        {"Economia", "Pregrado"},
        {"Finanzas y Negocios Internacionales", "Pregrado"},
        {"Mercadeo y Publicidad", "Pregrado"},
        {"Gestion del Talento Humano", "Pregrado"},
        {"Logistica y Distribucion Internacional", "Pregrado"},
        {"Administracion Financiera", "Pregrado"},
        {"Tecnologia en Gestion Bancaria", "Tecnologico"},
        {"Tecnologia en Gestion Logistica", "Tecnologico"},
        {"Especializacion en Finanzas", "Especializacion"},
        {"Especializacion en Gerencia Tributaria", "Especializacion"},
        {"Maestria en Administracion", "Maestria"}
    },
    // 2: FCS
    {
        {"Enfermeria", "Pregrado"},
        {"Instrumentacion Quirurgica", "Pregrado"},
        {"Fisioterapia", "Pregrado"},
        {"Fonoaudiologia", "Pregrado"},
        {"Terapia Ocupacional", "Pregrado"},
        {"Nutricion y Dietetica", "Pregrado"},
        {"Odontologia", "Pregrado"},
        {"Optometria", "Pregrado"},
        {"Psicologia Clinica", "Pregrado"},
        {"Salud Ocupacional y Seguridad", "Pregrado"},
        {"Tecnologia en Atencion Prehospitalaria", "Tecnologico"},
        {"Tecnologia en Citohistologia", "Tecnologico"},
        {"Especializacion en Epidemiologia", "Especializacion"},
        {"Especializacion en Auditoria en Salud", "Especializacion"},
        {"Maestria en Salud Publica", "Maestria"}
    },
    // 3: FDCP
    {
        {"Derecho", "Pregrado"},
        {"Psicologia", "Pregrado"},
        {"Sociologia", "Pregrado"},
        {"Ciencia Politica", "Pregrado"},
        {"Trabajo Social", "Pregrado"},
        {"Relaciones Internacionales", "Pregrado"},
        {"Antropologia", "Pregrado"},
        {"Criminalistica y Ciencias Forenses", "Pregrado"},
        {"Comunicacion Social y Periodismo", "Pregrado"},
        {"Filosofia Juridica", "Pregrado"},
        {"Especializacion en Derecho Penal", "Especializacion"},
        {"Especializacion en Derecho Administrativo", "Especializacion"},
        {"Especializacion en Derecho Constitucional", "Especializacion"},
        {"Especializacion en Derecho Laboral", "Especializacion"},
        {"Maestria en Conflicto y Paz", "Maestria"}
    },
    // 4: FBA
    {
        {"Licenciatura en Artes", "Pregrado"},
        {"Musica", "Pregrado"},
        {"Arte Dramatico", "Pregrado"},
        {"Diseno Grafico", "Pregrado"},
        {"Danza Tradicional y Contemporanea", "Pregrado"},
        {"Artes Plasticas y Visuales", "Pregrado"},
        {"Cinematografia y Medios Audiovisuales", "Pregrado"},
        {"Diseno de Modas", "Pregrado"},
        {"Produccion Musical", "Pregrado"},
        {"Gestion Cultural", "Pregrado"},
        {"Diseno Industrial", "Pregrado"},
        {"Especializacion en Pedagogia del Arte", "Especializacion"},
        {"Especializacion en Creacion Sonora", "Especializacion"},
        {"Maestria en Artes Visuales", "Maestria"},
        {"Maestria en Etnomusicologia", "Maestria"}
    },
    // 5: FED
    {
        {"Licenciatura en Matematicas", "Pregrado"},
        {"Licenciatura en Espanol e Ingles", "Pregrado"},
        {"Licenciatura en Literatura y Lengua Castellana", "Pregrado"},
        {"Licenciatura en Educacion Fisica Recreacion y Deportes", "Pregrado"},
        {"Licenciatura en Ciencias Naturales y Educacion Ambiental", "Pregrado"},
        {"Licenciatura en Educacion Infantil", "Pregrado"},
        {"Licenciatura en Ciencias Sociales", "Pregrado"},
        {"Licenciatura en Lenguas Extranjeras", "Pregrado"},
        {"Licenciatura en Informatica Educativa", "Pregrado"},
        {"Licenciatura en Pedagogia Infantil", "Pregrado"},
        {"Especializacion en Docencia Universitaria", "Especializacion"},
        {"Especializacion en Gestion Curricular", "Especializacion"},
        {"Especializacion en Orientacion Escolar", "Especializacion"},
        {"Maestria en Educacion", "Maestria"},
        {"Maestria en Neuroeducacion", "Maestria"}
    },
    // 6: FCB
    {
        {"Microbiologia", "Pregrado"},
        {"Biologia", "Pregrado"},
        {"Quimica", "Pregrado"},
        {"Fisica", "Pregrado"},
        {"Matematicas Puras", "Pregrado"},
        {"Estadistica Aplicada", "Pregrado"},
        {"Geologia", "Pregrado"},
        {"Ciencias Ambientales", "Pregrado"},
        {"Bioquimica", "Pregrado"},
        {"Biotecnologia", "Pregrado"},
        {"Quimica Farmaceutica", "Pregrado"},
        {"Especializacion en Analisis Quimico", "Especializacion"},
        {"Especializacion en Biologia Molecular", "Especializacion"},
        {"Maestria en Ciencias Fisicas", "Maestria"},
        {"Maestria en Biologia Aplicada", "Maestria"}
    },
    // 7: FAGRO
    {
        {"Agronomia", "Pregrado"},
        {"Medicina Veterinaria y Zootecnia", "Pregrado"},
        {"Ingenieria Agricola", "Pregrado"},
        {"Ingenieria Forestal", "Pregrado"},
        {"Zootecnia", "Pregrado"},
        {"Administracion de Empresas Agropecuarias", "Pregrado"},
        {"Agroecologia y Desarrollo Rural", "Pregrado"},
        {"Tecnologia en Produccion Agricola", "Tecnologico"},
        {"Tecnologia en Produccion Pecuaria", "Tecnologico"},
        {"Tecnologia en Riego y Drenaje", "Tecnologico"},
        {"Especializacion en Bienestar Animal", "Especializacion"},
        {"Especializacion en Gestion Ambiental Agropecuaria", "Especializacion"},
        {"Especializacion en Biotecnologia Vegetal", "Especializacion"},
        {"Maestria en Produccion Animal Tropical", "Maestria"},
        {"Maestria en Sanidad Vegetal", "Maestria"}
    },
    // 8: FHUM
    {
        {"Historia", "Pregrado"},
        {"Filosofia", "Pregrado"},
        {"Geografia", "Pregrado"},
        {"Linguistica", "Pregrado"},
        {"Literatura", "Pregrado"},
        {"Lenguas Modernas", "Pregrado"},
        {"Teologia y Estudios Religiosos", "Pregrado"},
        {"Estudios Culturales", "Pregrado"},
        {"Humanidades Digitales", "Pregrado"},
        {"Archivistica y Gestion Documental", "Pregrado"},
        {"Especializacion en Estudios Regionales", "Especializacion"},
        {"Especializacion en Didactica de la Historia", "Especializacion"},
        {"Especializacion en Semiotica", "Especializacion"},
        {"Maestria en Filosofia Contemporanea", "Maestria"},
        {"Maestria en Literatura Latinoamericana", "Maestria"}
    },
    // 9: FMED
    {
        {"Medicina General", "Pregrado"},
        {"Morfologia Humana", "Pregrado"},
        {"Fisiologia Medica", "Pregrado"},
        {"Farmacologia Clinica", "Pregrado"},
        {"Cirugia General", "Pregrado"},
        {"Pediatria", "Pregrado"},
        {"Ginecologia y Obstetricia", "Pregrado"},
        {"Medicina Interna", "Pregrado"},
        {"Anestesiologia", "Pregrado"},
        {"Patologia Forense y Clinica", "Pregrado"},
        {"Psiquiatria", "Pregrado"},
        {"Dermatologia", "Pregrado"},
        {"Especializacion en Gerencia Hospitalaria", "Especializacion"},
        {"Especializacion en Radiologia e Imagenes", "Especializacion"},
        {"Maestria en Ciencias Medicas", "Maestria"}
    }
};

string formatearCodigo(const string& prefijo, int numero, int ancho) {
    ostringstream oss;
    oss << prefijo << setfill('0') << setw(ancho) << numero;
    return oss.str();
}

const vector<string> DIAS_SEMANA = {
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"
};

struct FranjaHoraria {
    int inicio;
    int fin;
};

const vector<FranjaHoraria> FRANJAS_HORARIAS = {
    {6, 8},
    {8, 10},
    {10, 12},
    {14, 16},
    {16, 18},
    {18, 20},
    {20, 22}
};

vector<string> inicializarSalones() {
    vector<string> salones;
    salones.reserve(400);
    const string edificios = "ABCDEFGHIJ";
    for (char ed : edificios) {
        for (int piso = 1; piso <= 4; ++piso) {
            for (int num = 1; num <= 10; ++num) {
                ostringstream oss;
                oss << ed << "-" << piso << setfill('0') << setw(2) << num;
                salones.push_back(oss.str());
            }
        }
    }
    return salones;
}

} // namespace

void generarDatosMasivos(
    vector<Facultad>& facultades,
    vector<Programa>& programas,
    vector<Profesor>& profesores,
    vector<Curso>& cursos,
    vector<Estudiante>& estudiantes
) {
    // Generador aleatorio reproducible y rapido
    mt19937 rng(123456);
    uniform_int_distribution<size_t> distNombres(0, NOMBRES.size() - 1);
    uniform_int_distribution<size_t> distApellidos(0, APELLIDOS.size() - 1);
    uniform_int_distribution<size_t> distPrefijosCurso(0, PREFIJOS_CURSO.size() - 1);
    uniform_int_distribution<size_t> distSufijosCurso(0, SUFIJOS_ROMANOS.size() - 1);
    uniform_int_distribution<int> distCreditos(2, 4);
    uniform_int_distribution<int> distPorcentaje(1, 100);

    const vector<string> categorias = {"Auxiliar", "Asistente", "Asociado", "Titular"};
    const vector<string> posgrados = {"Ninguno", "Especializacion", "Maestria", "Doctorado"};
    const vector<int> horasCatedraOpciones = {4, 8, 12, 16};

    // 1. Limpiar y reservar memoria para maximo rendimiento
    facultades.clear();
    programas.clear();
    profesores.clear();
    cursos.clear();
    estudiantes.clear();

    facultades.reserve(10);
    programas.reserve(150);
    profesores.reserve(9000);
    cursos.reserve(7500);
    estudiantes.reserve(225000);

    cout << "  [1/5] Generando 10 facultades...\n";
    for (const auto& fdef : FACULTADES_DEF) {
        Facultad f;
        f.codigo = fdef.codigo;
        f.nombre = fdef.nombre;
        f.decano = fdef.decano;
        f.activo = true;
        facultades.push_back(f);
    }

    cout << "  [2/5] Generando 150 programas academicos (15 por facultad)...\n";
    int codProgramaNum = 1;
    for (size_t fIdx = 0; fIdx < FACULTADES_DEF.size(); ++fIdx) {
        const string& codFacultad = FACULTADES_DEF[fIdx].codigo;
        const auto& listaProgramas = PROGRAMAS_POR_FACULTAD[fIdx];
        for (const auto& pPlantilla : listaProgramas) {
            Programa p;
            p.codigo = formatearCodigo("PRG", codProgramaNum++, 3);
            p.nombre = pPlantilla.nombre;
            p.nivel = pPlantilla.nivel;
            p.codigoFacultad = codFacultad;
            p.activo = true;
            programas.push_back(p);
        }
    }

    cout << "  [3/5] Generando 9.000 profesores (60 por programa)...\n";
    int codProfesorNum = 70000001;
    // Guardamos los codigos de profesores por programa para asignarlos coherentemente a materias
    vector<vector<string>> profesoresPorPrograma(programas.size());

    for (size_t pIdx = 0; pIdx < programas.size(); ++pIdx) {
        const string& codProg = programas[pIdx].codigo;
        profesoresPorPrograma[pIdx].reserve(60);

        for (int i = 0; i < 60; ++i) {
            Profesor prof;
            prof.identificacion = to_string(codProfesorNum++);
            prof.nombreCompleto = NOMBRES[distNombres(rng)] + " " +
                                  APELLIDOS[distApellidos(rng)] + " " +
                                  APELLIDOS[distApellidos(rng)];
            prof.codigoPrograma = codProg;
            prof.activo = (distPorcentaje(rng) <= 95);

            int tipoRand = distPorcentaje(rng);
            if (tipoRand <= 30) {
                // Planta (30%)
                prof.tipoVinculacion = "Planta";
                prof.dedicacion = (distPorcentaje(rng) <= 70) ? "TiempoCompleto" : "MedioTiempo";
                prof.categoriaEscalafon = categorias[rng() % categorias.size()];
                prof.horasCatedraSemanales = 0;
                prof.adHonorem = false;
                prof.aniosExperiencia = 1 + (rng() % 25);
                prof.puntosTitulos = 20 + (rng() % 131);     // 20 a 150
                prof.puntosProductividad = rng() % 61;        // 0 a 60
                prof.posgrado = posgrados[rng() % posgrados.size()];
            } else if (tipoRand <= 70) {
                // Ocasional (40%)
                prof.tipoVinculacion = "Ocasional";
                prof.dedicacion = (distPorcentaje(rng) <= 70) ? "TiempoCompleto" : "MedioTiempo";
                prof.categoriaEscalafon = categorias[rng() % categorias.size()];
                prof.horasCatedraSemanales = 0;
                prof.adHonorem = false;
                prof.aniosExperiencia = 1 + (rng() % 15);
                prof.puntosTitulos = 0;
                prof.puntosProductividad = 0;
                prof.posgrado = posgrados[rng() % posgrados.size()];
            } else {
                // Catedratico (30%)
                prof.tipoVinculacion = "Catedratico";
                prof.dedicacion = "HorasCatedra";
                prof.categoriaEscalafon = "";
                prof.horasCatedraSemanales = horasCatedraOpciones[rng() % horasCatedraOpciones.size()];
                prof.adHonorem = (distPorcentaje(rng) <= 2);
                prof.aniosExperiencia = 1 + (rng() % 15);
                prof.puntosTitulos = 0;
                prof.puntosProductividad = 0;
                prof.posgrado = "";
            }

            profesoresPorPrograma[pIdx].push_back(prof.identificacion);
            profesores.push_back(prof);
        }
    }

    cout << "  [4/5] Generando 7.500 materias (50 por programa con profesor asignado)...\n";
    int codCursoNum = 1;
    vector<vector<string>> cursosPorPrograma(programas.size());

    for (size_t pIdx = 0; pIdx < programas.size(); ++pIdx) {
        const string& codProg = programas[pIdx].codigo;
        const string& nomProg = programas[pIdx].nombre;
        const auto& listaProfs = profesoresPorPrograma[pIdx];
        cursosPorPrograma[pIdx].reserve(50);

        for (int c = 0; c < 50; ++c) {
            Curso cur;
            cur.codigo = formatearCodigo("CUR", codCursoNum++, 5);
            string pref = PREFIJOS_CURSO[distPrefijosCurso(rng)];
            string suf = SUFIJOS_ROMANOS[c % SUFIJOS_ROMANOS.size()];
            cur.nombre = pref + " " + nomProg + " " + suf;
            cur.creditos = distCreditos(rng);
            // Se asigna aleatoriamente a uno de los 60 profesores del mismo programa
            cur.codigoProfesor = listaProfs[rng() % listaProfs.size()];
            cur.codigoPrograma = codProg;
            cur.activo = (distPorcentaje(rng) <= 95);

            cursosPorPrograma[pIdx].push_back(cur.codigo);
            cursos.push_back(cur);
        }
    }

    cout << "  [4.1] Generando horarios academicos libres de conflicto para 7.500 materias...\n";
    generarHorariosCursos(cursos);

    cout << "  [5/5] Generando 225.000 estudiantes (1.500 por programa) con matriculas y calificaciones...\n";
    long long codEstudianteNum = 1000000001LL;
    uniform_real_distribution<float> distBaseErra(1.8f, 3.20f);
    uniform_real_distribution<float> distBaseNormal(3.30f, 4.80f);
    uniform_real_distribution<float> distVar(-0.35f, 0.35f);

    for (size_t pIdx = 0; pIdx < programas.size(); ++pIdx) {
        const string& codProg = programas[pIdx].codigo;
        const auto& cursosProg = cursosPorPrograma[pIdx];

        for (int eIdx = 0; eIdx < 1500; ++eIdx) {
            Estudiante est;
            est.identificacion = to_string(codEstudianteNum++);
            est.nombreCompleto = NOMBRES[distNombres(rng)] + " " +
                                 APELLIDOS[distApellidos(rng)] + " " +
                                 APELLIDOS[distApellidos(rng)];
            est.codigoPrograma = codProg;

            int estRand = distPorcentaje(rng);
            if (estRand <= 90) {
                est.estado = "Activo";
                est.activo = true;
            } else if (estRand <= 95) {
                est.estado = "Graduado";
                est.activo = true;
            } else {
                est.estado = "Inactivo";
                est.activo = false;
            }

            // Asignacion de matriculas y calificaciones (ERRA: promedio < 3.25)
            // ~95% de estudiantes tienen 3-4 materias con notas
            // ~5% sin materias (recien matriculados / inactivos sin registro)
            if (estRand <= 95 && !cursosProg.empty()) {
                int riesgoRand = distPorcentaje(rng);
                float basePromedio = (riesgoRand <= 22) ? distBaseErra(rng) : distBaseNormal(rng);
                int numCursos = 3 + (rng() % 2); // 3 o 4 materias

                int startOffset = rng() % cursosProg.size();
                est.matriculas.reserve(numCursos);
                for (int k = 0; k < numCursos; ++k) {
                    Matricula m;
                    m.codigoCurso = cursosProg[(startOffset + k) % cursosProg.size()];
                    float nota = basePromedio + distVar(rng);
                    if (nota < 1.0f) nota = 1.0f;
                    if (nota > 5.0f) nota = 5.0f;
                    m.nota = std::round(nota * 10.0f) / 10.0f;
                    est.matriculas.push_back(m);
                }
            }

            estudiantes.push_back(move(est));
        }
    }
}

void menuGeneracionMasiva(
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
    cout << "\n===========================================================\n";
    cout << " GENERACION MASIVA DE DATOS ALEATORIOS (PARCIAL 1)\n";
    cout << "===========================================================\n";
    cout << "Estructura requerida:\n";
    cout << " - 10 Facultades\n";
    cout << " - 150 Programas academicos (15 por facultad)\n";
    cout << " - 9.000 Profesores (60 por programa)\n";
    cout << " - 7.500 Materias / Cursos (50 por programa)\n";
    cout << " - 225.000 Estudiantes (1.500 por programa)\n\n";
    cout << "ATENCION: Esta operacion reemplazara los datos actuales en\n";
    cout << "memoria y sobrescribira los archivos de persistencia en disco.\n";

    char respuesta = leerSiNo("\nEsta seguro de generar los datos masivos? (s/n): ");
    if (respuesta != 's') {
        cout << "\nOperacion cancelada. Los datos existentes no sufrieron cambios.\n";
        return;
    }

    cout << "\nIniciando generacion masiva...\n";
    auto inicio = chrono::high_resolution_clock::now();

    generarDatosMasivos(facultades, programas, profesores, cursos, estudiantes);

    cout << "\nGuardando datos en disco (formato delimitado por '|')...\n";
    guardarFacultades(facultades, rutaFacultades);
    guardarProgramas(programas, rutaProgramas);
    guardarProfesores(profesores, rutaProfesores);
    guardarCursos(cursos, rutaCursos);
    guardarEstudiantes(estudiantes, rutaEstudiantes, rutaMatriculas);

    auto fin = chrono::high_resolution_clock::now();
    chrono::duration<double> duracion = fin - inicio;

    cout << "\n===========================================================\n";
    cout << " GENERACION Y PERSISTENCIA COMPLETADA CON EXITO\n";
    cout << "===========================================================\n";
    cout << "Tiempo total: " << fixed << setprecision(2) << duracion.count() << " segundos.\n";
    cout << "Resumen de registros generados:\n";
    cout << " - Facultades:  " << facultades.size() << "\n";
    cout << " - Programas:   " << programas.size() << "\n";
    cout << " - Profesores:  " << profesores.size() << "\n";
    cout << " - Cursos:      " << cursos.size() << "\n";
    cout << " - Estudiantes: " << estudiantes.size() << "\n";
    cout << "Archivos actualizados correctamente en carpeta data/.\n";
}

int generarHorariosCursos(vector<Curso>& cursos) {
    static const auto SALONES = inicializarSalones();
    const size_t numSalones = SALONES.size();
    const size_t numFranjas = FRANJAS_HORARIAS.size();
    const size_t numSlots = DIAS_SEMANA.size() * numFranjas; // 42 slots

    unordered_map<string, uint64_t> ocupacionProfesor;
    unordered_map<string, uint64_t> ocupacionSalon;
    ocupacionProfesor.reserve(cursos.size() * 2);
    ocupacionSalon.reserve(numSalones * 2);

    mt19937 rng(987654);
    uniform_int_distribution<size_t> distSlot(0, numSlots - 1);
    uniform_int_distribution<size_t> distSalon(0, numSalones - 1);

    int asignados = 0;

    for (auto& c : cursos) {
        const string& profId = c.codigoProfesor;
        size_t startSlot = distSlot(rng);
        size_t startSalon = distSalon(rng);
        bool asignado = false;

        for (size_t sStep = 0; sStep < numSlots; ++sStep) {
            size_t slot = (startSlot + sStep) % numSlots;
            uint64_t mask = (1ULL << slot);

            if (!profId.empty() && (ocupacionProfesor[profId] & mask)) {
                continue; // Conflicto: profesor ocupado en este slot
            }

            for (size_t rStep = 0; rStep < numSalones; ++rStep) {
                size_t salIdx = (startSalon + rStep) % numSalones;
                const string& sal = SALONES[salIdx];

                if (!(ocupacionSalon[sal] & mask)) {
                    // Libre para profesor y aula
                    if (!profId.empty()) {
                        ocupacionProfesor[profId] |= mask;
                    }
                    ocupacionSalon[sal] |= mask;

                    size_t dIdx = slot / numFranjas;
                    size_t fIdx = slot % numFranjas;

                    c.dia = DIAS_SEMANA[dIdx];
                    c.horaInicio = FRANJAS_HORARIAS[fIdx].inicio;
                    c.horaFin = FRANJAS_HORARIAS[fIdx].fin;
                    c.salon = sal;

                    asignado = true;
                    asignados++;
                    break;
                }
            }
            if (asignado) break;
        }
    }
    return asignados;
}

void menuGeneracionHorarios(vector<Curso>& cursos, const string& rutaCursos) {
    cout << "\n===========================================================\n";
    cout << "      GENERACION AUTOMATICA DE HORARIOS ACADEMICOS         \n";
    cout << "===========================================================\n";
    cout << "Total de materias a programar: " << cursos.size() << "\n";
    cout << "Parametros de franjas y aulas:\n";
    cout << " - Dias: Lunes a Sabado (6 dias)\n";
    cout << " - Franjas horarias: 06:00 a 22:00 (bloques de 2 horas)\n";
    cout << " - Salones disponibles: 400 aulas (Edificios A al J)\n";
    cout << " - Control de conflictos: 0 colisiones en profesor o aula\n";

    char resp = leerSiNo("\nDesea generar y guardar los horarios de las materias? (s/n): ");
    if (resp != 's') {
        cout << "Operacion cancelada. No se modificaron los horarios.\n";
        return;
    }

    cout << "\nGenerando horarios academicos libres de conflicto...\n";
    auto t0 = chrono::high_resolution_clock::now();
    int asignados = generarHorariosCursos(cursos);
    guardarCursos(cursos, rutaCursos);
    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double> dur = t1 - t0;

    cout << "\n===========================================================\n";
    cout << "      HORARIOS GENERADOS Y GUARDADOS CON EXITO             \n";
    cout << "===========================================================\n";
    cout << "Materias procesadas:           " << cursos.size() << "\n";
    cout << "Materias con horario asignado: " << asignados << "\n";
    cout << "Conflictos profesor / franja : 0\n";
    cout << "Conflictos salon / franja    : 0\n";
    cout << "Tiempo de ejecucion:           " << fixed << setprecision(3) << dur.count() << " segundos.\n";
    cout << "Archivo de datos actualizado:  " << rutaCursos << "\n";

    // Muestra automatica de 4 ejemplos de cursos con horario
    cout << "\n--- EJEMPLOS DE ASIGNATURAS CON HORARIO ASIGNADO ---\n";
    cout << left << setw(10) << "Codigo"
         << setw(33) << "Nombre Asignatura"
         << setw(10) << "Programa"
         << setw(12) << "Profesor"
         << setw(12) << "Dia"
         << setw(15) << "Horario"
         << setw(10) << "Salon" << "\n";
    cout << string(102, '-') << "\n";

    size_t mostrados = 0;
    for (const auto& c : cursos) {
        if (c.horaInicio > 0) {
            string franja = to_string(c.horaInicio) + ":00-" + to_string(c.horaFin) + ":00";
            string nomStr = (c.nombre.size() > 31) ? c.nombre.substr(0, 29) + ".." : c.nombre;
            cout << left << setw(10) << c.codigo
                 << setw(33) << nomStr
                 << setw(10) << c.codigoPrograma
                 << setw(12) << c.codigoProfesor
                 << setw(12) << c.dia
                 << setw(15) << franja
                 << setw(10) << c.salon << "\n";
            if (++mostrados >= 4) break;
        }
    }
}

void consultarHorarioCurso(const vector<Curso>& cursos) {
    if (cursos.empty()) {
        cout << "\nNo hay cursos registrados.\n";
        return;
    }
    cout << "\n--- CONSULTA DE HORARIOS DE ASIGNATURAS ---\n";
    string codigo = leerPalabra("Ingrese codigo del curso (ej: CUR00001) o 'muestra' para ver 10: ");

    if (codigo == "muestra" || codigo.empty()) {
        cout << "\n--- MUESTRA REPRESENTATIVA DE HORARIOS (10 Asignaturas) ---\n";
        cout << left << setw(10) << "Codigo"
             << setw(35) << "Nombre Asignatura"
             << setw(12) << "Dia"
             << setw(14) << "Franja"
             << setw(10) << "Salon"
             << setw(12) << "Profesor"
             << setw(10) << "Programa" << "\n";
        cout << string(103, '-') << "\n";

        size_t muestra = min(size_t(10), cursos.size());
        for (size_t i = 0; i < muestra; ++i) {
            const auto& c = cursos[i];
            string franja = (c.horaInicio > 0) ? (to_string(c.horaInicio) + ":00 - " + to_string(c.horaFin) + ":00") : "Sin horario";
            string diaStr = c.dia.empty() ? "N/A" : c.dia;
            string salStr = c.salon.empty() ? "N/A" : c.salon;

            cout << left << setw(10) << c.codigo
                 << setw(35) << (c.nombre.size() > 33 ? c.nombre.substr(0, 31) + ".." : c.nombre)
                 << setw(12) << diaStr
                 << setw(14) << franja
                 << setw(10) << salStr
                 << setw(12) << c.codigoProfesor
                 << setw(10) << c.codigoPrograma << "\n";
        }
        return;
    }

    bool encontrado = false;
    for (const auto& c : cursos) {
        if (c.codigo == codigo) {
            encontrado = true;
            cout << "\n=======================================================\n";
            cout << "FICHA DE HORARIO - " << c.codigo << "\n";
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
            break;
        }
    }
    if (!encontrado) {
        cout << "Curso con codigo " << codigo << " no encontrado.\n";
    }
}

void evaluarErraMasivo(const vector<Estudiante>& estudiantes) {
    if (estudiantes.empty()) {
        cout << "\nNo hay estudiantes registrados en el sistema para evaluar.\n";
        return;
    }

    cout << "\n===========================================================\n";
    cout << "     EVALUACION MASIVA DE RENDIMIENTO ACADEMICO (ERRA)     \n";
    cout << "===========================================================\n";
    cout << "Criterio institucional : Promedio acumulado < 3.25\n";
    cout << "Regla de proteccion    : Estudiantes sin notas no generan alerta\n";
    cout << "Total de estudiantes   : " << estudiantes.size() << "\n";
    cout << "-----------------------------------------------------------\n";
    cout << "Evaluando desempeno academico institucional...\n";

    auto t0 = chrono::high_resolution_clock::now();

    size_t total = estudiantes.size();
    size_t conNotas = 0;
    size_t sinNotas = 0;
    size_t enErra = 0;
    size_t sinRiesgo = 0;
    double sumaPromedios = 0.0;

    for (const auto& e : estudiantes) {
        if (e.matriculas.empty()) {
            sinNotas++;
        } else {
            conNotas++;
            float prom = calcularPromedio(e);
            sumaPromedios += prom;
            if (estaEnRiesgoEbra(e)) {
                enErra++;
            } else {
                sinRiesgo++;
            }
        }
    }

    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double> dur = t1 - t0;

    double promGlobal = conNotas > 0 ? (sumaPromedios / conNotas) : 0.0;
    double pctErraTotal = (enErra * 100.0) / total;
    double pctErraConNotas = conNotas > 0 ? (enErra * 100.0) / conNotas : 0.0;
    double pctSinRiesgo = conNotas > 0 ? (sinRiesgo * 100.0) / conNotas : 0.0;
    double pctSinNotas = (sinNotas * 100.0) / total;

    cout << "\n===========================================================\n";
    cout << "          RESUMEN CONSOLIDADO DE ALERTA ERRA               \n";
    cout << "===========================================================\n";
    cout << left << setw(35) << "Total estudiantes en base:" << right << setw(10) << total << "\n";
    cout << left << setw(35) << "Estudiantes con asignaturas/notas:" << right << setw(10) << conNotas
         << " (" << fixed << setprecision(1) << (conNotas * 100.0 / total) << "%)\n";
    cout << left << setw(35) << "Estudiantes sin notas (sin alerta):" << right << setw(10) << sinNotas
         << " (" << fixed << setprecision(1) << pctSinNotas << "%)\n";
    cout << string(59, '-') << "\n";
    cout << left << setw(35) << "EN RIESGO ERRA (Promedio < 3.25):" << right << setw(10) << enErra
         << " (" << fixed << setprecision(1) << pctErraTotal << "% total | " << pctErraConNotas << "% con notas)\n";
    cout << left << setw(35) << "DESEMPENO SATISFACTORIO (>= 3.25):" << right << setw(10) << sinRiesgo
         << " (" << fixed << setprecision(1) << pctSinRiesgo << "% con notas)\n";
    cout << string(59, '-') << "\n";
    cout << left << setw(35) << "Promedio acumulado institucional:" << right << setw(10) << fixed << setprecision(2) << promGlobal << " / 5.00\n";
    cout << left << setw(35) << "Tiempo de procesamiento:" << right << setw(10) << fixed << setprecision(4) << dur.count() << " segundos\n";
    cout << "===========================================================\n";

    // Muestra representativa de 10 estudiantes
    cout << "\n--- MUESTRA REPRESENTATIVA DE EVALUACION (10 Estudiantes) ---\n";
    cout << left << setw(13) << "ID"
         << setw(26) << "Nombre"
         << setw(10) << "Programa"
         << setw(10) << "Materias"
         << setw(10) << "Promedio"
         << setw(15) << "Estado ERRA" << "\n";
    cout << string(84, '-') << "\n";

    size_t muestra = min(size_t(10), estudiantes.size());
    for (size_t i = 0; i < muestra; ++i) {
        const auto& e = estudiantes[i];
        float prom = calcularPromedio(e);
        string erraStr;
        if (e.matriculas.empty()) {
            erraStr = "Sin notas";
        } else if (estaEnRiesgoEbra(e)) {
            erraStr = "[ALERTA ERRA]";
        } else {
            erraStr = "OK";
        }
        string nomCorto = (e.nombreCompleto.size() > 24) ? e.nombreCompleto.substr(0, 22) + ".." : e.nombreCompleto;
        cout << left << setw(13) << e.identificacion
             << setw(26) << nomCorto
             << setw(10) << e.codigoPrograma
             << setw(10) << e.matriculas.size()
             << setw(10) << fixed << setprecision(2) << prom
             << setw(15) << erraStr << "\n";
    }
    cout << "===========================================================\n";
}


