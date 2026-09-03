"""Funciones de gestion (CRUD) por entidad.
FACULTADES, PROGRAMAS y CURSOS estan completos (mismo patron que la
version C++). ESTUDIANTES, PROFESORES y ADMINISTRATIVOS quedan pendientes
para el siguiente bloque de Python."""

from entidades import Facultad, Programa, Curso, Estudiante, Profesor, Administrativo
from interfaz import leer_palabra, es_cancelar, leer_entero, leer_si_no


# ============================ FACULTADES ============================

def crear_facultad(facultades):
    codigo = leer_palabra("Codigo facultad (o 'cancelar' para volver): ")
    if es_cancelar(codigo):
        print("Operacion cancelada.")
        return
    if buscar_facultad(facultades, codigo) is not None:
        print("Ya existe una facultad con ese codigo.")
        return
    nombre = input("Nombre: ").strip()
    decano = input("Decano: ").strip()
    facultades.append(Facultad(codigo, nombre, decano, activo=True))
    print("Facultad creada correctamente.")


def listar_facultades(facultades):
    print("\n--- Facultades registradas ---")
    if not facultades:
        print("(no hay facultades registradas)")
        return
    for f in facultades:
        print(f)


def buscar_facultad(facultades, codigo):
    for f in facultades:
        if f.codigo == codigo:
            return f
    return None


def modificar_facultad(facultades, codigo):
    f = buscar_facultad(facultades, codigo)
    if f is None:
        print("Facultad no encontrada.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({f.nombre}): ").strip()
    nuevo_decano = input(f"Nuevo decano ({f.decano}): ").strip()
    if nuevo_nombre:
        f.nombre = nuevo_nombre
    if nuevo_decano:
        f.decano = nuevo_decano
    print("Facultad modificada.")


def desactivar_facultad(facultades, codigo):
    f = buscar_facultad(facultades, codigo)
    if f is None:
        print("Facultad no encontrada.")
        return
    f.activo = False  # borrado LOGICO: se conserva el registro
    print("Facultad desactivada (borrado logico).")


def eliminar_facultad(facultades, codigo):
    f = buscar_facultad(facultades, codigo)
    if f is None:
        print("Facultad no encontrada.")
        return
    facultades.remove(f)  # borrado FISICO
    print("Facultad eliminada permanentemente.")


# ============================ PROGRAMAS ============================
# Mismo patron que Facultad, con una validacion extra: un Programa
# pertenece a una Facultad, asi que se verifica que la facultad exista
# y este activa antes de crear el programa.

def crear_programa(programas, facultades):
    codigo = leer_palabra("Codigo programa (o 'cancelar' para volver): ")
    if es_cancelar(codigo):
        print("Operacion cancelada.")
        return
    if buscar_programa(programas, codigo) is not None:
        print("Ya existe un programa con ese codigo.")
        return

    codigo_facultad = leer_palabra("Codigo de la facultad a la que pertenece: ")
    facultad = buscar_facultad(facultades, codigo_facultad)
    if facultad is None:
        print("Esa facultad no existe. Cree primero la facultad.")
        return
    if not facultad.activo:
        print("Esa facultad esta inactiva, no se le pueden asociar programas.")
        return

    nombre = input("Nombre del programa: ").strip()
    nivel = input("Nivel (Tecnologico/Pregrado/Especializacion/Maestria): ").strip()
    programas.append(Programa(codigo, nombre, nivel, codigo_facultad, activo=True))
    print("Programa creado correctamente.")


def listar_programas(programas):
    print("\n--- Programas academicos registrados ---")
    if not programas:
        print("(no hay programas registrados)")
        return
    for p in programas:
        estado = "Activo" if p.activo else "Inactivo"
        print(f"{p.codigo} | {p.nombre} | {p.nivel} | Facultad: {p.codigo_facultad} | {estado}")


def buscar_programa(programas, codigo):
    for p in programas:
        if p.codigo == codigo:
            return p
    return None


def modificar_programa(programas, codigo):
    p = buscar_programa(programas, codigo)
    if p is None:
        print("Programa no encontrado.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({p.nombre}): ").strip()
    nuevo_nivel = input(f"Nuevo nivel ({p.nivel}): ").strip()
    if nuevo_nombre:
        p.nombre = nuevo_nombre
    if nuevo_nivel:
        p.nivel = nuevo_nivel
    print("Programa modificado.")


def desactivar_programa(programas, codigo):
    p = buscar_programa(programas, codigo)
    if p is None:
        print("Programa no encontrado.")
        return
    p.activo = False
    print("Programa desactivado (borrado logico).")


def eliminar_programa(programas, codigo):
    p = buscar_programa(programas, codigo)
    if p is None:
        print("Programa no encontrado.")
        return
    programas.remove(p)
    print("Programa eliminado permanentemente.")


# ============================ CURSOS ============================
# Mismo patron, validando que el Programa exista. codigo_profesor se
# guarda como texto libre por ahora (aun no existe el modulo de
# Profesores en Python); se valida contra la lista real en el siguiente bloque.

def crear_curso(cursos, programas):
    codigo = leer_palabra("Codigo curso (o 'cancelar' para volver): ")
    if es_cancelar(codigo):
        print("Operacion cancelada.")
        return
    if buscar_curso(cursos, codigo) is not None:
        print("Ya existe un curso con ese codigo.")
        return

    codigo_programa = leer_palabra("Codigo del programa al que pertenece: ")
    programa = buscar_programa(programas, codigo_programa)
    if programa is None:
        print("Ese programa no existe. Cree primero el programa.")
        return
    if not programa.activo:
        print("Ese programa esta inactivo, no se le pueden asociar cursos.")
        return

    nombre = input("Nombre del curso: ").strip()
    try:
        creditos = int(input("Creditos: ").strip())
    except ValueError:
        print("Creditos invalidos, se asume 0.")
        creditos = 0
    codigo_profesor = input("Codigo del profesor (ENTER si aun no se asigna): ").strip()

    cursos.append(Curso(codigo, nombre, creditos, codigo_profesor, codigo_programa, activo=True))
    print("Curso creado correctamente.")


def listar_cursos(cursos):
    print("\n--- Cursos registrados ---")
    if not cursos:
        print("(no hay cursos registrados)")
        return
    for c in cursos:
        estado = "Activo" if c.activo else "Inactivo"
        profesor = c.codigo_profesor if c.codigo_profesor else "(sin asignar)"
        print(f"{c.codigo} | {c.nombre} | {c.creditos} creditos | "
              f"Programa: {c.codigo_programa} | Profesor: {profesor} | {estado}")


def buscar_curso(cursos, codigo):
    for c in cursos:
        if c.codigo == codigo:
            return c
    return None


def modificar_curso(cursos, codigo):
    c = buscar_curso(cursos, codigo)
    if c is None:
        print("Curso no encontrado.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({c.nombre}): ").strip()
    nuevos_creditos = input(f"Nuevos creditos ({c.creditos}): ").strip()
    if nuevo_nombre:
        c.nombre = nuevo_nombre
    if nuevos_creditos:
        try:
            c.creditos = int(nuevos_creditos)
        except ValueError:
            print("Creditos invalidos, se mantiene el valor anterior.")
    print("Curso modificado.")


def desactivar_curso(cursos, codigo):
    c = buscar_curso(cursos, codigo)
    if c is None:
        print("Curso no encontrado.")
        return
    c.activo = False
    print("Curso desactivado (borrado logico).")


def eliminar_curso(cursos, codigo):
    c = buscar_curso(cursos, codigo)
    if c is None:
        print("Curso no encontrado.")
        return
    cursos.remove(c)
    print("Curso eliminado permanentemente.")


# ============================ ESTUDIANTES ============================
# Mismo patron, mas dos operaciones propias del negocio academico:
# matricular/cancelar curso, y la ficha con promedio + alerta EBRA.
# Las matriculas viven DENTRO de cada Estudiante (lista anidada de dicts).

def crear_estudiante(estudiantes, programas):
    identificacion = leer_palabra("Identificacion (o 'cancelar' para volver): ")
    if es_cancelar(identificacion):
        print("Operacion cancelada.")
        return
    if buscar_estudiante(estudiantes, identificacion) is not None:
        print("Ya existe un estudiante con esa identificacion.")
        return

    codigo_programa = leer_palabra("Codigo del programa al que pertenece: ")
    programa = buscar_programa(programas, codigo_programa)
    if programa is None:
        print("Ese programa no existe. Cree primero el programa.")
        return

    nombre = input("Nombre completo: ").strip()
    estudiantes.append(Estudiante(identificacion, nombre, codigo_programa,
                                   estado="Activo", activo=True))
    print("Estudiante creado correctamente.")


def listar_estudiantes(estudiantes):
    print("\n--- Estudiantes registrados ---")
    if not estudiantes:
        print("(no hay estudiantes registrados)")
        return
    for e in estudiantes:
        estado_activo = "Activo" if e.activo else "Inactivo"
        print(f"{e.identificacion} | {e.nombre_completo} | Programa: {e.codigo_programa} | "
              f"{e.estado} | {estado_activo} | Cursos matriculados: {len(e.matriculas)}")


def buscar_estudiante(estudiantes, identificacion):
    for e in estudiantes:
        if e.identificacion == identificacion:
            return e
    return None


def modificar_estudiante(estudiantes, identificacion):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({e.nombre_completo}): ").strip()
    if nuevo_nombre:
        e.nombre_completo = nuevo_nombre
    print("Estudiante modificado.")


def desactivar_estudiante(estudiantes, identificacion):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return
    e.activo = False
    e.estado = "Inactivo"
    print("Estudiante desactivado (borrado logico).")


def eliminar_estudiante(estudiantes, identificacion):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return
    estudiantes.remove(e)
    print("Estudiante eliminado permanentemente.")


# ---- Matricula / cancelacion (operan sobre la lista anidada) ----

def matricular_curso(estudiantes, identificacion, cursos):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return

    codigo_curso = input("Codigo del curso a matricular: ").strip()
    curso = buscar_curso(cursos, codigo_curso)
    if curso is None:
        print("Ese curso no existe.")
        return
    if not curso.activo:
        print("Ese curso esta inactivo.")
        return

    # Evitar doble matricula en el mismo curso
    for m in e.matriculas:
        if m["codigo_curso"] == codigo_curso:
            print("El estudiante ya esta matriculado en ese curso.")
            return

    nota_texto = input("Nota (0.0 si aun no tiene, se puede modificar despues): ").strip()
    try:
        nota = float(nota_texto)
    except ValueError:
        print("Nota invalida, se asume 0.0")
        nota = 0.0

    e.matriculas.append({"codigo_curso": codigo_curso, "nota": nota})
    print("Matricula registrada correctamente.")


def cancelar_curso(estudiantes, identificacion):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return

    codigo_curso = input("Codigo del curso a cancelar: ").strip()
    for m in e.matriculas:
        if m["codigo_curso"] == codigo_curso:
            e.matriculas.remove(m)
            print("Curso cancelado (retirado de la matricula).")
            return
    print("El estudiante no esta matriculado en ese curso.")


def consultar_estudiante(estudiantes, identificacion):
    e = buscar_estudiante(estudiantes, identificacion)
    if e is None:
        print("Estudiante no encontrado.")
        return

    print("\n===== Ficha del estudiante =====")
    print(f"ID: {e.identificacion} | {e.nombre_completo}")
    print(f"Programa: {e.codigo_programa} | Estado: {e.estado}")
    print("Cursos matriculados:")
    if not e.matriculas:
        print("  (ninguno)")
    else:
        for m in e.matriculas:
            print(f"  {m['codigo_curso']} -> nota: {m['nota']}")
    print(f"Promedio acumulado: {e.calcular_promedio():.2f}")
    if e.esta_en_riesgo_ebra():
        print("*** ALERTA EBRA: estudiante en riesgo de desercion academica"
              " (promedio < 3.25) ***")
    print("=================================")


# ============================ PROFESORES ============================
# Los campos con valores fijos (tipo de vinculacion, dedicacion,
# categoria) se eligen por MENU NUMERADO en vez de texto libre, para
# que un error de tipeo no dane silenciosamente el calculo de nomina.

def crear_profesor(profesores, programas):
    identificacion = leer_palabra("Identificacion (o 'cancelar' para volver): ")
    if es_cancelar(identificacion):
        print("Operacion cancelada.")
        return
    if buscar_profesor(profesores, identificacion) is not None:
        print("Ya existe un profesor con esa identificacion.")
        return

    codigo_programa = leer_palabra("Codigo del programa al que pertenece: ")
    programa = buscar_programa(programas, codigo_programa)
    if programa is None:
        print("Ese programa no existe. Cree primero el programa.")
        return

    nombre = input("Nombre completo: ").strip()

    print("\nTipo de vinculacion:")
    print("1. Planta\n2. Ocasional\n3. Catedratico")
    opcion_tipo = leer_entero("Opcion: ")
    tipos = {1: "Planta", 2: "Ocasional", 3: "Catedratico"}
    if opcion_tipo not in tipos:
        print("Opcion de tipo de vinculacion invalida.")
        return
    tipo_vinculacion = tipos[opcion_tipo]

    horas_catedra = 0
    ad_honorem = False
    categoria_escalafon = ""

    if tipo_vinculacion == "Catedratico":
        dedicacion = "HorasCatedra"
        horas_catedra = leer_entero("Horas catedra semanales (maximo 18): ")
        if horas_catedra > 18:
            print("El Acuerdo 027 de 2024 limita a 18 horas semanales.")
            return
        ad_honorem = leer_si_no("Es vinculacion ad-honorem (sin remuneracion)? (s/n): ") == "s"
    else:
        print("\nDedicacion:")
        print("1. TiempoCompleto\n2. MedioTiempo")
        opcion_dedic = leer_entero("Opcion: ")
        dedicaciones = {1: "TiempoCompleto", 2: "MedioTiempo"}
        if opcion_dedic not in dedicaciones:
            print("Opcion de dedicacion invalida.")
            return
        dedicacion = dedicaciones[opcion_dedic]

        print("\nCategoria escalafon:")
        print("1. Auxiliar\n2. Asistente\n3. Asociado\n4. Titular")
        opcion_cat = leer_entero("Opcion: ")
        categorias = {1: "Auxiliar", 2: "Asistente", 3: "Asociado", 4: "Titular"}
        if opcion_cat not in categorias:
            print("Opcion de categoria invalida.")
            return
        categoria_escalafon = categorias[opcion_cat]

    anios_experiencia = leer_entero("Anios de experiencia: ")
    puntos_titulos = leer_entero("Puntos por titulos: ")
    puntos_productividad = leer_entero("Puntos por productividad: ")

    profesores.append(Profesor(
        identificacion, nombre, codigo_programa, tipo_vinculacion, dedicacion,
        categoria_escalafon, horas_catedra, ad_honorem, anios_experiencia,
        puntos_titulos, puntos_productividad, activo=True
    ))
    print("Profesor creado correctamente.")


def listar_profesores(profesores):
    print("\n--- Profesores registrados ---")
    if not profesores:
        print("(no hay profesores registrados)")
        return
    for p in profesores:
        estado = "Activo" if p.activo else "Inactivo"
        print(f"{p.identificacion} | {p.nombre_completo} | {p.tipo_vinculacion} | "
              f"{p.dedicacion} | {p.categoria_escalafon} | Programa: {p.codigo_programa} | {estado}")


def buscar_profesor(profesores, identificacion):
    for p in profesores:
        if p.identificacion == identificacion:
            return p
    return None


def modificar_profesor(profesores, identificacion):
    p = buscar_profesor(profesores, identificacion)
    if p is None:
        print("Profesor no encontrado.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({p.nombre_completo}): ").strip()
    if nuevo_nombre:
        p.nombre_completo = nuevo_nombre
    nuevos_anios = input(f"Nuevos anios de experiencia ({p.anios_experiencia}): ").strip()
    if nuevos_anios:
        try:
            p.anios_experiencia = int(nuevos_anios)
        except ValueError:
            print("Valor invalido, se mantiene el anterior.")
    print("Profesor modificado.")


def desactivar_profesor(profesores, identificacion):
    p = buscar_profesor(profesores, identificacion)
    if p is None:
        print("Profesor no encontrado.")
        return
    p.activo = False
    print("Profesor desactivado (borrado logico).")


def eliminar_profesor(profesores, identificacion):
    p = buscar_profesor(profesores, identificacion)
    if p is None:
        print("Profesor no encontrado.")
        return
    profesores.remove(p)
    print("Profesor eliminado permanentemente.")


def consultar_profesor(profesores, identificacion):
    p = buscar_profesor(profesores, identificacion)
    if p is None:
        print("Profesor no encontrado.")
        return
    from nomina import imprimir_desglose_nomina
    imprimir_desglose_nomina(p)


# ============================ ADMINISTRATIVOS ============================
# Mismo patron. La facultad es OPCIONAL (vacia = nivel central). El tipo
# de contratacion se elige por menu numerado, igual que en Profesor.

def crear_administrativo(admins, facultades):
    identificacion = leer_palabra("Identificacion (o 'cancelar' para volver): ")
    if es_cancelar(identificacion):
        print("Operacion cancelada.")
        return
    if buscar_administrativo(admins, identificacion) is not None:
        print("Ya existe un administrativo con esa identificacion.")
        return

    nombre = input("Nombre completo: ").strip()
    cargo = input("Cargo (ej. Secretario Academico, Auxiliar Financiero): ").strip()
    categoria = input("Categoria (ej. Nivel 1, Nivel 2, Nivel 3): ").strip()

    codigo_facultad = leer_palabra("Codigo de facultad (ENTER en blanco = nivel central): ")
    if codigo_facultad and buscar_facultad(facultades, codigo_facultad) is None:
        print("Esa facultad no existe. Cree primero la facultad, o deje en blanco para nivel central.")
        return

    print("\nTipo de contratacion:")
    print("1. Planta\n2. Provisional\n3. Contrato")
    opcion_tipo = leer_entero("Opcion: ")
    tipos = {1: "Planta", 2: "Provisional", 3: "Contrato"}
    if opcion_tipo not in tipos:
        print("Opcion de tipo de contratacion invalida.")
        return
    tipo_contratacion = tipos[opcion_tipo]

    salario_base = leer_entero("Salario base: ")

    admins.append(Administrativo(identificacion, nombre, cargo, categoria,
                                  tipo_contratacion, salario_base,
                                  codigo_facultad, activo=True))
    print("Administrativo creado correctamente.")


def listar_administrativos(admins):
    print("\n--- Administrativos registrados ---")
    if not admins:
        print("(no hay administrativos registrados)")
        return
    for a in admins:
        estado = "Activo" if a.activo else "Inactivo"
        facultad = a.codigo_facultad if a.codigo_facultad else "(nivel central)"
        print(f"{a.identificacion} | {a.nombre_completo} | {a.cargo} | {a.categoria} | "
              f"{a.tipo_contratacion} | Facultad: {facultad} | "
              f"Salario base: ${a.salario_base:,.2f} | {estado}")


def buscar_administrativo(admins, identificacion):
    for a in admins:
        if a.identificacion == identificacion:
            return a
    return None


def modificar_administrativo(admins, identificacion):
    a = buscar_administrativo(admins, identificacion)
    if a is None:
        print("Administrativo no encontrado.")
        return
    nuevo_nombre = input(f"Nuevo nombre ({a.nombre_completo}): ").strip()
    if nuevo_nombre:
        a.nombre_completo = nuevo_nombre
    nuevo_cargo = input(f"Nuevo cargo ({a.cargo}): ").strip()
    if nuevo_cargo:
        a.cargo = nuevo_cargo
    nuevo_salario = input(f"Nuevo salario base ({a.salario_base}): ").strip()
    if nuevo_salario:
        try:
            a.salario_base = float(nuevo_salario)
        except ValueError:
            print("Valor invalido, se mantiene el anterior.")
    print("Administrativo modificado.")


def desactivar_administrativo(admins, identificacion):
    a = buscar_administrativo(admins, identificacion)
    if a is None:
        print("Administrativo no encontrado.")
        return
    a.activo = False
    print("Administrativo desactivado (borrado logico).")


def eliminar_administrativo(admins, identificacion):
    a = buscar_administrativo(admins, identificacion)
    if a is None:
        print("Administrativo no encontrado.")
        return
    admins.remove(a)
    print("Administrativo eliminado permanentemente.")
