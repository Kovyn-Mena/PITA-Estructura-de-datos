# PITA — Programa Integrado de Transacciones Académicas
**Universidad Popular del Cesar (UPC)** · Estructura de Datos · **Parcial 1**

---

## 🏛️ Descripción General

**PITA** es una plataforma universitaria de alto rendimiento diseñada e implementada en **C++ (C++17)** y **Python (3.8+)**. El sistema administra y procesa el flujo completo de una universidad masiva con más de **1.000.000 de registros** interconectados en memoria y persistencia en texto plano delimitado por tuberías (|).

### 📊 Datos Masivos de la Universidad
- **10 Facultades** (FAC01 a FAC10)
- **150 Programas Académicos** (15 programas por facultad)
- **9.000 Profesores** (60 profesores por programa: Planta, Ocasionales y Cátedra)
- **7.500 Cursos / Asignaturas** (50 asignaturas por programa)
- **225.000 Estudiantes** (1.500 estudiantes por programa)
- **~750.000+ Matrículas y Calificaciones** (3 a 4 materias por estudiante activo)

---

## ✨ Funcionalidades Principales (Parcial 1)

1. **Generación Automática y Aleatoria:** Creación determinista y reproducible de la universidad completa con guardado rápido en disco.
2. **Cálculo Masivo de Nómina Docente:** Liquidación oficial auditada bajo normatividad colombiana vigente:
   - **Planta:** Decreto 1279 de 2002 y Decreto 318 de 2026 (Puntos salariales, bonificación de dirección, primas semestrales, vacaciones, aportes PILA y patronales).
   - **Ocasionales:** Acuerdo UPC 027 de 2024 (Art. 24) sobre SMMLV 2026 (.750.905 COP) con bonificación de posgrado (Especialización, Maestría, Doctorado).
   - **Cátedra:** Acuerdo UPC 027 de 2024 (Art. 23) según cualificación docente.
3. **Generación de Horarios Libres de Conflicto:**
   - 42 franjas semanales (Lunes a Sábado, bloques de 2 horas entre 06:00 y 22:00) y 400 salones (Edificios A-J, 4 pisos).
   - Algoritmo de bitmasks con **0 colisiones de docente y 0 colisiones de aula** para 7.500 asignaturas.
4. **Evaluación Masiva ERRA / EBRA:**
   - Evaluación institucional según la regla de promedio acumulado < 3.25.
   - Reporte consolidado con porcentaje en riesgo, porcentaje satisfactorio y promedio institucional.
5. **Navegación Autosuficiente en Terminal (UX):**
   - Sugerencias dinámicas con identificadores reales disponibles en memoria (ID estudiante, ID profesor, Código curso).
   - Consultas rápidas por categoría (ejemplos, estudiantes en riesgo/sin riesgo, profesores por vinculación, cursos con horario y muestra tabular de 10 asignaturas).
   - Control seguro de datos vacíos.

---

## 📁 Estructura del Proyecto

```text
PITA/
├── cpp/                     # Implementación en C++17
│   ├── include/             # Encabezados (.h): entidades, generador, gestion, interfaz, nomina, persistencia
│   ├── src/                 # Implementación (.cpp): generador, gestion, interfaz, main, nomina, persistencia
│   ├── data/                # Archivos de datos de respaldo
│   └── Makefile             # Automatización de compilación
├── python/                  # Implementación en Python 3.8+
│   ├── src/                 # Módulos (.py): entidades, generador, gestion, gui, interfaz, main, nomina, persistencia
│   └── data/                # Archivos de persistencia en texto plano
├── data/                    # Persistencia compartida e intercambiable
├── docs/                    # Documentación técnica y especificaciones
│   ├── DOCUMENTACION_PARCIAL_1.md  # Documentación maestra y detallada del Parcial 1
│   └── formato_persistencia.md     # Estructura del formato delimitado por '|'
└── README.md                # Este documento
```

---

## 🚀 Instrucciones de Ejecución

### 1. Versión C++ (Consola Interactiva)
Requisitos: g++ con soporte C++17.

```bash
# Compilar y enlazar
g++ -std=c++17 -Wall -O2 -Icpp/include cpp/src/*.cpp -o cpp/pita.exe

# Ejecutar
./cpp/pita.exe
```

*Opcional con Makefile:*
```bash
cd cpp
make run
```

### 2. Versión Python (Consola Interactiva)
Requisitos: Python 3.8+.

```bash
# Validación de sintaxis
python -m py_compile python/src/*.py

# Ejecutar menú de consola
python python/src/main.py
```

### 3. Versión Gráfica Python (GUI)
```bash
python python/src/gui.py
```

---

## 📖 Documentación Detallada
Para consultar el análisis de complejidad algorítmica, comparativa de consumo de memoria RAM, tiempos de respuesta y desglose normativo, consulta:
- [Documentación Técnica del Parcial 1](docs/DOCUMENTACION_PARCIAL_1.md)
- [Formato de Persistencia](docs/formato_persistencia.md)
