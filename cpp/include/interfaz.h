#ifndef INTERFAZ_H
#define INTERFAZ_H

#include <string>

// Borra el contenido visible de la consola.
// Windows usa el comando "cls", Linux/Mac usa "clear" (se resuelve en
// tiempo de compilacion con #ifdef _WIN32, ver interfaz.cpp).
void limpiarPantalla();

// Muestra "Presione una tecla para continuar..." y espera a que el
// usuario presione CUALQUIER tecla (no exige que sea ENTER especificamente).
// Se usa SIEMPRE antes de limpiar la pantalla, para que el usuario alcance
// a leer el resultado de la operacion antes de que se borre.
void pausar();

// Muestra un mensaje y lee UN SOLO digito (0-9) como opcion de menu,
// SIN esperar a que se presione ENTER. Si la tecla no es un digito,
// muestra un mensaje de error y vuelve a preguntar (tambien sin ENTER).
int leerOpcionInmediata(const std::string& mensaje);

// Pregunta algo tipo "(s/n)" y lee la respuesta de un SOLO caracter,
// SIN esperar a que se presione ENTER. Si el caracter no es 's' ni 'n',
// muestra un mensaje de error y vuelve a preguntar (tambien sin ENTER).
// Devuelve 's' o 'n' en minuscula.
char leerSiNo(const std::string& mensaje);

// Muestra un mensaje y lee UNA PALABRA (sin espacios) como respuesta,
// dejando el buffer de entrada limpio para que un getline() posterior
// funcione bien a la primera. Se usa para codigos/identificaciones.
std::string leerPalabra(const std::string& mensaje);

// true si el texto (sin importar mayusculas/minusculas) es "cancelar".
// Se usa junto con leerPalabra() para poder abortar una operacion
// escribiendo esa palabra en vez de un codigo — asi siempre hay una
// forma de "volver atras" sin tener que cerrar el programa.
bool esCancelar(const std::string& texto);

// Lee un numero entero de forma segura (ej. creditos de un curso).
// Si el usuario escribe texto en vez de un numero, no se cuelga: avisa
// del error y vuelve a pedirlo.
int leerEntero();

#endif
