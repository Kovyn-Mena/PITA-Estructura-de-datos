#include "../include/generador.h"
#include "../include/persistencia.h"
#include "../include/interfaz.h"
#include <iostream>
#include <chrono>
#include <random>
#include <iomanip>
#include <sstream>

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
    for (size_t pIdx = 0; pIdx < programas.size(); ++pIdx) {
        const string& codProg = programas[pIdx].codigo;
        const string& nomProg = programas[pIdx].nombre;
        const auto& listaProfs = profesoresPorPrograma[pIdx];

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

            cursos.push_back(cur);
        }
    }

    cout << "  [5/5] Generando 225.000 estudiantes (1.500 por programa)...\n";
    long long codEstudianteNum = 1000000001LL;
    for (size_t pIdx = 0; pIdx < programas.size(); ++pIdx) {
        const string& codProg = programas[pIdx].codigo;
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
