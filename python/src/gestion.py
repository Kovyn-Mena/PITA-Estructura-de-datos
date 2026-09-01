"""Funciones de gestion (CRUD) por entidad.
FACULTADES esta completo como patron de referencia; el resto se implementa
siguiendo la misma estructura (Dia 6-7 del cronograma)."""

from entidades import Facultad


# ============================ FACULTADES ============================

def crear_facultad(facultades):
    codigo = input("Codigo facultad: ").strip()
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
# TODO: crear_programa, listar_programas, buscar_programa,
#       modificar_programa, desactivar_programa, eliminar_programa

# ============================ CURSOS ============================
# TODO: mismo patron que Facultad

# ============================ ESTUDIANTES ============================
# TODO: mismo patron + matricular_curso, cancelar_curso
#       (usar Estudiante.calcular_promedio() y esta_en_riesgo_ebra())

# ============================ PROFESORES ============================
# TODO: mismo patron

# ============================ ADMINISTRATIVOS ============================
# TODO: mismo patron
