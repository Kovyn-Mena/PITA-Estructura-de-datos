#ifndef INTERFAZ_H
#define INTERFAZ_H

#include <string>

// Colores ANSI para terminal profesional
namespace Colores {
    const std::string RESET   = "\033[0m";
    const std::string BOLD    = "\033[1m";
    const std::string DIM     = "\033[2m";
    const std::string CYAN    = "\033[36m";
    const std::string GREEN   = "\033[32m";
    const std::string YELLOW  = "\033[33m";
    const std::string RED     = "\033[31m";
    const std::string BLUE    = "\033[34m";
    const std::string MAGENTA = "\033[35m";
}

// Inicializa soporte para colores ANSI (VT100) en Windows
void habilitarColoresTerminal();

// Borra el contenido visible de la consola.
void limpiarPantalla();

// Muestra "Presione una tecla para continuar..." y espera cualquier tecla.
void pausar();

// Componentes visuales de presentacion
void encabezadoPrincipal();
void tituloSeccion(const std::string& titulo);
void separador(int ancho = 60);
void mensajeExito(const std::string& msg);
void mensajeError(const std::string& msg);
void mensajeInfo(const std::string& msg);
void mensajeAlerta(const std::string& msg);

// Lectura de opciones y teclado
char leerOpcionMenu(const std::string& mensaje);
int leerOpcionInmediata(const std::string& mensaje);
char leerSiNo(const std::string& mensaje);
std::string leerPalabra(const std::string& mensaje);
bool esCancelar(const std::string& texto);
int leerEntero();
float leerFlotante();

#endif

