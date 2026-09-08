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

Requisitos: Python 3.8 o superior. Sin dependencias externas (solo librería estándar y Tkinter).

### Interfaz Gráfica (GUI recomendada):
```bash
python python/src/gui.py
```

### Interfaz de Consola:
```bash
cd python/src
python main.py
```

## Uso del programa
1. **Versión Gráfica (`gui.py`):**
   - Sistema interactivo de ventanas tipo escritorio con Dock inferior.
   - Pestañas para Facultades, Programas, Cursos, Estudiantes, Profesores, Administrativos y Nómina.
   - Botón "Ver nómina" en Profesores y Administrativos que abre el **Desprendible Oficial de Pago** institucional (cálculo auditable UPC, deducciones de ley, prestaciones completas, aportes patronales y opción mensual/anual).
2. **Versión C++ (`cpp/`):**
   - Mantiene la misma lógica exacta y almacenamiento de datos.
   - Menú interactivo en consola con opción 6 en Profesores y Administrativos para ver e imprimir el desprendible oficial.
3. Al salir, los datos se conservan sincronizados en las carpetas `data/`.

## Normativa Salarial 2026 Aplicada
- **Docentes de Planta:** Decreto 1279 de 2002 y Decreto 318 de 2026 (Punto salarial: $23.924 COP).
- **Docentes Ocasionales:** Acuerdo UPC 027 de 2024 (Art. 24) sobre SMMLV 2026 ($1.750.905 COP).
- **Docentes Catedráticos:** Acuerdo UPC 027 de 2024 (Art. 23).
- **Personal Administrativo:** Escala Salarial Oficial por Niveles (Nivel 1 al 4) y Decretos Salariales 2026.
- **Seguridad Social y Parafiscales:** Decreto 1990 de 2016 (redondeo a pesos enteros), Salud (4% empleado / 8.5% patronal), Pensión (4% empleado / 12% patronal), Fondo Solidaridad Pensional (1% si $\ge 4$ SMMLV), ARL (0.522%) y Caja Compensación (4%).
- **Prestaciones Sociales:** Prima de Servicios, Cesantías, Intereses de Cesantías (Ley 52/1975), Prima de Navidad, Vacaciones, Prima de Vacaciones y Bonificación por Servicios.

## Documentación de diseño
Ver `docs/formato_persistencia.md` para el detalle del formato de los archivos de datos,
y el documento Word entregado junto con este proyecto para el diseño conceptual completo,
la normatividad aplicada (Decreto 1279 de 2002 y Acuerdo 027 de 2024) y las decisiones
de estructura de datos tomadas.
