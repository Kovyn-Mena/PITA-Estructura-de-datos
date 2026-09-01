"""PITA - Programa Integrado de Transacciones Academicas
Universidad Popular del Cesar
Punto de entrada: ejecutar con `python main.py` desde la carpeta python/src
"""

from entidades import Profesor
from gestion import (
    crear_facultad, listar_facultades, modificar_facultad,
    desactivar_facultad, eliminar_facultad
)
from persistencia import guardar_facultades, cargar_facultades
from nomina import imprimir_desglose_nomina

RUTA_FACULTADES = "../data/facultades.txt"
# TODO: agregar rutas de los demas archivos de datos a medida que se implementen.


def menu_facultades(facultades):
    opcion = None
    while opcion != "0":
        print("\n--- Menu Facultades ---")
        print("1. Crear\n2. Listar\n3. Modificar\n4. Desactivar\n5. Eliminar\n0. Volver")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            crear_facultad(facultades)
        elif opcion == "2":
            listar_facultades(facultades)
        elif opcion == "3":
            codigo = input("Codigo a modificar: ").strip()
            modificar_facultad(facultades, codigo)
        elif opcion == "4":
            codigo = input("Codigo a desactivar: ").strip()
            desactivar_facultad(facultades, codigo)
        elif opcion == "5":
            codigo = input("Codigo a eliminar: ").strip()
            eliminar_facultad(facultades, codigo)
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def demo_nomina():
    # Profesor de ejemplo para probar el modulo de nomina mientras se
    # conecta con la gestion real de profesores.
    demo = Profesor(
        identificacion="DEMO",
        nombre_completo="Profesor de ejemplo",
        codigo_programa="SIS",
        tipo_vinculacion="Planta",
        dedicacion="TiempoCompleto",
        categoria_escalafon="Asociado",
        anios_experiencia=8,
        puntos_titulos=60,
        puntos_productividad=15,
    )
    imprimir_desglose_nomina(demo)


def main():
    print("=====================================================")
    print(" PITA - Programa Integrado de Transacciones Academicas")
    print(" Universidad Popular del Cesar")
    print("=====================================================")

    facultades = []

    respuesta = input("\nDesea cargar los datos existentes? (s/n): ").strip().lower()
    if respuesta == "s":
        facultades = cargar_facultades(RUTA_FACULTADES)
        print(f"Datos cargados: {len(facultades)} facultad(es).")
    else:
        print("Iniciando sin datos precargados.")

    opcion = None
    while opcion != "0":
        print("\n===== MENU PRINCIPAL =====")
        print("1. Gestionar Facultades")
        print("2. Gestionar Programas       [TODO]")
        print("3. Gestionar Cursos          [TODO]")
        print("4. Gestionar Estudiantes     [TODO]")
        print("5. Gestionar Profesores      [TODO]")
        print("6. Gestionar Administrativos [TODO]")
        print("7. Simular nomina de un profesor (demo)")
        print("0. Guardar y salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            menu_facultades(facultades)
        elif opcion == "7":
            demo_nomina()
        elif opcion == "0":
            guardar_facultades(facultades, RUTA_FACULTADES)
            print("Datos guardados. Hasta luego.")
        else:
            print("Opcion no disponible todavia o invalida.")


if __name__ == "__main__":
    main()
