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

DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]
FRANJAS_HORARIAS = [
    (6, 8),
    (8, 10),
    (10, 12),
    (14, 16),
    (16, 18),
    (18, 20),
    (20, 22),
]

SALONES_DEF = [
    f"{ed}-{piso}{num:02d}"
    for ed in "ABCDEFGHIJ"
    for piso in range(1, 5)
    for num in range(1, 11)
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
    cursos_por_prog = {}
    for prog in programas:
        lista_profs = profesores_por_prog[prog.codigo]
        lista_cursos_prog = []
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
            lista_cursos_prog.append(cod_cur)
        cursos_por_prog[prog.codigo] = lista_cursos_prog

    print("  [4.1] Generando horarios academicos libres de conflicto para 7.500 materias...")
    generar_horarios_cursos(cursos)

    print("  [5/5] Generando 225.000 estudiantes (1.500 por programa) con matriculas y calificaciones...")
    estudiantes = []
    cod_est_num = 1000000001
    for prog in programas:
        lista_cur = cursos_por_prog[prog.codigo]
        len_cur = len(lista_cur)
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

            est = Estudiante(
                identificacion=id_est,
                nombre_completo=nom,
                codigo_programa=prog.codigo,
                estado=estado,
                activo=activo,
            )

            # Asignacion de matriculas y calificaciones (ERRA: promedio < 3.25)
            # ~95% de estudiantes tienen 3-4 materias con notas
            # ~5% sin materias (recien matriculados / inactivos sin registro)
            if rand_est <= 95 and len_cur > 0:
                riesgo_rand = rng.randint(1, 100)
                if riesgo_rand <= 22:
                    base_promedio = rng.uniform(1.8, 3.20)
                else:
                    base_promedio = rng.uniform(3.30, 4.80)

                num_cursos = rng.randint(3, 4)
                start_offset = rng.randint(0, len_cur - 1)
                for k in range(num_cursos):
                    cod_c = lista_cur[(start_offset + k) % len_cur]
                    nota = base_promedio + rng.uniform(-0.35, 0.35)
                    nota = max(1.0, min(5.0, round(nota, 1)))
                    est.matriculas.append({"codigo_curso": cod_c, "nota": nota})

            estudiantes.append(est)

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


def generar_horarios_cursos(cursos):
    """Asigna horarios y aulas sin conflictos para cada asignatura de la lista."""
    num_salones = len(SALONES_DEF)
    num_franjas = len(FRANJAS_HORARIAS)
    num_slots = len(DIAS_SEMANA) * num_franjas

    prof_ocupado = {}
    salon_ocupado = {}

    rng = random.Random(987654)
    asignados = 0

    for c in cursos:
        prof_id = c.codigo_profesor
        start_slot = rng.randint(0, num_slots - 1)
        start_salon = rng.randint(0, num_salones - 1)
        asignado = False

        for s_step in range(num_slots):
            slot = (start_slot + s_step) % num_slots
            mask = 1 << slot

            if prof_id and (prof_ocupado.get(prof_id, 0) & mask):
                continue

            for r_step in range(num_salones):
                sal_idx = (start_salon + r_step) % num_salones
                sal = SALONES_DEF[sal_idx]

                if not (salon_ocupado.get(sal, 0) & mask):
                    if prof_id:
                        prof_ocupado[prof_id] = prof_ocupado.get(prof_id, 0) | mask
                    salon_ocupado[sal] = salon_ocupado.get(sal, 0) | mask

                    d_idx = slot // num_franjas
                    f_idx = slot % num_franjas

                    c.dia = DIAS_SEMANA[d_idx]
                    c.hora_inicio = FRANJAS_HORARIAS[f_idx][0]
                    c.hora_fin = FRANJAS_HORARIAS[f_idx][1]
                    c.salon = sal

                    asignado = True
                    asignados += 1
                    break
            if asignado:
                break

    return asignados


def menu_generacion_horarios(cursos, ruta_cursos):
    """Menú interactivo de consola para generar y guardar horarios de cursos."""
    print("\n===========================================================")
    print("      GENERACION AUTOMATICA DE HORARIOS ACADEMICOS         ")
    print("===========================================================")
    print(f"Total de materias a programar: {len(cursos):,}")
    print("Parametros de franjas y aulas:")
    print(" - Dias: Lunes a Sabado (6 dias)")
    print(" - Franjas horarias: 06:00 a 22:00 (bloques de 2 horas)")
    print(" - Salones disponibles: 400 aulas (Edificios A al J)")
    print(" - Control de conflictos: 0 colisiones en profesor o aula")

    resp = leer_si_no("\nDesea generar y guardar los horarios de las materias? (s/n): ")
    if resp != "s":
        print("Operacion cancelada. No se modificaron los horarios.")
        return

    print("\nGenerando horarios academicos libres de conflicto...")
    t0 = time.time()
    asignados = generar_horarios_cursos(cursos)
    guardar_cursos(cursos, ruta_cursos)
    t1 = time.time()

    print("\n===========================================================")
    print("      HORARIOS GENERADOS Y GUARDADOS CON EXITO             ")
    print("===========================================================")
    print(f"Materias procesadas:           {len(cursos):,}")
    print(f"Materias con horario asignado: {asignados:,}")
    print("Conflictos profesor / franja : 0")
    print("Conflictos salon / franja    : 0")
    print(f"Tiempo de ejecucion:           {t1 - t0:.3f} segundos.")
    print(f"Archivo de datos actualizado:  {ruta_cursos}")

    # Muestra automatica de 4 ejemplos de cursos con horario
    print("\n--- EJEMPLOS DE ASIGNATURAS CON HORARIO ASIGNADO ---")
    print(f"{'Codigo':<10} {'Nombre Asignatura':<33} {'Programa':<10} {'Profesor':<12} {'Dia':<12} {'Horario':<15} {'Salon':<10}")
    print("-" * 102)

    mostrados = 0
    for c in cursos:
        if getattr(c, "hora_inicio", 0) > 0:
            franja = f"{c.hora_inicio}:00-{c.hora_fin}:00"
            nom = (c.nombre[:31] + "..") if len(c.nombre) > 33 else c.nombre
            dia_str = getattr(c, "dia", "") or "N/A"
            sal_str = getattr(c, "salon", "") or "N/A"
            print(f"{c.codigo:<10} {nom:<33} {c.codigo_programa:<10} {c.codigo_profesor:<12} {dia_str:<12} {franja:<15} {sal_str:<10}")
            mostrados += 1
            if mostrados >= 4:
                break


def consultar_horario_curso(cursos):
    """Permite consultar el horario de un curso específico o muestra una tabla representativa."""
    if not cursos:
        print("\nNo hay cursos registrados.")
        return

    print("\n--- CONSULTA DE HORARIOS DE ASIGNATURAS ---")
    codigo = input("Ingrese codigo del curso (ej: CUR00001) o presione ENTER para ver muestra: ").strip()

    if not codigo or codigo.lower() == "muestra":
        print("\n--- MUESTRA REPRESENTATIVA DE HORARIOS (10 Asignaturas) ---")
        print(f"{'Codigo':<10} {'Nombre Asignatura':<35} {'Dia':<12} {'Franja':<14} {'Salon':<10} {'Profesor':<12} {'Programa':<10}")
        print("-" * 103)
        muestra = cursos[:10]
        for c in muestra:
            franja = f"{c.hora_inicio}:00 - {c.hora_fin}:00" if getattr(c, "hora_inicio", 0) > 0 else "Sin horario"
            dia_str = getattr(c, "dia", "") or "N/A"
            sal_str = getattr(c, "salon", "") or "N/A"
            nom = c.nombre[:32] + ".." if len(c.nombre) > 34 else c.nombre
            print(f"{c.codigo:<10} {nom:<35} {dia_str:<12} {franja:<14} {sal_str:<10} {c.codigo_profesor:<12} {c.codigo_programa:<10}")
        return

    encontrado = None
    for c in cursos:
        if c.codigo.upper() == codigo.upper():
            encontrado = c
            break

    if encontrado:
        c = encontrado
        print("\n=======================================================")
        print(f"FICHA DE HORARIO - {c.codigo}")
        print("=======================================================")
        print(f"Asignatura    : {c.nombre}")
        print(f"Creditos      : {c.creditos}")
        print(f"Programa      : {c.codigo_programa}")
        print(f"Profesor      : {c.codigo_profesor}")
        dia = getattr(c, "dia", "") or "(Sin horario)"
        print(f"Dia           : {dia}")
        if getattr(c, "hora_inicio", 0) > 0:
            print(f"Horario       : {c.hora_inicio}:00 a {c.hora_fin}:00")
        else:
            print("Horario       : (Sin horario)")
        salon = getattr(c, "salon", "") or "(Sin salon)"
        print(f"Aula/Salon    : {salon}")
        estado = "Activo" if c.activo else "Inactivo"
        print(f"Estado        : {estado}")
        print("=======================================================")
    else:
        print(f"Curso con codigo {codigo} no encontrado.")


def evaluar_erra_masivo(estudiantes):
    """Evalúa masivamente la alerta institucional ERRA (promedio acumulado < 3.25)
    en todos los estudiantes registrados.
    """
    if not estudiantes:
        print("\nNo hay estudiantes registrados en el sistema para evaluar.")
        return

    print("\n===========================================================")
    print("     EVALUACION MASIVA DE RENDIMIENTO ACADEMICO (ERRA)     ")
    print("===========================================================")
    print("Criterio institucional : Promedio acumulado < 3.25")
    print("Regla de proteccion    : Estudiantes sin notas no generan alerta")
    print(f"Total de estudiantes   : {len(estudiantes):,}")
    print("-----------------------------------------------------------")
    print("Evaluando desempeno academico institucional...")

    t0 = time.time()

    total = len(estudiantes)
    con_notas = 0
    sin_notas = 0
    en_erra = 0
    sin_riesgo = 0
    suma_promedios = 0.0

    for e in estudiantes:
        if not e.matriculas:
            sin_notas += 1
        else:
            con_notas += 1
            prom = e.calcular_promedio()
            suma_promedios += prom
            if e.esta_en_riesgo_ebra():
                en_erra += 1
            else:
                sin_riesgo += 1

    t1 = time.time()
    dur = t1 - t0

    prom_global = (suma_promedios / con_notas) if con_notas > 0 else 0.0
    pct_erra_total = (en_erra * 100.0) / total
    pct_erra_con_notas = (en_erra * 100.0 / con_notas) if con_notas > 0 else 0.0
    pct_sin_riesgo = (sin_riesgo * 100.0 / con_notas) if con_notas > 0 else 0.0
    pct_sin_notas = (sin_notas * 100.0) / total

    print("\n===========================================================")
    print("          RESUMEN CONSOLIDADO DE ALERTA ERRA               ")
    print("===========================================================")
    print(f"{'Total estudiantes en base:':<35} {total:>10,}")
    print(f"{'Estudiantes con asignaturas/notas:':<35} {con_notas:>10,} ({con_notas * 100.0 / total:.1f}%)")
    print(f"{'Estudiantes sin notas (sin alerta):':<35} {sin_notas:>10,} ({pct_sin_notas:.1f}%)")
    print("-" * 59)
    print(f"{'EN RIESGO ERRA (Promedio < 3.25):':<35} {en_erra:>10,} ({pct_erra_total:.1f}% total | {pct_erra_con_notas:.1f}% con notas)")
    print(f"{'DESEMPENO SATISFACTORIO (>= 3.25):':<35} {sin_riesgo:>10,} ({pct_sin_riesgo:.1f}% con notas)")
    print("-" * 59)
    print(f"{'Promedio acumulado institucional:':<35} {prom_global:>10.2f} / 5.00")
    print(f"{'Tiempo de procesamiento:':<35} {dur:>10.4f} segundos")
    print("===========================================================")

    # Muestra representativa de 10 estudiantes
    print("\n--- MUESTRA REPRESENTATIVA DE EVALUACION (10 Estudiantes) ---")
    print(f"{'ID':<13} {'Nombre':<26} {'Programa':<10} {'Materias':<10} {'Promedio':<10} {'Estado ERRA':<15}")
    print("-" * 84)

    muestra = estudiantes[:10]
    for e in muestra:
        prom = e.calcular_promedio()
        if not e.matriculas:
            erra_str = "Sin notas"
        elif e.esta_en_riesgo_ebra():
            erra_str = "[ALERTA ERRA]"
        else:
            erra_str = "OK"
        nom_corto = (e.nombre_completo[:22] + "..") if len(e.nombre_completo) > 24 else e.nombre_completo
        print(f"{e.identificacion:<13} {nom_corto:<26} {e.codigo_programa:<10} {len(e.matriculas):<10} {prom:<10.2f} {erra_str:<15}")
    print("===========================================================")


