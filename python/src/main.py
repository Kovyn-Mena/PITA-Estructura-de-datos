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
    desactivar_administrativo, eliminar_administrativo,
)
from persistencia import (
    guardar_facultades, cargar_facultades,
    guardar_programas, cargar_programas,
    guardar_cursos, cargar_cursos,
    guardar_estudiantes, cargar_estudiantes,
    guardar_profesores, cargar_profesores,
    guardar_administrativos, cargar_administrativos,
)
from interfaz import limpiar_pantalla, pausar, leer_opcion_inmediata, leer_si_no

RUTA_FACULTADES = "../data/facultades.txt"
RUTA_PROGRAMAS = "../data/programas.txt"
RUTA_CURSOS = "../data/cursos.txt"
RUTA_ESTUDIANTES = "../data/estudiantes.txt"
RUTA_MATRICULAS = "../data/matriculas.txt"
RUTA_PROFESORES = "../data/profesores.txt"
RUTA_ADMINISTRATIVOS = "../data/administrativos.txt"


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
        print("6. Ver desglose de nomina")
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
        elif opcion == 0:
            break
        else:
            print("Opcion invalida.")
            pausar()


def main():
    limpiar_pantalla()
    print("=====================================================")
    print(" PITA - Programa Integrado de Transacciones Academicas")
    print(" Universidad Popular del Cesar")
    print("=====================================================")

    facultades = []
    programas = []
    cursos = []
    estudiantes = []
    profesores = []
    administrativos = []

    respuesta = leer_si_no("\nDesea cargar los datos existentes? (s/n): ")
    if respuesta == "s":
        facultades = cargar_facultades(RUTA_FACULTADES)
        programas = cargar_programas(RUTA_PROGRAMAS)
        cursos = cargar_cursos(RUTA_CURSOS)
        estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
        profesores = cargar_profesores(RUTA_PROFESORES)
        administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
        print(f"Datos cargados: {len(facultades)} facultad(es), "
              f"{len(programas)} programa(s), {len(cursos)} curso(s), "
              f"{len(estudiantes)} estudiante(s), {len(profesores)} profesor(es), "
              f"{len(administrativos)} administrativo(s).")
    else:
        print("Iniciando sin datos precargados.")
    pausar()

    opcion = None
    while opcion != 0:
        limpiar_pantalla()
        print("\n===== MENU PRINCIPAL =====")
        print("1. Gestionar Facultades")
        print("2. Gestionar Programas")
        print("3. Gestionar Cursos")
        print("4. Gestionar Estudiantes")
        print("5. Gestionar Profesores")
        print("6. Gestionar Administrativos")
        print("7. Recargar datos desde archivo")
        print("0. Guardar y salir (o presione ENTER)")
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
            menu_administrativos(administrativos, facultades)
        elif opcion == 7:
            if leer_si_no("Se perdera lo que no haya guardado. Continuar? (s/n): ") == "s":
                facultades = cargar_facultades(RUTA_FACULTADES)
                programas = cargar_programas(RUTA_PROGRAMAS)
                cursos = cargar_cursos(RUTA_CURSOS)
                estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
                profesores = cargar_profesores(RUTA_PROFESORES)
                administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
                print(f"Datos recargados desde archivo: {len(facultades)} facultad(es), "
                      f"{len(programas)} programa(s), {len(cursos)} curso(s), "
                      f"{len(estudiantes)} estudiante(s), {len(profesores)} profesor(es), "
                      f"{len(administrativos)} administrativo(s).")
            else:
                print("Operacion cancelada.")
            pausar()
        elif opcion == 0:
            guardar_facultades(facultades, RUTA_FACULTADES)
            guardar_programas(programas, RUTA_PROGRAMAS)
            guardar_cursos(cursos, RUTA_CURSOS)
            guardar_estudiantes(estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS)
            guardar_profesores(profesores, RUTA_PROFESORES)
            guardar_administrativos(administrativos, RUTA_ADMINISTRATIVOS)
            print("Datos guardados. Hasta luego.")
        else:
            print("Opcion no disponible todavia o invalida.")
            pausar()


if __name__ == "__main__":
    main()
