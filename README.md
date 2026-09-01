# PITA — Programa Integrado de Transacciones Académicas
Universidad Popular del Cesar · Estructura de Datos · Taller 1

Grupo: [nombres e iniciales de los integrantes]

## Contenido del proyecto
```
PITA/
├── cpp/            Version en C++
│   ├── include/     Headers (.h): entidades, gestion, nomina, persistencia
│   ├── src/         Implementacion (.cpp) y main.cpp
│   ├── data/        Archivos de datos (texto plano)
│   └── Makefile
├── python/         Version en Python (misma logica y formato de datos)
│   ├── src/         entidades.py, gestion.py, nomina.py, persistencia.py, main.py
│   └── data/        Archivos de datos (texto plano)
└── docs/           Diagrama de diseño y especificación del formato de persistencia
```

## Cómo ejecutar — versión C++

Requisitos: `g++` con soporte C++17 (cualquier instalación estándar de Linux/Mac/WSL sirve).

```bash
cd cpp
make run
```

Esto compila (`make`) y ejecuta (`./pita`) en un solo paso. Si solo quieres compilar:
```bash
make
./pita
```

Para limpiar el binario compilado:
```bash
make clean
```

## Cómo ejecutar — versión Python

Requisitos: Python 3.8 o superior. Sin dependencias externas (solo librería estándar).

```bash
cd python/src
python3 main.py
```

## Uso del programa
1. Al iniciar, el programa pregunta si desea **cargar los datos existentes** desde `data/`
   o **iniciar sin datos**. Se puede responder `s` o `n`.
2. El menú principal permite navegar a la gestión de cada entidad (Facultades, Programas,
   Cursos, Estudiantes, Profesores, Administrativos) y simular el cálculo de nómina.
3. Cada submenú de entidad permite Crear, Listar, Modificar, Desactivar y Eliminar.
4. Al salir (opción `0` del menú principal), los datos se guardan automáticamente en `data/`.

## Datos de prueba
El proyecto se entrega con datos precargados en las carpetas `data/` de cada versión,
para que el profesor pueda probar el sistema sin necesidad de digitar información.

## Documentación de diseño
Ver `docs/formato_persistencia.md` para el detalle del formato de los archivos de datos,
y el documento Word entregado junto con este proyecto para el diseño conceptual completo,
la normatividad aplicada (Decreto 1279 de 2002 y Acuerdo 027 de 2024) y las decisiones
de estructura de datos tomadas.
