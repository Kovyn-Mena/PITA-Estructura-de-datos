"""Interfaz de consola: limpiar pantalla, pausas, lectura de opciones sin
ENTER, confirmaciones s/n. Es el equivalente en Python de cpp/src/interfaz.cpp
-- mismas decisiones de diseno, mismo comportamiento para el usuario."""

import os
import sys

# La consola NO se controla igual en todos los sistemas operativos.
# Windows tiene su propia libreria (msvcrt) para leer teclas sueltas;
# Linux/Mac usan la libreria estandar termios/tty para lograr lo mismo.
# Se detecta automaticamente cual esta disponible al importar el modulo.
try:
    import msvcrt
    _ES_WINDOWS = True
except ImportError:
    import termios
    import tty
    _ES_WINDOWS = False


class Colores:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def encabezado_principal():
    print(f"{Colores.CYAN}{Colores.BOLD}"
          f"============================================================\n"
          f"                    PARCIAL 1\n"
          f"              SISTEMA UNIVERSITARIO\n"
          f"============================================================{Colores.RESET}")


def titulo_seccion(titulo):
    print(f"\n{Colores.CYAN}{Colores.BOLD}--- {titulo} ---{Colores.RESET}")


def separador(ancho=60):
    print(f"{Colores.DIM}{'-' * ancho}{Colores.RESET}")


def mensaje_exito(msg):
    print(f"{Colores.GREEN}{Colores.BOLD}[OK] {Colores.RESET}{Colores.GREEN}{msg}{Colores.RESET}")


def mensaje_error(msg):
    print(f"{Colores.RED}{Colores.BOLD}[ERROR] {Colores.RESET}{Colores.RED}{msg}{Colores.RESET}")


def mensaje_info(msg):
    print(f"{Colores.CYAN}[i] {Colores.RESET}{msg}")


def mensaje_alerta(msg):
    print(f"{Colores.YELLOW}{Colores.BOLD}[!] {Colores.RESET}{Colores.YELLOW}{msg}{Colores.RESET}")


def _leer_caracter_inmediato():
    """Lee UN SOLO caracter sin esperar ENTER. Funcion 'privada' de este
    modulo (empieza con _): solo la usan las funciones publicas de aqui abajo."""
    if _ES_WINDOWS and sys.stdin.isatty():
        c = msvcrt.getch().decode("utf-8", errors="ignore")
        print(c, end="", flush=True)  # msvcrt no muestra el caracter, lo mostramos nosotros
        return c
    elif _ES_WINDOWS:
        ch = sys.stdin.read(1)
        return ch if ch else "\n"
    else:
        fd = sys.stdin.fileno()
        try:
            configuracion_original = termios.tcgetattr(fd)
        except termios.error:
            # No hay una terminal real disponible (ej. entrada redirigida
            # desde un archivo, IDE que no da consola interactiva real).
            # Respaldo: leer una linea normal en vez de caerse.
            linea = sys.stdin.readline()
            return linea[0] if linea else "\n"
        try:
            tty.setcbreak(fd)  # desactiva el "modo canonico" (no espera ENTER)
            c = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, configuracion_original)
        return c


def pausar():
    """Espera a que el usuario presione CUALQUIER tecla para continuar."""
    print("\nPresione una tecla para continuar...", end="", flush=True)
    _leer_caracter_inmediato()
    print()


def leer_opcion_menu(mensaje):
    """Lee un caracter de opcion de menu alfanumerico (ej: 0-9, a, r)."""
    while True:
        print(mensaje, end="", flush=True)
        c = _leer_caracter_inmediato()
        print()
        if c in ("\n", "\r", ""):
            return "0"
        if c.isalnum():
            return c.lower()
        print("Opcion invalida. Ingrese una de las opciones mostradas.")


def leer_opcion_inmediata(mensaje):
    """Lee UN SOLO digito (0-9) como opcion de menu, sin esperar ENTER.
    ENTER por si solo se interpreta como 0 (Volver/Salir) — comportamiento
    esperado por instinto."""
    while True:
        print(mensaje, end="", flush=True)
        c = _leer_caracter_inmediato()
        print()
        if c in ("\n", "\r", ""):
            return 0
        if c.isdigit():
            return int(c)
        print("Opcion invalida. Ingrese un numero de las opciones mostradas.")


def leer_si_no(mensaje):
    """Pregunta algo tipo '(s/n)' y lee UN SOLO caracter, sin esperar ENTER.
    Si no es 's' ni 'n', avisa y vuelve a preguntar."""
    while True:
        print(mensaje, end="", flush=True)
        c = _leer_caracter_inmediato().lower()
        print()
        if c in ("s", "n"):
            return c
        print("Opcion invalida. Por favor ingrese 's' o 'n'.")


def leer_palabra(mensaje):
    """Lee una palabra normal (con ENTER, como cualquier input de texto)."""
    return input(mensaje).strip()


def es_cancelar(texto):
    """True si el texto (sin importar mayusculas/minusculas) es 'cancelar'.
    Se usa junto con leer_palabra() para poder abortar una operacion
    escribiendo esa palabra en vez de un codigo."""
    return texto.strip().lower() == "cancelar"


def leer_entero(mensaje=""):
    """Lee un numero entero de forma segura. Si el usuario escribe texto
    en vez de un numero, no se cuelga: avisa y vuelve a pedirlo."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Entrada invalida. Ingrese un numero.")
