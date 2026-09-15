"""Módulo de Generación Automática y Aleatoria de Datos Masivos (Parcial 1).

Estructura generada:
- 10 Facultades
- 150 Programas académicos (15 por facultad)
- 9.000 Profesores (60 por programa)
- 7.500 Cursos / Asignaturas (50 por programa)
- 225.000 Estudiantes (1.500 por programa)

Garantiza relaciones de integridad referencial válidas, identificadores únicos
y compatibilidad total con el modelo de persistencia y nómina.
"""

import time
import random
from entidades import Facultad, Programa, Curso, Estudiante, Profesor
from persistencia import (
    guardar_facultades,
    guardar_programas,
    guardar_cursos,
    guardar_estudiantes,
    guardar_profesores,
)
from interfaz import leer_si_no

NOMBRES = [
    "Carlos", "Juan", "Maria", "Laura", "Andres", "Valentina", "Diego", "Ana", "Luis", "Sofia",
    "Jorge", "Camila", "Mateo", "Mariana", "Gabriel", "Isabella", "Felipe", "Daniela", "Alejandro", "Paula",
    "David", "Natalia", "Sebastian", "Lucia", "Julian", "Catalina", "Camilo", "Andrea", "Esteban", "Carolina",
    "Santiago", "Sara", "Manuel", "Gabriela", "Ricardo", "Vanessa", "Fernando", "Diana", "Oscar", "Adriana"
]

APELLIDOS = [
    "Perez", "Rodriguez", "Gomez", "Fernandez", "Sanchez", "Torres", "Castro", "Diaz", "Vargas", "Martinez",
    "Rojas", "Morales", "Ortiz", "Gutierrez", "Navarro", "Alvarez", "Mendoza", "Castillo", "Jimenez", "Vasquez",
    "Romero", "Herrera", "Medina", "Aguilar", "Pena", "Silva", "Suarez", "Cabrera", "Rios", "Reyes",
    "Salazar", "Delgado", "Guerrero", "Cortes", "Cardona", "Mejia", "Bautista", "Valencia", "Ochoa", "Velez"
]

PREFIJOS_CURSO = [
    "Fundamentos de", "Introduccion a", "Metodos de", "Sistemas de", "Analisis de",
    "Diseno de", "Taller de", "Seminario de", "Laboratorio de", "Teoria de",
    "Practica de", "Modelos de", "Optimizacion de", "Evaluacion de", "Tecnologia de",
    "Estructura de", "Principios de", "Desarrollo de", "Investigacion en", "Gestion de"
]

SUFIJOS_ROMANOS = ["I", "II", "III", "IV", "V", "Avanzado", "Aplicado", "Integral"]

FACULTADES_DEF = [
    ("FING", "Facultad de Ingenierias y Tecnologias", "Armando Luis Cotes de Armas"),
    ("FACE", "Facultad de Ciencias Administrativas Contables y Economicas", "Carmen Alicia Perez"),
    ("FCS", "Facultad de Ciencias de la Salud", "Roberto Gomez Fernandez"),
    ("FDCP", "Facultad de Derecho Ciencias Politicas y Sociales", "Alvaro Enrique Rodriguez"),
    ("FBA", "Facultad de Bellas Artes", "Marta Cecilia Gutierrez"),
    ("FED", "Facultad de Educacion", "Luis Eduardo Martinez"),
    ("FCB", "Facultad de Ciencias Basicas", "Gloria Ines Mendoza"),
    ("FAGRO", "Facultad de Ciencias Agropecuarias y Ambientales", "Carlos Alberto Morales"),
    ("FHUM", "Facultad de Humanidades y Ciencias Sociales", "Patricia Elena Castillo"),
    ("FMED", "Facultad de Medicina", "Hernando Jose Alvarez"),
]

PROGRAMAS_POR_FACULTAD = [
    # 0: FING
    [
        ("Ingenieria de Sistemas", "Pregrado"),
        ("Ingenieria Electronica", "Pregrado"),
        ("Ingenieria Ambiental y Sanitaria", "Pregrado"),
        ("Ingenieria Agroindustrial", "Pregrado"),
        ("Ingenieria Civil", "Pregrado"),
        ("Ingenieria Mecanica", "Pregrado"),
        ("Ingenieria Industrial", "Pregrado"),
        ("Ingenieria Quimica", "Pregrado"),
        ("Ingenieria Biomedica", "Pregrado"),
        ("Ingenieria de Telecomunicaciones", "Pregrado"),
        ("Ingenieria de Alimentos", "Pregrado"),
        ("Ingenieria Mecatronica", "Pregrado"),
        ("Tecnologia en Desarrollo de Software", "Tecnologico"),
        ("Tecnologia en Redes y Seguridad", "Tecnologico"),
        ("Tecnologia en Automatizacion Industrial", "Tecnologico"),
    ],
    # 1: FACE
    [
        ("Administracion de Empresas", "Pregrado"),
        ("Administracion de Empresas Turisticas y Hoteleras", "Pregrado"),
        ("Comercio Internacional", "Pregrado"),
        ("Contaduria Publica", "Pregrado"),
        ("Economia", "Pregrado"),
        ("Finanzas y Negocios Internacionales", "Pregrado"),
        ("Mercadeo y Publicidad", "Pregrado"),
        ("Gestion del Talento Humano", "Pregrado"),
        ("Logistica y Distribucion Internacional", "Pregrado"),
        ("Administracion Financiera", "Pregrado"),
        ("Tecnologia en Gestion Bancaria", "Tecnologico"),
        ("Tecnologia en Gestion Logistica", "Tecnologico"),
        ("Especializacion en Finanzas", "Especializacion"),
        ("Especializacion en Gerencia Tributaria", "Especializacion"),
        ("Maestria en Administracion", "Maestria"),
    ],
    # 2: FCS
    [
        ("Enfermeria", "Pregrado"),
        ("Instrumentacion Quirurgica", "Pregrado"),
        ("Fisioterapia", "Pregrado"),
        ("Fonoaudiologia", "Pregrado"),
        ("Terapia Ocupacional", "Pregrado"),
        ("Nutricion y Dietetica", "Pregrado"),
        ("Odontologia", "Pregrado"),
        ("Optometria", "Pregrado"),
        ("Psicologia Clinica", "Pregrado"),
        ("Salud Ocupacional y Seguridad", "Pregrado"),
        ("Tecnologia en Atencion Prehospitalaria", "Tecnologico"),
        ("Tecnologia en Citohistologia", "Tecnologico"),
        ("Especializacion en Epidemiologia", "Especializacion"),
        ("Especializacion en Auditoria en Salud", "Especializacion"),
        ("Maestria en Salud Publica", "Maestria"),
    ],
    # 3: FDCP
    [
        ("Derecho", "Pregrado"),
        ("Psicologia", "Pregrado"),
        ("Sociologia", "Pregrado"),
        ("Ciencia Politica", "Pregrado"),
        ("Trabajo Social", "Pregrado"),
        ("Relaciones Internacionales", "Pregrado"),
        ("Antropologia", "Pregrado"),
        ("Criminalistica y Ciencias Forenses", "Pregrado"),
        ("Comunicacion Social y Periodismo", "Pregrado"),
        ("Filosofia Juridica", "Pregrado"),
        ("Especializacion en Derecho Penal", "Especializacion"),
        ("Especializacion en Derecho Administrativo", "Especializacion"),
        ("Especializacion en Derecho Constitucional", "Especializacion"),
        ("Especializacion en Derecho Laboral", "Especializacion"),
        ("Maestria en Conflicto y Paz", "Maestria"),
    ],
    # 4: FBA
    [
        ("Licenciatura en Artes", "Pregrado"),
        ("Musica", "Pregrado"),
        ("Arte Dramatico", "Pregrado"),
        ("Diseno Grafico", "Pregrado"),
        ("Danza Tradicional y Contemporanea", "Pregrado"),
        ("Artes Plasticas y Visuales", "Pregrado"),
        ("Cinematografia y Medios Audiovisuales", "Pregrado"),
        ("Diseno de Modas", "Pregrado"),
        ("Produccion Musical", "Pregrado"),
        ("Gestion Cultural", "Pregrado"),
        ("Diseno Industrial", "Pregrado"),
        ("Especializacion en Pedagogia del Arte", "Especializacion"),
        ("Especializacion en Creacion Sonora", "Especializacion"),
        ("Maestria en Artes Visuales", "Maestria"),
        ("Maestria en Etnomusicologia", "Maestria"),
    ],
    # 5: FED
    [
        ("Licenciatura en Matematicas", "Pregrado"),
        ("Licenciatura en Espanol e Ingles", "Pregrado"),
        ("Licenciatura en Literatura y Lengua Castellana", "Pregrado"),
        ("Licenciatura en Educacion Fisica Recreacion y Deportes", "Pregrado"),
        ("Licenciatura en Ciencias Naturales y Educacion Ambiental", "Pregrado"),
        ("Licenciatura en Educacion Infantil", "Pregrado"),
        ("Licenciatura en Ciencias Sociales", "Pregrado"),
        ("Licenciatura en Lenguas Extranjeras", "Pregrado"),
        ("Licenciatura en Informatica Educativa", "Pregrado"),
        ("Licenciatura en Pedagogia Infantil", "Pregrado"),
        ("Especializacion en Docencia Universitaria", "Especializacion"),
        ("Especializacion en Gestion Curricular", "Especializacion"),
        ("Especializacion en Orientacion Escolar", "Especializacion"),
        ("Maestria en Educacion", "Maestria"),
        ("Maestria en Neuroeducacion", "Maestria"),
    ],
    # 6: FCB
    [
        ("Microbiologia", "Pregrado"),
        ("Biologia", "Pregrado"),
        ("Quimica", "Pregrado"),
        ("Fisica", "Pregrado"),
        ("Matematicas Puras", "Pregrado"),
        ("Estadistica Aplicada", "Pregrado"),
        ("Geologia", "Pregrado"),
        ("Ciencias Ambientales", "Pregrado"),
        ("Bioquimica", "Pregrado"),
        ("Biotecnologia", "Pregrado"),
        ("Quimica Farmaceutica", "Pregrado"),
        ("Especializacion en Analisis Quimico", "Especializacion"),
        ("Especializacion en Biologia Molecular", "Especializacion"),
        ("Maestria en Ciencias Fisicas", "Maestria"),
        ("Maestria en Biologia Aplicada", "Maestria"),
    ],
    # 7: FAGRO
    [
        ("Agronomia", "Pregrado"),
        ("Medicina Veterinaria y Zootecnia", "Pregrado"),
        ("Ingenieria Agricola", "Pregrado"),
        ("Ingenieria Forestal", "Pregrado"),
        ("Zootecnia", "Pregrado"),
        ("Administracion de Empresas Agropecuarias", "Pregrado"),
        ("Agroecologia y Desarrollo Rural", "Pregrado"),
        ("Tecnologia en Produccion Agricola", "Tecnologico"),
        ("Tecnologia en Produccion Pecuaria", "Tecnologico"),
        ("Tecnologia en Riego y Drenaje", "Tecnologico"),
        ("Especializacion en Bienestar Animal", "Especializacion"),
        ("Especializacion en Gestion Ambiental Agropecuaria", "Especializacion"),
        ("Especializacion en Biotecnologia Vegetal", "Especializacion"),
        ("Maestria en Produccion Animal Tropical", "Maestria"),
        ("Maestria en Sanidad Vegetal", "Maestria"),
    ],
    # 8: FHUM
    [
        ("Historia", "Pregrado"),
        ("Filosofia", "Pregrado"),
        ("Geografia", "Pregrado"),
        ("Linguistica", "Pregrado"),
        ("Literatura", "Pregrado"),
        ("Lenguas Modernas", "Pregrado"),
        ("Teologia y Estudios Religiosos", "Pregrado"),
        ("Estudios Culturales", "Pregrado"),
        ("Humanidades Digitales", "Pregrado"),
        ("Archivistica y Gestion Documental", "Pregrado"),
        ("Especializacion en Estudios Regionales", "Especializacion"),
        ("Especializacion en Didactica de la Historia", "Especializacion"),
        ("Especializacion en Semiotica", "Especializacion"),
        ("Maestria en Filosofia Contemporanea", "Maestria"),
        ("Maestria en Literatura Latinoamericana", "Maestria"),
    ],
    # 9: FMED
    [
        ("Medicina General", "Pregrado"),
        ("Morfologia Humana", "Pregrado"),
        ("Fisiologia Medica", "Pregrado"),
        ("Farmacologia Clinica", "Pregrado"),
        ("Cirugia General", "Pregrado"),
        ("Pediatria", "Pregrado"),
        ("Ginecologia y Obstetricia", "Pregrado"),
        ("Medicina Interna", "Pregrado"),
        ("Anestesiologia", "Pregrado"),
        ("Patologia Forense y Clinica", "Pregrado"),
        ("Psiquiatria", "Pregrado"),
        ("Dermatologia", "Pregrado"),
        ("Especializacion en Gerencia Hospitalaria", "Especializacion"),
        ("Especializacion en Radiologia e Imagenes", "Especializacion"),
        ("Maestria en Ciencias Medicas", "Maestria"),
    ],
]


def generar_datos_masivos():
    """Genera en memoria las estructuras completas requeridas por Parcial 1."""
    rng = random.Random(123456)
    categorias = ["Auxiliar", "Asistente", "Asociado", "Titular"]
    posgrados = ["Ninguno", "Especializacion", "Maestria", "Doctorado"]
    horas_opciones = [4, 8, 12, 16]

    print("  [1/5] Generando 10 facultades...")
    facultades = [
        Facultad(codigo, nombre, decano, activo=True)
        for codigo, nombre, decano in FACULTADES_DEF
    ]

    print("  [2/5] Generando 150 programas academicos (15 por facultad)...")
    programas = []
    cod_prog_num = 1
    for f_idx, fac in enumerate(facultades):
        for nombre, nivel in PROGRAMAS_POR_FACULTAD[f_idx]:
            cod_prog = f"PRG{cod_prog_num:03d}"
            cod_prog_num += 1
            programas.append(Programa(cod_prog, nombre, nivel, fac.codigo, activo=True))

    print("  [3/5] Generando 9.000 profesores (60 por programa)...")
    profesores = []
    cod_prof_num = 70000001
    profesores_por_prog = {}

    for prog in programas:
        lista_ids_prog = []
        for _ in range(60):
            id_prof = str(cod_prof_num)
            cod_prof_num += 1
            nom = f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}"
            activo = (rng.randint(1, 100) <= 95)
            tipo_rand = rng.randint(1, 100)

            if tipo_rand <= 30:
                tipo = "Planta"
                dedicacion = "TiempoCompleto" if rng.randint(1, 100) <= 70 else "MedioTiempo"
                cat = rng.choice(categorias)
                horas = 0
                adhonorem = False
                exp = rng.randint(1, 25)
                p_tit = rng.randint(20, 150)
                p_prod = rng.randint(0, 60)
                posg = rng.choice(posgrados)
            elif tipo_rand <= 70:
                tipo = "Ocasional"
                dedicacion = "TiempoCompleto" if rng.randint(1, 100) <= 70 else "MedioTiempo"
                cat = rng.choice(categorias)
                horas = 0
                adhonorem = False
                exp = rng.randint(1, 15)
                p_tit = 0
                p_prod = 0
                posg = rng.choice(posgrados)
            else:
                tipo = "Catedratico"
                dedicacion = "HorasCatedra"
                cat = ""
                horas = rng.choice(horas_opciones)
                adhonorem = (rng.randint(1, 100) <= 2)
                exp = rng.randint(1, 15)
                p_tit = 0
                p_prod = 0
                posg = ""

            profesores.append(Profesor(
                identificacion=id_prof,
                nombre_completo=nom,
                codigo_programa=prog.codigo,
                tipo_vinculacion=tipo,
                dedicacion=dedicacion,
                categoria_escalafon=cat,
                horas_catedra_semanales=horas,
                ad_honorem=adhonorem,
                anios_experiencia=exp,
                puntos_titulos=p_tit,
                puntos_productividad=p_prod,
                activo=activo,
                posgrado=posg,
            ))
            lista_ids_prog.append(id_prof)
        profesores_por_prog[prog.codigo] = lista_ids_prog

    print("  [4/5] Generando 7.500 materias (50 por programa con profesor asignado)...")
    cursos = []
    cod_curso_num = 1
    for prog in programas:
        lista_profs = profesores_por_prog[prog.codigo]
        for c_idx in range(50):
            cod_cur = f"CUR{cod_curso_num:05d}"
            cod_curso_num += 1
            pref = rng.choice(PREFIJOS_CURSO)
            suf = SUFIJOS_ROMANOS[c_idx % len(SUFIJOS_ROMANOS)]
            nombre_cur = f"{pref} {prog.nombre} {suf}"
            creditos = rng.randint(2, 4)
            prof_id = rng.choice(lista_profs)
            activo = (rng.randint(1, 100) <= 95)

            cursos.append(Curso(
                codigo=cod_cur,
                nombre=nombre_cur,
                creditos=creditos,
                codigo_profesor=prof_id,
                codigo_programa=prog.codigo,
                activo=activo,
            ))

    print("  [5/5] Generando 225.000 estudiantes (1.500 por programa)...")
    estudiantes = []
    cod_est_num = 1000000001
    for prog in programas:
        for _ in range(1500):
            id_est = str(cod_est_num)
            cod_est_num += 1
            nom = f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}"
            rand_est = rng.randint(1, 100)
            if rand_est <= 90:
                estado = "Activo"
                activo = True
            elif rand_est <= 95:
                estado = "Graduado"
                activo = True
            else:
                estado = "Inactivo"
                activo = False

            estudiantes.append(Estudiante(
                identificacion=id_est,
                nombre_completo=nom,
                codigo_programa=prog.codigo,
                estado=estado,
                activo=activo,
            ))

    return facultades, programas, profesores, cursos, estudiantes


def menu_generacion_masiva(
    facultades, programas, cursos, estudiantes, profesores,
    ruta_facultades, ruta_programas, ruta_cursos,
    ruta_estudiantes, ruta_matriculas, ruta_profesores
):
    """Muestra confirmación y ejecuta la generación masiva con persistencia."""
    print("\n===========================================================")
    print(" GENERACION MASIVA DE DATOS ALEATORIOS (PARCIAL 1)")
    print("===========================================================")
    print("Estructura requerida:")
    print(" - 10 Facultades")
    print(" - 150 Programas academicos (15 por facultad)")
    print(" - 9.000 Profesores (60 por programa)")
    print(" - 7.500 Materias / Cursos (50 por programa)")
    print(" - 225.000 Estudiantes (1.500 por programa)\n")
    print("ATENCION: Esta operacion reemplazara los datos actuales en")
    print("memoria y sobrescribira los archivos de persistencia en disco.")

    resp = leer_si_no("\nEsta seguro de generar los datos masivos? (s/n): ")
    if resp != "s":
        print("\nOperacion cancelada. Los datos existentes no sufrieron cambios.")
        return

    print("\nIniciando generacion masiva...")
    t0 = time.time()

    nuevas_fac, nuevos_prog, nuevos_prof, nuevos_cur, nuevos_est = generar_datos_masivos()

    # Actualizar listas en memoria
    facultades.clear()
    facultades.extend(nuevas_fac)

    programas.clear()
    programas.extend(nuevos_prog)

    profesores.clear()
    profesores.extend(nuevos_prof)

    cursos.clear()
    cursos.extend(nuevos_cur)

    estudiantes.clear()
    estudiantes.extend(nuevos_est)

    print("\nGuardando datos en disco (formato delimitado por '|')...")
    guardar_facultades(facultades, ruta_facultades)
    guardar_programas(programas, ruta_programas)
    guardar_profesores(profesores, ruta_profesores)
    guardar_cursos(cursos, ruta_cursos)
    guardar_estudiantes(estudiantes, ruta_estudiantes, ruta_matriculas)

    t1 = time.time()

    print("\n===========================================================")
    print(" GENERACION Y PERSISTENCIA COMPLETADA CON EXITO")
    print("===========================================================")
    print(f"Tiempo total: {t1 - t0:.2f} segundos.")
    print("Resumen de registros generados:")
    print(f" - Facultades:  {len(facultades)}")
    print(f" - Programas:   {len(programas)}")
    print(f" - Profesores:  {len(profesores)}")
    print(f" - Cursos:      {len(cursos)}")
    print(f" - Estudiantes: {len(estudiantes)}")
    print("Archivos actualizados correctamente en carpeta data/.")
