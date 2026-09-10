#include "../include/interfaz.h"
#include <iostream>
#include <cctype>
#include <limits>

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

// Lee UN SOLO caracter sin esperar ENTER. Es una funcion "privada" de
// este archivo (static): solo la usan las funciones publicas de aqui abajo.
static char leerCaracterInmediato() {
#ifdef _WIN32
    char c = _getch();       // _getch() de Windows: lee y NO muestra el caracter
    cout << c;                 // lo mostramos nosotros para que el usuario vea que escribio
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

    c = getchar(); // lee una sola tecla, sin esperar ENTER

    // Si el usuario presiono una tecla extra por costumbre (ej. ENTER
    // despues de "s"), esa tecla queda esperando sin usarse. Se descarta
    // aqui para que no interfiera con la siguiente lectura del programa.
    tcflush(STDIN_FILENO, TCIFLUSH);

    tcsetattr(STDIN_FILENO, TCSANOW, &configuracionOriginal); // restaurar la terminal
    return c;
#endif
}

void pausar() {
    cout << "\nPresione una tecla para continuar...";
    leerCaracterInmediato(); // NO importa cual tecla sea, cualquiera continua
    cout << "\n";
}

int leerOpcionInmediata(const string& mensaje) {
    char c;
    while (true) {
        cout << mensaje;
        c = leerCaracterInmediato();
        cout << "\n";
        if (c == '\n' || c == '\r') {
            // ENTER por si solo se interpreta como "Volver"/"Salir" (opcion 0).
            // Es el comportamiento que la mayoria espera por instinto.
            return 0;
        }
        if (isdigit(static_cast<unsigned char>(c))) {
            return c - '0'; // convierte el caracter '0'-'9' al numero real
        }
        cout << "Opcion invalida. Ingrese un numero de las opciones mostradas.\n";
    }
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

string leerPalabra(const string& mensaje) {
    string palabra;
    cout << mensaje;
    cin >> palabra;
    // Deja el buffer limpio (sin '\n' pendiente) para que un getline()
    // que venga despues no se salte una linea por error.
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    return palabra;
}

bool esCancelar(const string& texto) {
    string copia = texto;
    for (auto& c : copia) c = static_cast<char>(tolower(static_cast<unsigned char>(c)));
    return copia == "cancelar";
}

int leerEntero() {
    int valor;
    while (true) {
        cin >> valor;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Entrada invalida. Ingrese un numero entero: ";
            continue;
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        return valor;
    }
}

float leerFlotante() {
    float valor;
    while (true) {
        cin >> valor;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Entrada invalida. Ingrese una nota valida (ej. 3.5): ";
            continue;
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        return valor;
    }
}
