"""PITA - Programa Integrado de Transacciones Academicas
Universidad Popular del Cesar
Punto de entrada: ejecutar con `python main.py` desde la carpeta python/src

NOTA DE DISENO (pantalla): cada menu limpia la pantalla ANTES de dibujarse,
y hace pausar() DESPUES de cada accion (excepto "Volver"). Asi el usuario
siempre alcanza a leer el resultado de lo que hizo antes de que la pantalla
se borre para mostrar el menu de nuevo. ENTER por si solo equivale a la
opcion 0 (Volver/Salir).

NOTA DE DISENO (confirmacion): las acciones irreversibles (Eliminar, que es
borrado FISICO) piden confirmacion con leer_si_no() antes de ejecutarse.
Si el usuario responde 'n', la operacion se cancela sin tocar los datos.

Este es el equivalente en Python de cpp/src/main.cpp -- mismas decisiones
de diseno, mismo comportamiento para el usuario, mismo formato de datos.
"""

import os

from gestion import (
    crear_facultad, listar_facultades, modificar_facultad,
    desactivar_facultad, eliminar_facultad, buscar_facultad,
    crear_programa, listar_programas, modificar_programa,
    desactivar_programa, eliminar_programa,
    crear_curso, listar_cursos, modificar_curso,
    desactivar_curso, eliminar_curso,
    crear_estudiante, listar_estudiantes, modificar_estudiante,
    desactivar_estudiante, eliminar_estudiante,
    matricular_curso, cancelar_curso, consultar_estudiante,
    crear_profesor, listar_profesores, modificar_profesor,
    desactivar_profesor, eliminar_profesor, consultar_profesor,
    crear_administrativo, listar_administrativos, modificar_administrativo,
    desactivar_administrativo, eliminar_administrativo, consultar_administrativo,
)
from persistencia import (
    guardar_facultades, cargar_facultades,
    guardar_programas, cargar_programas,
    guardar_cursos, cargar_cursos,
    guardar_estudiantes, cargar_estudiantes,
    guardar_profesores, cargar_profesores,
    guardar_administrativos, cargar_administrativos,
)
from interfaz import (
    limpiar_pantalla, pausar, leer_opcion_inmediata,
    leer_opcion_menu, leer_si_no, leer_palabra, es_cancelar,
    Colores, encabezado_principal, titulo_seccion, separador,
    mensaje_exito, mensaje_error, mensaje_info, mensaje_alerta
)
from generador import (
    menu_generacion_masiva, menu_generacion_horarios,
    consultar_horario_curso, evaluar_erra_masivo,
    generar_datos_masivos, generar_horarios_cursos
)
from nomina import calcular_nomina_masiva

# Rutas ABSOLUTAS calculadas a partir de la ubicacion de este archivo, para
# que el programa funcione sin importar desde que carpeta se ejecute
# (ej. python3 python/src/main.py desde la raiz del proyecto tambien funciona).
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "..", "data")

RUTA_FACULTADES = os.path.join(_DATA_DIR, "facultades.txt")
RUTA_PROGRAMAS = os.path.join(_DATA_DIR, "programas.txt")
RUTA_CURSOS = os.path.join(_DATA_DIR, "cursos.txt")
RUTA_ESTUDIANTES = os.path.join(_DATA_DIR, "estudiantes.txt")
RUTA_MATRICULAS = os.path.join(_DATA_DIR, "matriculas.txt")
RUTA_PROFESORES = os.path.join(_DATA_DIR, "profesores.txt")
RUTA_ADMINISTRATIVOS = os.path.join(_DATA_DIR, "administrativos.txt")


def menu_facultades(facultades):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Facultades ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_facultad(facultades)
            pausar()
        elif opcion == 2:
            listar_facultades(facultades)
            pausar()
        elif opcion == 3:
            codigo = input("Codigo a modificar: ").strip()
            modificar_facultad(facultades, codigo)
            pausar()
        elif opcion == 4:
            codigo = input("Codigo a desactivar: ").strip()
            desactivar_facultad(facultades, codigo)
            pausar()
        elif opcion == 5:
            codigo = input("Codigo a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_facultad(facultades, codigo)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_programas(programas, facultades):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Programas ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_programa(programas, facultades)
            pausar()
        elif opcion == 2:
            listar_programas(programas)
            pausar()
        elif opcion == 3:
            codigo = input("Codigo a modificar: ").strip()
            modificar_programa(programas, codigo)
            pausar()
        elif opcion == 4:
            codigo = input("Codigo a desactivar: ").strip()
            desactivar_programa(programas, codigo)
            pausar()
        elif opcion == 5:
            codigo = input("Codigo a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_programa(programas, codigo)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_cursos(cursos, programas):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Cursos ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("6. Generar horarios academicos")
        print("7. Consultar horario de curso")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_curso(cursos, programas)
            pausar()
        elif opcion == 2:
            listar_cursos(cursos)
            pausar()
        elif opcion == 3:
            codigo = input("Codigo a modificar: ").strip()
            modificar_curso(cursos, codigo)
            pausar()
        elif opcion == 4:
            codigo = input("Codigo a desactivar: ").strip()
            desactivar_curso(cursos, codigo)
            pausar()
        elif opcion == 5:
            codigo = input("Codigo a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_curso(cursos, codigo)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 6:
            menu_generacion_horarios(cursos, RUTA_CURSOS)
            pausar()
        elif opcion == 7:
            consultar_curso_ficha(cursos)
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_estudiantes(estudiantes, programas, cursos):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Estudiantes ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("6. Matricular curso\n7. Cancelar curso\n8. Ver ficha (promedio + alerta EBRA)")
        print("9. Evaluacion ERRA masiva (Parcial 1)")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_estudiante(estudiantes, programas)
            pausar()
        elif opcion == 2:
            listar_estudiantes(estudiantes)
            pausar()
        elif opcion == 3:
            identificacion = input("Identificacion a modificar: ").strip()
            modificar_estudiante(estudiantes, identificacion)
            pausar()
        elif opcion == 4:
            identificacion = input("Identificacion a desactivar: ").strip()
            desactivar_estudiante(estudiantes, identificacion)
            pausar()
        elif opcion == 5:
            identificacion = input("Identificacion a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_estudiante(estudiantes, identificacion)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 6:
            identificacion = input("Identificacion del estudiante: ").strip()
            matricular_curso(estudiantes, identificacion, cursos)
            pausar()
        elif opcion == 7:
            identificacion = input("Identificacion del estudiante: ").strip()
            cancelar_curso(estudiantes, identificacion)
            pausar()
        elif opcion == 8:
            identificacion = input("Identificacion del estudiante: ").strip()
            consultar_estudiante(estudiantes, identificacion)
            pausar()
        elif opcion == 9:
            evaluar_erra_masivo(estudiantes)
            pausar()
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_profesores(profesores, programas):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Profesores ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("6. Ver desglose individual de nomina")
        print("7. Calcular nomina universitaria masiva")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_profesor(profesores, programas)
            pausar()
        elif opcion == 2:
            listar_profesores(profesores)
            pausar()
        elif opcion == 3:
            identificacion = input("Identificacion a modificar: ").strip()
            modificar_profesor(profesores, identificacion)
            pausar()
        elif opcion == 4:
            identificacion = input("Identificacion a desactivar: ").strip()
            desactivar_profesor(profesores, identificacion)
            pausar()
        elif opcion == 5:
            identificacion = input("Identificacion a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_profesor(profesores, identificacion)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 6:
            identificacion = input("Identificacion del profesor: ").strip()
            consultar_profesor(profesores, identificacion)
            pausar()
        elif opcion == 7:
            calcular_nomina_masiva(profesores)
            pausar()
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_administrativos(admins, facultades):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n--- Menu Administrativos ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar")
        print("6. Ver liquidacion de nomina")
        print("0. Volver (o presione ENTER)")
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            crear_administrativo(admins, facultades)
            pausar()
        elif opcion == 2:
            listar_administrativos(admins)
            pausar()
        elif opcion == 3:
            identificacion = input("Identificacion a modificar: ").strip()
            modificar_administrativo(admins, identificacion)
            pausar()
        elif opcion == 4:
            identificacion = input("Identificacion a desactivar: ").strip()
            desactivar_administrativo(admins, identificacion)
            pausar()
        elif opcion == 5:
            identificacion = input("Identificacion a eliminar: ").strip()
            if leer_si_no("Esta accion NO se puede deshacer. Confirma? (s/n): ") == "s":
                eliminar_administrativo(admins, identificacion)
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 6:
            identificacion = input("Identificacion del administrativo: ").strip()
            consultar_administrativo(admins, identificacion)
            pausar()
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def menu_gestion_avanzada(facultades, programas, cursos, estudiantes, profesores, admins):
    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        titulo_seccion("MODULOS DE GESTION CLASICA (CRUD)")
        print("1. Gestionar Facultades")
        print("2. Gestionar Programas")
        print("3. Gestionar Cursos")
        print("4. Gestionar Estudiantes")
        print("5. Gestionar Profesores")
        print("6. Gestionar Administrativos")
        print("0. Volver al menu principal (o presione ENTER)")
        separador()
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            menu_facultades(facultades)
        elif opcion == 2:
            menu_programas(programas, facultades)
        elif opcion == 3:
            menu_cursos(cursos, programas)
        elif opcion == 4:
            menu_estudiantes(estudiantes, programas, cursos)
        elif opcion == 5:
            menu_profesores(profesores, programas)
        elif opcion == 6:
            menu_administrativos(admins, facultades)
        elif opcion == 0:
            break
        else:
            mensaje_error("Opcion invalida.")
            pausar()


def mostrar_estadisticas_universitarias(fac, prog, cur, est, prof):
    print("\n------------------------------------------------------------")
    print("                 ESTADISTICAS UNIVERSIDAD                   ")
    print("------------------------------------------------------------")
    print(f"{'Facultades':<35} {len(fac):>15,}")
    print(f"{'Programas academicos':<35} {len(prog):>15,}")
    print(f"{'Estudiantes registrados':<35} {len(est):>15,}")
    print(f"{'Profesores registrados':<35} {len(prof):>15,}")
    print(f"{'Cursos / Asignaturas':<35} {len(cur):>15,}")
    print("------------------------------------------------------------")


def consultar_estudiante_ficha(estudiantes):
    if not estudiantes:
        mensaje_alerta("No hay estudiantes cargados en el sistema.")
        pausar()
        return
    opcion = None
    while opcion != 0 and opcion != 5:
        limpiar_pantalla()
        titulo_seccion("CONSULTA DE FICHA DE ESTUDIANTE")
        print("1. Buscar por identificacion")
        print("2. Mostrar estudiante aleatorio")
        print("3. Mostrar estudiante en riesgo ERRA")
        print("4. Mostrar estudiante sin riesgo ERRA")
        print("5. Volver (o presione ENTER)")
        separador()
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            identificacion = leer_palabra("Ingrese identificacion del estudiante (o 'cancelar' para volver): ")
            if not es_cancelar(identificacion) and identificacion:
                consultar_estudiante(estudiantes, identificacion)
            pausar()
        elif opcion == 2:
            est = random.choice(estudiantes)
            mensaje_info(f"Mostrando ficha del estudiante aleatorio (ID: {est.identificacion}):")
            consultar_estudiante(estudiantes, est.identificacion)
            pausar()
        elif opcion == 3:
            id_ejemplo = None
            for est in estudiantes:
                if getattr(est, "activo", True) and est.esta_en_riesgo_ebra():
                    id_ejemplo = est.identificacion
                    break
            if id_ejemplo:
                mensaje_info(f"Mostrando ficha de estudiante en riesgo ERRA (ID: {id_ejemplo}):")
                consultar_estudiante(estudiantes, id_ejemplo)
            else:
                mensaje_alerta("No se encontro ningun estudiante en riesgo ERRA en memoria.")
            pausar()
        elif opcion == 4:
            id_ejemplo = None
            for est in estudiantes:
                if getattr(est, "activo", True) and getattr(est, "matriculas", []) and not est.esta_en_riesgo_ebra():
                    id_ejemplo = est.identificacion
                    break
            if id_ejemplo:
                mensaje_info(f"Mostrando ficha de estudiante sin riesgo ERRA (ID: {id_ejemplo}):")
                consultar_estudiante(estudiantes, id_ejemplo)
            else:
                mensaje_alerta("No se encontro ningun estudiante con promedio satisfactorio en memoria.")
            pausar()
        elif opcion == 5 or opcion == 0:
            break
        else:
            mensaje_error("Opcion invalida.")
            pausar()


def mostrar_ficha_curso_detallada(c):
    print("\n=======================================================")
    print(f"FICHA DE ASIGNATURA - {c.codigo}")
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


def listar_cursos_muestra(cursos, max_count=10):
    muestra = cursos[:max_count]
    print(f"\n--- MUESTRA REPRESENTATIVA DE CURSOS ({len(muestra)} Asignaturas) ---")
    print(f"{'Codigo':<10} {'Nombre Asignatura':<33} {'Programa':<10} {'Profesor':<12} {'Dia':<12} {'Horario':<15} {'Salon':<10}")
    print("-" * 102)
    for c in muestra:
        franja = f"{c.hora_inicio}:00-{c.hora_fin}:00" if getattr(c, "hora_inicio", 0) > 0 else "Sin horario"
        dia_str = getattr(c, "dia", "") or "N/A"
        sal_str = getattr(c, "salon", "") or "N/A"
        nom = (c.nombre[:31] + "..") if len(c.nombre) > 33 else c.nombre
        print(f"{c.codigo:<10} {nom:<33} {c.codigo_programa:<10} {c.codigo_profesor:<12} {dia_str:<12} {franja:<15} {sal_str:<10}")


def consultar_curso_ficha(cursos):
    if not cursos:
        mensaje_alerta("No hay cursos registrados en el sistema.")
        pausar()
        return
    opcion = None
    while opcion != 0 and opcion != 5:
        limpiar_pantalla()
        titulo_seccion("CONSULTA DE CURSO / HORARIOS")
        print("1. Buscar por codigo")
        print("2. Mostrar curso aleatorio")
        print("3. Mostrar curso con horario")
        print("4. Listar cursos de ejemplo")
        print("5. Volver (o presione ENTER)")
        separador()
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            codigo = leer_palabra("Ingrese codigo del curso (o 'cancelar' para volver): ")
            if not es_cancelar(codigo) and codigo:
                encontrado = None
                for c in cursos:
                    if c.codigo.upper() == codigo.upper():
                        encontrado = c
                        break
                if encontrado:
                    mostrar_ficha_curso_detallada(encontrado)
                else:
                    mensaje_alerta(f"Curso con codigo {codigo} no encontrado.")
            pausar()
        elif opcion == 2:
            c = random.choice(cursos)
            mensaje_info(f"Mostrando ficha de curso aleatorio (Codigo: {c.codigo}):")
            mostrar_ficha_curso_detallada(c)
            pausar()
        elif opcion == 3:
            c_horario = None
            for c in cursos:
                if getattr(c, "activo", True) and getattr(c, "hora_inicio", 0) > 0:
                    c_horario = c
                    break
            if c_horario:
                mensaje_info(f"Mostrando ficha de curso con horario programado (Codigo: {c_horario.codigo}):")
                mostrar_ficha_curso_detallada(c_horario)
            else:
                mensaje_alerta("No se encontro ningun curso con horario asignado en memoria.")
            pausar()
        elif opcion == 4:
            listar_cursos_muestra(cursos, 10)
            pausar()
        elif opcion == 5 or opcion == 0:
            break
        else:
            mensaje_error("Opcion invalida.")
            pausar()


import random


def consultar_profesor_ficha(profesores):
    if not profesores:
        mensaje_alerta("No hay profesores cargados en el sistema.")
        pausar()
        return
    opcion = None
    while opcion != 0 and opcion != 6:
        limpiar_pantalla()
        titulo_seccion("CONSULTA DE FICHA Y LIQUIDACION DE PROFESOR")
        print("1. Buscar por identificacion")
        print("2. Mostrar profesor de planta")
        print("3. Mostrar profesor ocasional")
        print("4. Mostrar profesor catedratico")
        print("5. Mostrar profesor aleatorio")
        print("6. Volver (o presione ENTER)")
        separador()
        opcion = leer_opcion_inmediata("Opcion: ")

        if opcion == 1:
            identificacion = leer_palabra("Ingrese identificacion del profesor (o 'cancelar' para volver): ")
            if not es_cancelar(identificacion) and identificacion:
                consultar_profesor(profesores, identificacion)
            pausar()
        elif opcion == 2:
            id_ejemplo = None
            for prof in profesores:
                if getattr(prof, "activo", True) and prof.tipo_vinculacion == "Planta":
                    id_ejemplo = prof.identificacion
                    break
            if id_ejemplo:
                mensaje_info(f"Mostrando ficha de profesor de Planta (ID: {id_ejemplo}):")
                consultar_profesor(profesores, id_ejemplo)
            else:
                mensaje_alerta("No se encontro ningun profesor de Planta en memoria.")
            pausar()
        elif opcion == 3:
            id_ejemplo = None
            for prof in profesores:
                if getattr(prof, "activo", True) and prof.tipo_vinculacion == "Ocasional":
                    id_ejemplo = prof.identificacion
                    break
            if id_ejemplo:
                mensaje_info(f"Mostrando ficha de profesor Ocasional (ID: {id_ejemplo}):")
                consultar_profesor(profesores, id_ejemplo)
            else:
                mensaje_alerta("No se encontro ningun profesor Ocasional en memoria.")
            pausar()
        elif opcion == 4:
            id_ejemplo = None
            for prof in profesores:
                if getattr(prof, "activo", True) and prof.tipo_vinculacion == "Catedratico":
                    id_ejemplo = prof.identificacion
                    break
            if id_ejemplo:
                mensaje_info(f"Mostrando ficha de profesor Catedratico (ID: {id_ejemplo}):")
                consultar_profesor(profesores, id_ejemplo)
            else:
                mensaje_alerta("No se encontro ningun profesor Catedratico en memoria.")
            pausar()
        elif opcion == 5:
            prof = random.choice(profesores)
            mensaje_info(f"Mostrando ficha de profesor aleatorio (ID: {prof.identificacion}):")
            consultar_profesor(profesores, prof.identificacion)
            pausar()
        elif opcion == 6 or opcion == 0:
            break
        else:
            mensaje_error("Opcion invalida.")
            pausar()


def ejecutar_proceso_completo(
    facultades, programas, cursos, estudiantes, profesores,
    ruta_facultades, ruta_programas, ruta_cursos,
    ruta_estudiantes, ruta_matriculas, ruta_profesores
):
    limpiar_pantalla()
    encabezado_principal()
    titulo_seccion("EJECUCION DEL PROCESO COMPLETO (PARCIAL 1)")
    print("Este proceso ejecutara de forma integrada y secuencial:")
    print("  1. Generacion masiva (10 Fac, 150 Prog, 9k Prof, 7.5k Cur, 225k Est)")
    print("  2. Estadisticas consolidadas")
    print("  3. Asignacion de horarios libres de conflicto")
    print("  4. Calculo masivo de nomina")
    print("  5. Evaluacion de riesgo academico (ERRA)")
    print("  6. Guardado y persistencia en disco\n")

    if leer_si_no("Desea iniciar la ejecucion del proceso completo? (s/n): ") != "s":
        mensaje_info("Operacion cancelada por el usuario.")
        return

    import time
    t0 = time.time()

    # 1. Generacion
    titulo_seccion("1. GENERACION MASIVA DE ESTRUCTURA UNIVERSITARIA")
    nuevas_fac, nuevos_prog, nuevos_prof, nuevos_cur, nuevos_est = generar_datos_masivos()
    facultades.clear(); facultades.extend(nuevas_fac)
    programas.clear(); programas.extend(nuevos_prog)
    profesores.clear(); profesores.extend(nuevos_prof)
    cursos.clear(); cursos.extend(nuevos_cur)
    estudiantes.clear(); estudiantes.extend(nuevos_est)
    mensaje_exito("Generacion masiva completada con exito.")

    # 2. Estadisticas
    titulo_seccion("2. ESTADISTICAS CONSOLIDADAS")
    mostrar_estadisticas_universitarias(facultades, programas, cursos, estudiantes, profesores)

    # 3. Horarios
    titulo_seccion("3. GENERACION DE HORARIOS ACADEMICOS")
    asignados = generar_horarios_cursos(cursos)
    mensaje_exito(f"{asignados:,} materias con horario asignado (0 conflictos).")

    # 4. Nomina
    titulo_seccion("4. CALCULO DE NOMINA UNIVERSITARIA")
    calcular_nomina_masiva(profesores)

    # 5. ERRA
    titulo_seccion("5. EVALUACION DE RIESGO ACADEMICO (ERRA)")
    evaluar_erra_masivo(estudiantes)

    # 6. Persistencia
    titulo_seccion("6. GUARDADO Y PERSISTENCIA")
    guardar_facultades(facultades, ruta_facultades)
    guardar_programas(programas, ruta_programas)
    guardar_profesores(profesores, ruta_profesores)
    guardar_cursos(cursos, ruta_cursos)
    guardar_estudiantes(estudiantes, ruta_estudiantes, ruta_matriculas)
    mensaje_exito("Archivos en carpeta data/ actualizados correctamente.")

    dur = time.time() - t0
    separador()
    print(f"{Colores.GREEN}{Colores.BOLD}>>> PROCESO COMPLETO FINALIZADO EXITOSAMENTE EN {dur:.2f} SEGUNDOS <<<{Colores.RESET}")
    separador()


def main():
    limpiar_pantalla()
    encabezado_principal()

    facultades = []
    programas = []
    cursos = []
    estudiantes = []
    profesores = []
    administrativos = []

    respuesta = leer_si_no("\nDesea cargar los datos existentes? (s/n): ")
    if respuesta == "s":
        print("\nCargando datos desde persistencia...")
        facultades = cargar_facultades(RUTA_FACULTADES)
        programas = cargar_programas(RUTA_PROGRAMAS)
        cursos = cargar_cursos(RUTA_CURSOS)
        estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
        profesores = cargar_profesores(RUTA_PROFESORES)
        administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
        mensaje_exito(f"Datos cargados correctamente: {len(facultades)} facultades, "
                      f"{len(programas)} programas, {len(cursos)} cursos, "
                      f"{len(estudiantes):,} estudiantes, {len(profesores):,} profesores.")
    else:
        mensaje_info("Iniciando sin datos precargados.")
    pausar()

    opcion = None
    while opcion != "0":
        limpiar_pantalla()
        encabezado_principal()
        print(f"{Colores.CYAN}{Colores.BOLD}===== MENU PRINCIPAL - PARCIAL 1 ====={Colores.RESET}")
        print("1. Generar universidad (10 Fac, 150 Prog, 9k Prof, 7.5k Cur, 225k Est)")
        print("2. Ver estadisticas de la universidad")
        print("3. Calcular nomina universitaria masiva")
        print("4. Generar y verificar horarios academicos")
        print("5. Analizar riesgo academico (ERRA)")
        print("6. Consultar estudiante (Ficha y promedio)")
        print("7. Consultar profesor (Ficha y liquidacion)")
        print("8. Consultar curso (Ficha y horarios)")
        print("9. Ejecutar proceso completo (Flujo integrado Parcial 1)")
        print("A. Gestion avanzada / Modulos clasicos (CRUD)")
        print("R. Recargar datos desde archivo")
        print("0. Guardar y salir (o presione ENTER)")
        separador()
        opcion = leer_opcion_menu("Seleccione una opcion: ")

        if opcion == "1":
            menu_generacion_masiva(
                facultades, programas, cursos, estudiantes, profesores,
                RUTA_FACULTADES, RUTA_PROGRAMAS, RUTA_CURSOS,
                RUTA_ESTUDIANTES, RUTA_MATRICULAS, RUTA_PROFESORES
            )
            pausar()
        elif opcion == "2":
            mostrar_estadisticas_universitarias(facultades, programas, cursos, estudiantes, profesores)
            pausar()
        elif opcion == "3":
            calcular_nomina_masiva(profesores)
            pausar()
        elif opcion == "4":
            menu_generacion_horarios(cursos, RUTA_CURSOS)
            pausar()
        elif opcion == "5":
            evaluar_erra_masivo(estudiantes)
            pausar()
        elif opcion == "6":
            consultar_estudiante_ficha(estudiantes)
        elif opcion == "7":
            consultar_profesor_ficha(profesores)
        elif opcion == "8":
            consultar_curso_ficha(cursos)
        elif opcion == "9":
            ejecutar_proceso_completo(
                facultades, programas, cursos, estudiantes, profesores,
                RUTA_FACULTADES, RUTA_PROGRAMAS, RUTA_CURSOS,
                RUTA_ESTUDIANTES, RUTA_MATRICULAS, RUTA_PROFESORES
            )
            pausar()
        elif opcion == "a":
            menu_gestion_avanzada(facultades, programas, cursos, estudiantes, profesores, administrativos)
        elif opcion == "r":
            if leer_si_no("Se perdera lo que no haya guardado. Continuar? (s/n): ") == "s":
                print("\nRecargando datos desde disco...")
                facultades = cargar_facultades(RUTA_FACULTADES)
                programas = cargar_programas(RUTA_PROGRAMAS)
                cursos = cargar_cursos(RUTA_CURSOS)
                estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
                profesores = cargar_profesores(RUTA_PROFESORES)
                administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
                mensaje_exito(f"Datos recargados desde archivo: {len(facultades)} facultades, "
                              f"{len(programas)} programas, {len(cursos)} cursos, "
                              f"{len(estudiantes):,} estudiantes, {len(profesores):,} profesores.")
            else:
                mensaje_info("Operacion cancelada.")
            pausar()
        elif opcion == "0":
            print("\nGuardando datos en disco...")
            guardar_facultades(facultades, RUTA_FACULTADES)
            guardar_programas(programas, RUTA_PROGRAMAS)
            guardar_cursos(cursos, RUTA_CURSOS)
            guardar_estudiantes(estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS)
            guardar_profesores(profesores, RUTA_PROFESORES)
            guardar_administrativos(administrativos, RUTA_ADMINISTRATIVOS)
            mensaje_exito("Todos los datos fueron guardados exitosamente. Hasta luego.")
        else:
            mensaje_error("Opcion no disponible o invalida.")
            pausar()


if __name__ == "__main__":
    main()
