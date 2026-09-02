#include "../include/interfaz.h"
#include <iostream>
#include <limits>
#include <cctype>

// La consola NO se controla igual en todos los sistemas operativos.
// Windows tiene sus propias librerias (conio.h) para leer teclas sueltas;
// Linux/Mac usan la libreria POSIX (termios.h) para lograr lo mismo.
// #ifdef _WIN32 elige automaticamente el bloque correcto al compilar,
// segun en que sistema se este compilando el programa.
#ifdef _WIN32
    #include <conio.h>
#else
    #include <termios.h>
    #include <unistd.h>
#endif

using namespace std;

void limpiarPantalla() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pausar() {
    cout << "\nPresione ENTER para continuar...";
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

int leerOpcion() {
    int valor;
    cin >> valor;
    if (cin.fail()) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        return -1; // valor invalido, no coincide con ningun caso del menu
    }
    return valor;
}

// Lee UN SOLO caracter sin esperar ENTER. Es una funcion "privada" de
// este archivo (static): nadie fuera de aqui la necesita directamente,
// solo leerSiNo() la usa internamente.
static char leerCaracterInmediato() {
#ifdef _WIN32
    char c = _getch();       // _getch() de Windows: lee y NO muestra el caracter
    cout << c;                // lo mostramos nosotros para que el usuario vea que escribio
    return c;
#else
    char c;
    termios configuracionOriginal, configuracionNueva;

    tcgetattr(STDIN_FILENO, &configuracionOriginal); // guardar como estaba la terminal
    configuracionNueva = configuracionOriginal;
    configuracionNueva.c_lflag &= ~ICANON;            // desactivar "modo canonico"
    // (modo canonico = la terminal espera ENTER antes de entregar la entrada
    //  al programa; al desactivarlo, cada tecla llega de inmediato)
    tcsetattr(STDIN_FILENO, TCSANOW, &configuracionNueva);

    c = getchar(); // ahora si lee una sola tecla, sin esperar ENTER

    tcsetattr(STDIN_FILENO, TCSANOW, &configuracionOriginal); // restaurar la terminal
    return c;
#endif
}

char leerSiNo(const string& mensaje) {
    char c;
    while (true) {
        cout << mensaje;
        c = static_cast<char>(tolower(leerCaracterInmediato()));
        cout << "\n";
        if (c == 's' || c == 'n') return c;
        cout << "Opcion invalida. Por favor ingrese 's' o 'n'.\n";
    }
}
