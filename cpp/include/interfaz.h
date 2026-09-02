#ifndef INTERFAZ_H
#define INTERFAZ_H

#include <string>

// Borra el contenido visible de la consola.
// Windows usa el comando "cls", Linux/Mac usa "clear" (se resuelve en
// tiempo de compilacion con #ifdef _WIN32, ver interfaz.cpp).
void limpiarPantalla();

// Muestra "Presione ENTER para continuar..." y espera. Se usa SIEMPRE
// antes de limpiar la pantalla, para que el usuario alcance a leer el
// resultado de la operacion (listado, ficha, confirmacion, etc.) antes
// de que se borre.
void pausar();

// Lee un numero entero de forma segura (opcion de menu). Si el usuario
// escribe texto en vez de un numero, no se cuelga: limpia el error y
// devuelve -1 (que no coincide con ningun caso del menu).
int leerOpcion();

// Pregunta algo tipo "(s/n)" y lee la respuesta de un SOLO caracter,
// SIN esperar a que se presione ENTER. Si el caracter no es 's' ni 'n',
// muestra un mensaje de error y vuelve a preguntar (tambien sin ENTER).
// Devuelve 's' o 'n' en minuscula.
char leerSiNo(const std::string& mensaje);

#endif
