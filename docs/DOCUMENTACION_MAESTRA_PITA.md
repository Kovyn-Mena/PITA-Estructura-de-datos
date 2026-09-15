# UNIVERSIDAD POPULAR DEL CESAR
## FACULTAD DE INGENIERÍAS Y TECNOLÓGICAS
### DEPARTAMENTO DE INGENIERÍA DE SISTEMAS
**Asignatura:** Estructura de Datos (Taller 1: Listas)  
**Proyecto:** PITA — Programa Integrado de Transacciones Académicas  
**Versión del Sistema:** 1.0 (Consolidado Final)  
**Fecha:** Septiembre de 2026 — Valledupar, Cesar  

---

# DOCUMENTACIÓN MAESTRA DEL SISTEMA PITA

```
================================================================================
           PROGRAMA INTEGRADO DE TRANSACCIONES ACADÉMICAS (PITA)
                    UNIVERSIDAD POPULAR DEL CESAR
================================================================================
```

## Control del Documento

| Campo | Detalle Institucional |
| :--- | :--- |
| **Título del Documento** | Documentación Maestra y Especificación Técnica del Sistema PITA |
| **Institución** | Universidad Popular del Cesar (UPC) |
| **Facultad** | Facultad de Ingenierías y Tecnológicas |
| **Programa Académico** | Ingeniería de Sistemas |
| **Asignatura** | Estructura de Datos |
| **Actividad Evaluativa** | Taller 1: Listas |
| **Docente Titular** | Ing. Adith Pérez |
| **Entorno de Desarrollo** | C++ (C++17, GCC/MinGW) y Python (Python 3.8+, Tkinter Desktop GUI) |
| **Estructura Central de Datos** | Colecciones dinámicas secuenciales en memoria (`std::vector` en C++, `list` en Python) |
| **Mecanismo de Persistencia** | Archivos de texto plano con delimitador pipe (`|`) en directorio `data/` |
| **Estado del Proyecto** | **COMPLETO Y FINALIZADO (100% implementado y verificado)** |

---

## Tabla de Contenido

1. [Introducción](#1-introducción)
2. [Planteamiento del Problema](#2-planteamiento-del-problema)
3. [Justificación](#3-justificación)
4. [Objetivos](#4-objetivos)
   - 4.1. [Objetivo General](#41-objetivo-general)
   - 4.2. [Objetivos Específicos](#42-objetivos-específicos)
5. [Alcance del Sistema](#5-alcance-del-sistema)
   - 5.1. [Alcance Funcional](#51-alcance-funcional)
   - 5.2. [Delimitación del Alcance Académico](#52-delimitación-del-alcance-académico)
6. [Requerimientos del Sistema](#6-requerimientos-del-sistema)
   - 6.1. [Requerimientos Funcionales (RF)](#61-requerimientos-funcionales-rf)
   - 6.2. [Requerimientos No Funcionales (RNF)](#62-requerimientos-no-funcionales-rnf)
7. [Estrategia de Solución y Arquitectura de Software](#7-estrategia-de-solución-y-arquitectura-de-software)
   - 7.1. [Arquitectura en Capas Modulares](#71-arquitectura-en-capas-modulares)
   - 7.2. [Estrategia de Implementación en Espejo (C++ y Python)](#72-estrategia-de-implementación-en-espejo-c-y-python)
8. [Diseño de Estructuras de Datos (TADs y Listas)](#8-diseño-de-estructuras-de-datos-tads-y-listas)
   - 8.1. [Justificación del Uso de Listas Secuenciales](#81-justificación-del-uso-de-listas-secuenciales)
   - 8.2. [Análisis de Complejidad Algorítmica](#82-análisis-de-complejidad-algorítmica)
9. [Modelo de Dominio y Especificación de Entidades](#9-modelo-de-dominio-y-especificación-de-entidades)
   - 9.1. [Entidades Institucionales y Curriculares (Facultad, Programa, Curso)](#91-entidades-institucionales-y-curriculares)
   - 9.2. [Entidad Estudiante y Registro de Matrículas](#92-entidad-estudiante-y-registro-de-matrículas)
   - 9.3. [Entidad Profesor y Modalidades de Vinculación](#93-entidad-profesor-y-modalidades-de-vinculación)
   - 9.4. [Entidad Administrativo y Escala Salarial](#94-entidad-administrativo-y-escala-salarial)
   - 9.5. [Matriz de Relaciones y Cardinalidad](#95-matriz-de-relaciones-y-cardinalidad)
10. [Variables de Entrada y Salida del Modelo (Punto 6 del Taller)](#10-variables-de-entrada-y-salida-del-modelo)
    - 10.1. [Modelo Académico](#101-modelo-académico)
    - 10.2. [Modelo Salarial y Prestacional](#102-modelo-salarial-y-prestacional)
11. [Reglas de Negocio y Lógica de Aplicación](#11-reglas-de-negocio-y-lógica-de-aplicación)
    - 11.1. [Operaciones CRUD Estándar por TAD](#111-operaciones-crud-estándar-por-tad)
    - 11.2. [Reglas Académicas, Matrícula y Promedio](#112-reglas-académicas-matrícula-y-promedio)
    - 11.3. [Regla Institucional EBRA (Evaluación de Bajo Rendimiento Académico)](#113-regla-institucional-ebra)
12. [Modelo de Liquidación de Nómina y Marco Normativo 2026](#12-modelo-de-liquidación-de-nómina-y-marco-normativo-2026)
    - 12.1. [Docentes de Planta (Decreto 1279 de 2002 y Decreto 318 de 2026)](#121-docentes-de-planta)
    - 12.2. [Docentes Ocasionales (Acuerdo UPC 027 de 2024, Art. 24)](#122-docentes-ocasionales)
    - 12.3. [Docentes Catedráticos (Acuerdo UPC 027 de 2024, Art. 23)](#123-docentes-catedráticos)
    - 12.4. [Personal Administrativo (Escala Salarial Oficial de 4 Niveles)](#124-personal-administrativo)
    - 12.5. [Deducciones de Ley del Trabajador (PILA y Estatuto Tributario)](#125-deducciones-de-ley-del-trabajador)
    - 12.6. [Aportes Patronales Institucionales UPC (Costo Empleador)](#126-aportes-patronales-institucionales-upc)
    - 12.7. [Provisiones Mensuales de Prestaciones Sociales](#127-provisiones-mensuales-de-prestaciones-sociales)
13. [Persistencia de Datos e Interoperabilidad](#13-persistencia-de-datos-e-interoperabilidad)
    - 13.1. [Formato Pipe-Delimited (`|`)](#131-formato-pipe-delimited)
    - 13.2. [Inventario de Archivos en `data/`](#132-inventario-de-archivos-en-data)
    - 13.3. [Política de Arranque: Carga de Datos vs. Ejecución Limpia (Requisito 11)](#133-política-de-arranque)
14. [Diseño e Implementación en C++](#14-diseño-e-implementación-en-c)
    - 14.1. [Estructura del Código Fuente (`cpp/`)](#141-estructura-del-código-fuente-cpp)
    - 14.2. [Manejo de Entrada/Salida, Menús y Estética en Consola](#142-manejo-de-entradasalida-menús-y-estética-en-consola)
    - 14.3. [Instrucciones de Compilación y Ejecución](#143-instrucciones-de-compilación-y-ejecución)
15. [Diseño e Implementación en Python](#15-diseño-e-implementación-en-python)
    - 15.1. [Estructura del Código Fuente (`python/`)](#151-estructura-del-código-fuente-python)
    - 15.2. [Interfaz Gráfica de Escritorio (Desktop GUI en Tkinter)](#152-interfaz-gráfica-de-escritorio-desktop-gui-en-tkinter)
    - 15.3. [Modo Consola Interactivo](#153-modo-consola-interactivo)
16. [Casos de Uso Principales (Flujos de Proceso)](#16-casos-de-uso-principales-flujos-de-proceso)
17. [Verificación, Pruebas y Resultados](#17-verificación-pruebas-y-resultados)
18. [Matriz de Cumplimiento de los Parámetros del Taller 1](#18-matriz-de-cumplimiento-de-los-parámetros-del-taller-1)
19. [Conclusiones](#19-conclusiones)
20. [Referencias Documentales y Normativas](#20-referencias-documentales-y-normativas)

---

# 1. Introducción

El presente documento constituye la memoria técnica, diseño conceptual y documentación de ingeniería del software **PITA (Programa Integrado de Transacciones Académicas)**. Este sistema ha sido desarrollado como respuesta formal a los requerimientos del **Taller 1 de la asignatura Estructura de Datos** del programa de Ingeniería de Sistemas en la Universidad Popular del Cesar (UPC).

El proyecto PITA simula y reemplaza funcionalmente el sistema institucional de información universitaria (denominado comúnmente *Vortal*), articulando la gestión académica, estudiantil, docente, administrativa y de talento humano. A diferencia de las soluciones empresariales comerciales basadas en motores de bases de datos relacionales externos (RDBMS), el desafío central de este taller reside en resolver la coherencia transaccional, las relaciones de cardinalidad, la búsqueda, la agregación y la persistencia de datos mediante el uso riguroso de **Tipos Abstractos de Datos (TAD)** y **estructuras de datos basadas en listas**, implementadas de manera equivalente e interoperable en **C++** y **Python**.

El sistema integra adicionalmente un motor de simulación de nómina auditable fundamentado en la legislación laboral colombiana y los estatutos propios de la Universidad Popular del Cesar (Decreto 1279 de 2002, Acuerdo UPC 027 de 2024, Decreto 318 de 2026, Decreto 159 de 2026 y Ley 100 de 1993), demostrando que una arquitectura de listas en memoria bien estructurada es capaz de procesar liquidaciones salariales multinivel con deducciones de ley, aportes patronales y provisiones prestacionales exactas.

---

# 2. Planteamiento del Problema

La gestión de las transacciones académicas y administrativas en una institución de educación superior de carácter público plantea múltiples retos de interdependencia conceptual:
1. **Jerarquía Institucional Multicapa:** Una facultad alberga múltiples programas académicos; cada programa articula planes curriculares compuestos por cursos; los cursos demandan la asignación de un docente cualificado y la inscripción controlada de estudiantes.
2. **Ciclo de Vida Académico y Alerta Temprana:** Los estudiantes cursan asignaturas de manera dinámica. El cálculo acumulado de su rendimiento no es un campo estático, sino un proceso en memoria derivado de sus notas. Aquellos estudiantes cuyo promedio acumulado sea inferior al umbral institucional deben ser clasificados bajo la condición de **EBRA (Evaluación de Bajo Rendimiento Académico)** para activar mecanismos de retención y acompañamiento psicopedagógico.
3. **Complejidad y Heterogeneidad en la Nómina Docente y Administrativa:** Coexisten regímenes salariales dispares dentro del mismo claustro:
   - *Docentes de Planta:* Regidos por el sistema salarial de puntos del Decreto 1279 de 2002, donde intervienen títulos, categoría en el escalafón, experiencia y productividad investigativa.
   - *Docentes Ocasionales:* Regidos por el Acuerdo UPC 027 de 2024, calculados con factores de salarios mínimos legales mensuales vigentes (SMMLV) y bonificaciones adicionales por títulos de postgrado que no constituyen salario.
   - *Docentes Catedráticos:* Retribuidos en función de horas mensuales certificadas (máximo 18 semanales) bajo resolución rectoral, permitiendo además la figura *Ad-honorem* sin contraprestación monetaria.
   - *Personal Administrativo:* Gobernado por una escala de cuatro niveles oficiales del sector público.
4. **Persistencia e Interoperabilidad sin Dependencias Externas:** El sistema debe conservar su información en disco mediante archivos de texto plano estructurado, garantizando que un lote de datos exportado por el ejecutable compilado en C++ pueda ser leído, modificado y salvado por la interfaz en Python sin ninguna pérdida de fidelidad.

---

# 3. Justificación

La implementación de PITA permite consolidar los fundamentos de la programación orientada a objetos y las estructuras de datos avanzadas:
- **Demostración de Abstracción y Encapsulamiento:** Se modelan tipos abstractos de datos específicos para cada concepto del dominio (Facultades, Programas, Cursos, Estudiantes, Profesores y Administrativos), garantizando que las responsabilidades de estado y comportamiento se encuentren perfectamente acotadas.
- **Eficiencia en Memoria vs. Simplicidad:** Al evitar la sobrecarga de un motor SQL externo, el estudiante de ingeniería comprende a bajo nivel el costo computacional de las operaciones secuenciales ($O(1)$, $O(n)$), las referencias cruzadas mediante claves foráneas lógicas y los algoritmos de filtrado y agregación.
- **Contraste Multiplataforma y Multilenguaje:** Desarrollar dos versiones idénticas (C++ nativo de alto rendimiento y Python de alto nivel con GUI interactiva) exige un diseño conceptual riguroso previo. Ambas implementaciones actúan como espejo y auditoría cruzada mutua.
- **Conexión con la Realidad Institucional:** El ejercicio no se limita a manipular datos ficticios abstractos, sino que traduce decretos gubernamentales y acuerdos del Consejo Superior de la UPC en algoritmos ejecutables y desprendibles oficiales de pago.

---

# 4. Objetivos

### 4.1 Objetivo General
Diseñar, implementar y verificar un sistema integral basado en estructuras de datos de listas para la gestión de transacciones académicas, estudiantiles, docentes, administrativas y de nómina de la Universidad Popular del Cesar (PITA), con persistencia en archivos planos e interfaces operativas completas tanto en C++ como en Python.

### 4.2 Objetivos Específicos
1. Modelar formalmente los Tipos Abstractos de Datos (TAD) para las seis entidades nodales: `Facultad`, `Programa`, `Curso`, `Estudiante`, `Profesor` y `Administrativo`, además de la estructura relacional `Matricula`.
2. Implementar para cada TAD las operaciones canónicas de manipulación de datos: creación, inclusión en listas, consulta individual y general, modificación de atributos, desactivación (borrado lógico) y eliminación permanente (borrado físico).
3. Desarrollar la lógica académica estudiantil, permitiendo la matrícula y cancelación de asignaturas, el cálculo dinámico del promedio ponderado simple y la activación automática de la alerta de bajo rendimiento (EBRA) ante promedios inferiores a 3.25.
4. Diseñar e integrar el motor de liquidación salarial de acuerdo con el Decreto 1279 de 2002, Acuerdo UPC 027 de 2024 y decretos salariales de 2026, calculando devengados, deducciones de ley (PILA, salud, pensión, FSP, estampilla pro-UPC, retención en la fuente), aportes patronales institucionales y provisiones de prestaciones sociales.
5. Garantizar la persistencia simétrica mediante archivos de texto plano delimitados por tuberías (`|`), permitiendo al usuario decidir en el arranque si desea iniciar con datos precargados o comenzar una sesión limpia.
6. Proporcionar interfaces de usuario con alto valor estético y ergonómico: consola interactiva con refresco inteligente en C++ y Python, y una aplicación de escritorio profesional con ventanas modales y Dock inferior en Python (Tkinter).

---

# 5. Alcance del Sistema

### 5.1 Alcance Funcional
El sistema PITA cubre en su totalidad los siguientes módulos operativos:
- **Módulo Institucional:** Registro, consulta, edición, desactivación lógica y borrado físico de Facultades y Programas Académicos adscritos.
- **Módulo Curricular:** Gestión de asignaturas (Cursos) con código, nombre, número de créditos, código de programa y asignación docente.
- **Módulo Estudiantil y Académico:** Administración de estudiantes, matrícula y retiro de cursos, asignación de calificaciones numéricas, cómputo de promedio en tiempo real y detección preventiva de deserción académica (Alerta EBRA).
- **Módulo de Talento Humano Docente:** Clasificación contractual por regímenes:
  - Planta (tiempo completo / medio tiempo, escalafón de auxiliar a titular, puntos por títulos y productividad).
  - Ocasional (factores directos de SMMLV según escalafón y dedicación, bonificación mensual por cualificación de postgrado: especialización, maestría o doctorado).
  - Catedrático (asignación horaria semanal de hasta 18 horas y modalidad especial ad-honorem).
- **Módulo Administrativo:** Gestión de funcionarios clasificados en cuatro niveles de escala salarial oficial (Asistencial, Técnico, Profesional, Directivo), tipos de contratación (Planta, Provisional, Contrato) y vinculación a facultad o nivel central.
- **Módulo de Liquidación y Auditoría Salarial:** Emisión de desprendibles institucionales oficiales detallados con desglose mensual y proyección anualizada, deducciones obligatorias, costos para la UPC y provisiones prestacionales.
- **Módulo de Persistencia:** Serialización y deserialización automática de 7 archivos de datos en disco.

### 5.2 Delimitación del Alcance Académico
Conforme a los lineamientos del Taller 1 de Estructura de Datos:
- El almacenamiento se gestiona en memoria primaria durante la ejecución del programa; la sincronización con memoria secundaria se realiza al arrancar y al finalizar la sesión.
- No se incorporan gestores de bases de datos relacionales externos (MySQL, PostgreSQL, etc.) ni capas intermedias de mapeo objeto-relacional (ORM), preservando la pureza didáctica de las estructuras de datos nativas.
- Las validaciones normativas y laborales representan un modelo de simulación matemática formal basado en decretos colombianos, diseñado con fines pedagógicos y técnicos.

---

# 6. Requerimientos del Sistema

### 6.1 Requerimientos Funcionales (RF)

| Código | Requerimiento Funcional | Componente Asociado | Estado |
| :--- | :--- | :--- | :--- |
| **RF-01** | Gestionar el conjunto de facultades institucionales (CRUD completo). | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-02** | Gestionar los programas académicos asociados a facultades existentes. | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-03** | Gestionar las asignaturas (cursos) asociadas a programas y profesores. | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-04** | Gestionar la información de estudiantes y su estado curricular. | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-05** | Permitir la matrícula y cancelación de cursos por parte del estudiante. | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-06** | Calcular el promedio ponderado simple del estudiante en memoria. | `entidades.h` / `entidades.py` | **100% CUMPLIDO** |
| **RF-07** | Detectar y emitir alerta automática de bajo rendimiento (EBRA < 3.25). | `gestion.cpp` / `gui.py` | **100% CUMPLIDO** |
| **RF-08** | Gestionar información personal, contractual y académica de profesores. | `gestion.cpp` / `gestion.py` | **100% CUMPLIDO** |
| **RF-09** | Liquidar salarios de Planta aplicando puntos y Decreto 1279 de 2002. | `nomina.cpp` / `nomina.py` | **100% CUMPLIDO** |
| **RF-10** | Liquidar Ocasionales y Catedráticos según Acuerdo UPC 027 de 2024. | `nomina.cpp` / `nomina.py` | **100% CUMPLIDO** |
| **RF-11** | Gestionar funcionarios administrativos y aplicar escala salarial por niveles. | `gestion.cpp` / `nomina.py` | **100% CUMPLIDO** |
| **RF-12** | Liquidar deducciones de ley (salud, pensión, FSP, estampilla, retefuente). | `nomina.cpp` / `nomina.py` | **100% CUMPLIDO** |
| **RF-13** | Calcular aportes patronales UPC y provisiones de prestaciones sociales. | `nomina.cpp` / `nomina.py` | **100% CUMPLIDO** |
| **RF-14** | Persistir datos en texto plano y ofrecer arranque con o sin datos previos. | `persistencia.*` / `main.*` | **100% CUMPLIDO** |

### 6.2 Requerimientos No Funcionales (RNF)
- **RNF-01 (Interoperabilidad Estricta):** Los archivos generados en disco deben ser idénticos e intercambiables entre los entornos de ejecución de C++ y Python.
- **RNF-02 (Integridad Referencial en Memoria):** No se permite la creación de registros dependientes que apunten a entidades inexistentes (ej. crear un programa bajo una facultad no registrada, o inscribir un curso a un programa inválido).
- **RNF-03 (Borrado Lógico y Físico Diferenciado):** Cada entidad soporta la desactivación lógica (`activo = false`) que preserva la trazabilidad del registro sin eliminarlo de la lista, y la eliminación física irreversible con confirmación de usuario.
- **RNF-04 (Ergonomía y Estética Visual):** Cumpliendo el ítem 10 del taller, la versión en consola implementa limpieza de pantalla, pausado inteligente y atajos rápidos de teclado. La versión gráfica en Python ofrece una interfaz de escritorio pulida con paleta institucional, tarjetas de indicadores y navegación mediante Dock.

---

# 7. Estrategia de Solución y Arquitectura de Software

### 7.1 Arquitectura en Capas Modulares
Para evitar código espagueti y facilitar la mantenibilidad, el sistema se desacopla en cinco capas lógicas bien delimitadas:

```
+-----------------------------------------------------------------------+
|                       CAPA DE PRESENTACIÓN / UI                       |
|   - Modo Consola Interactivo (C++ / Python): main.cpp, main.py        |
|   - Modo Gráfico de Escritorio (Python Tkinter): gui.py (PitaApp)     |
+-----------------------------------------------------------------------+
                                  │
                                  ▼
+-----------------------------------------------------------------------+
|                    CAPA DE GESTIÓN Y LÓGICA (CRUD)                    |
|   - Controladores de flujo y validaciones referenciales              |
|   - gestion.h / gestion.cpp  |  gestion.py                            |
+-----------------------------------------------------------------------+
            │                                             │
            ▼                                             ▼
+------------------------------------+  +-------------------------------+
|      CAPA DE DOMINIO (TADs)        |  |    CAPA SALARIAL Y NÓMINA     |
| - Facultad, Programa, Curso        |  | - Fórmulas Dec. 1279 y Ac. 027|
| - Estudiante, Profesor, Admin      |  | - Deducciones PILA, Aportes   |
| - Matricula (anidada)              |  | - Prestaciones sociales       |
| entidades.h  |  entidades.py       |  | nomina.h / cpp  |  nomina.py  |
+------------------------------------+  +-------------------------------+
                                  │
                                  ▼
+-----------------------------------------------------------------------+
|                         CAPA DE PERSISTENCIA                          |
|   - Serialización y deserialización en texto plano (|)                |
|   - persistencia.h / persistencia.cpp  |  persistencia.py             |
|   - Directorio de archivos: data/*.txt                                |
+-----------------------------------------------------------------------+
```

### 7.2 Estrategia de Implementación en Espejo (C++ y Python)
Se adoptó una disciplina de desarrollo homólogo:
1. Las entidades poseen exactamente los mismos identificadores de campo y tipos correspondientes (`std::string` $\leftrightarrow$ `str`, `int` $\leftrightarrow$ `int`, `double/float` $\leftrightarrow$ `float`, `bool` $\leftrightarrow$ `bool`).
2. El motor de persistencia utiliza el mismo orden secuencial de columnas en cada línea de archivo.
3. Las constantes salariales (punto salarial de $23.924, SMMLV de $1.750.905, deducciones del 4%, etc.) son compartidas entre ambos lenguajes, arrojando centavo a centavo el mismo resultado aritmético.

---

# 8. Diseño de Estructuras de Datos (TADs y Listas)

### 8.1 Justificación del Uso de Listas Secuenciales
El enunciado del Taller 1 establece las **Listas** como el objeto de estudio central. En la implementación:
- En **C++**, se utilizan vectores dinámicos (`std::vector<T>`), los cuales representan la abstracción canónica de listas de tamaño variable contiguas en memoria con acceso aleatorio e iteración secuencial segura.
- En **Python**, se utilizan listas nativas dinámicas (`list`), proveyendo colecciones heterogéneas flexibles con gestión automática de memoria.

La elección de listas dinámicas permite:
- Modelar de forma natural colecciones abiertas de tamaño desconocido en tiempo de compilación.
- Facilitar la serialización hacia y desde archivos de texto plano recorriendo los nodos de principio a fin.
- Implementar listas anidadas dentro de una entidad primaria: por ejemplo, cada objeto `Estudiante` posee su propia lista interna de `matriculas`, encapsulando la relación uno a muchos sin necesidad de tablas intermedias relacionales complejas en memoria.

### 8.2 Análisis de Complejidad Algorítmica

| Operación | Complejidad Temporal | Justificación Técnica |
| :--- | :---: | :--- |
| **Inserción (Inclusión)** | $O(1)$ amortizado | Inserción al final de la lista dinámica (`push_back` en C++, `append` en Python). |
| **Búsqueda por Clave** | $O(n)$ | Recorrido lineal comparando el código o documento identificador. |
| **Consulta General (Listar)** | $O(n)$ | Visita secuencial completa e impresión de cada elemento de la colección. |
| **Modificación de Registro** | $O(n)$ | Localización lineal del nodo ($O(n)$) seguida de mutación directa en memoria ($O(1)$). |
| **Desactivación (Borrado Lógico)** | $O(n)$ | Localización lineal ($O(n)$) y actualización de bandera booleana `activo = false` ($O(1)$). |
| **Eliminación (Borrado Físico)** | $O(n)$ | Localización lineal y desplazamiento interno de elementos remanentes en el vector/lista. |
| **Persistencia (Guardado en Disco)**| $O(n)$ | Recorrido lineal serializando un registro por línea hacia el flujo de archivo. |

---

# 9. Modelo de Dominio y Especificación de Entidades

### 9.1 Entidades Institucionales y Curriculares

#### A. TAD Facultad
Representa la unidad académica y administrativa de mayor jerarquía.
- `codigo` (Cadena, Clave Primaria): Código único identificador (ej. `FIS`).
- `nombre` (Cadena): Denominación oficial (ej. *Facultad de Ingenierías y Tecnológicas*).
- `decano` (Cadena): Nombre del titular de la decanatura.
- `activo` (Booleano): Bandera para borrado lógico (`true` = Activa, `false` = Inactiva).

#### B. TAD Programa
Unidad académica curricular adscrita formalmente a una facultad.
- `codigo` (Cadena, Clave Primaria): Identificador único del programa (ej. `SIS`).
- `nombre` (Cadena): Denominación académica (ej. *Ingeniería de Sistemas*).
- `nivel` (Cadena): Nivel de formación (*Tecnológico, Pregrado, Especialización, Maestría*).
- `codigo_facultad` (Cadena, Clave Foránea): Vínculo obligatorio a una Facultad existente.
- `activo` (Booleano): Control de borrado lógico.

#### C. TAD Curso
Asignatura académica dictada dentro de un programa y asignada a un docente.
- `codigo` (Cadena, Clave Primaria): Código de la asignatura (ej. `EDD1`).
- `nombre` (Cadena): Nombre del curso (ej. *Estructura de Datos*).
- `creditos` (Entero): Número de créditos académicos según plan curricular.
- `codigo_profesor` (Cadena, Clave Foránea): Identificación del docente asignado (o vacío si está vacante).
- `codigo_programa` (Cadena, Clave Foránea): Vínculo con el programa académico al que pertenece.
- `activo` (Booleano): Control de borrado lógico.

---

### 9.2 Entidad Estudiante y Registro de Matrículas

#### A. TAD Estudiante
Representa al alumno activo o egresado de la institución.
- `identificacion` (Cadena, Clave Primaria): Documento de identidad único.
- `nombre_completo` (Cadena): Nombres y apellidos.
- `codigo_programa` (Cadena, Clave Foránea): Programa académico en el que se encuentra matriculado.
- `estado` (Cadena): Estado académico administrativo (*Activo, Inactivo, Graduado*).
- `activo` (Booleano): Control de borrado lógico.
- `matriculas` (Lista de Matrículas): **Estructura anidada en memoria** que almacena las asignaturas inscritas por el alumno.

#### B. Estructura Anidada Matricula
- `codigo_curso` (Cadena): Código de la asignatura inscrita.
- `nota` (Decimal/Flotante): Calificación obtenida en escala de 0.0 a 5.0.

*Métodos propios del TAD Estudiante:*
- `calcular_promedio()`: Recorre la lista interna de matrículas y computa el promedio simple de las notas registradas:
  $$\text{Promedio} = \frac{\sum_{i=1}^{k} \text{nota}_i}{k}$$
- `esta_en_riesgo_ebra()`: Evalúa si $\text{Promedio} < 3.25$. Retorna `false` si el estudiante no posee cursos con nota para evitar falsos positivos iniciales.

---

### 9.3 Entidad Profesor y Modalidades de Vinculación

#### TAD Profesor
Modela al personal docente articulando su información personal, académica y de nómina según las tres modalidades reconocidas en el Acuerdo UPC 027 de 2024 y el Decreto 1279 de 2002:
- `identificacion` (Cadena, Clave Primaria): Cédula o identificador docente.
- `nombre_completo` (Cadena): Nombres y apellidos.
- `codigo_programa` (Cadena, Clave Foránea): Programa de adscripción principal.
- `tipo_vinculacion` (Cadena): Modalidad contractual (*Planta, Ocasional, Catedratico*).
- `dedicacion` (Cadena): Jornada laboral (*TiempoCompleto, MedioTiempo, HorasCatedra*).
- `categoria_escalafon` (Cadena): Ubicación en el escalafón universitario (*Auxiliar, Asistente, Asociado, Titular*).
- `horas_catedra_semanales` (Entero): Asignación lectiva para catedráticos (hasta 18 horas).
- `ad_honorem` (Booleano): Determina si la labor docente se presta sin asignación pecuniaria.
- `anios_experiencia` (Entero): Años certificados de ejercicio docente/profesional.
- `puntos_titulos` (Entero): Puntos salariales por posgrados reconocidos (para docentes de Planta).
- `puntos_productividad` (Entero): Puntos acumulados por artículos, libros y patentes (Decreto 1279).
- `posgrado` (Cadena): Máximo título obtenido para docentes Ocasionales/Catedráticos (*Ninguno, Especialización, Maestría, Doctorado*).
- `activo` (Booleano): Control de borrado lógico.

---

### 9.4 Entidad Administrativo y Escala Salarial

#### TAD Administrativo
Modela al personal técnico, asistencial y directivo que garantiza el funcionamiento operacional de la universidad:
- `identificacion` (Cadena, Clave Primaria): Documento de identidad único.
- `nombre_completo` (Cadena): Nombres y apellidos del funcionario.
- `cargo` (Cadena): Rol institucional (ej. *Secretario Académico, Auxiliar Contable, Asesor de Rectoría*).
- `categoria` (Cadena): Nivel oficial de escala salarial (*Nivel 1, Nivel 2, Nivel 3, Nivel 4*).
- `tipo_contratacion` (Cadena): Naturaleza de la vinculación (*Planta, Provisional, Contrato*).
- `salario_base` (Flotante): Asignación salarial básica pactada o adoptada por escala oficial.
- `codigo_facultad` (Cadena, Clave Foránea Opcional): Facultad donde presta servicio; si permanece vacante representa adscripción a *Nivel Central / Rectoría*.
- `activo` (Booleano): Control de borrado lógico.

---

### 9.5 Matriz de Relaciones y Cardinalidad

| Entidad Origen | Entidad Destino | Cardinalidad | Mecanismo de Resolución en el Sistema |
| :--- | :--- | :---: | :--- |
| **Facultad** | **Programa** | $1 : N$ | Campo `codigo_facultad` en cada Programa. |
| **Programa** | **Curso** | $1 : N$ | Campo `codigo_programa` en cada Curso. |
| **Profesor** | **Curso** | $1 : N$ | Campo `codigo_profesor` en cada Curso. |
| **Programa** | **Estudiante**| $1 : N$ | Campo `codigo_programa` en cada Estudiante. |
| **Estudiante**| **Matricula** | $1 : N$ | Lista interna dinámica de matrículas contenida en `Estudiante`. |
| **Curso** | **Matricula** | $1 : N$ | Campo `codigo_curso` en cada elemento de matrícula. |
| **Facultad** | **Administrativo** | $1 : N$ (0..1) | Campo opcional `codigo_facultad` en Administrativo (vacío = Nivel Central). |

---

# 10. Variables de Entrada y Salida del Modelo (Punto 6 del Taller)

En estricto cumplimiento del **Punto 6 del Taller 1**, a continuación se identifican y discriminan exhaustivamente las variables de entrada y salida tanto de la estructura académica como del modelo salarial:

### 10.1 Modelo Académico

#### Variables de Entrada
- `codigoFacultad`, `nombreFacultad`, `decanoFacultad`.
- `codigoPrograma`, `nombrePrograma`, `nivelFormacion`, `facultadAdscrita`.
- `codigoCurso`, `nombreCurso`, `creditosCurso`, `profesorAsignado`, `programaCurso`.
- `identificacionEstudiante`, `nombreEstudiante`, `programaEstudiante`, `estadoEstudiante`.
- `cursoAMatricular`, `notaObtenida` (escala 0.0 a 5.0).
- `cursoACancelar`.

#### Variables de Salida
- `estadoOperacion`: Confirmación o rechazo con causa técnica detallada de cada transacción.
- `listadoEntidades`: Vistas tabulares y filtradas por facultad, programa o curso.
- `promedioAcumulado`: Promedio ponderado simple computado en memoria.
- `alertaEBRA`: Booleano y mensaje prominente de alerta cuando `promedio < 3.25`.
- `estadoRegistro`: Indicador de registro Activo o Inactivo (borrado lógico).
- `archivosPersistidos`: Volcado estructurado en `data/*.txt`.

### 10.2 Modelo Salarial y Prestacional

#### Variables de Entrada
- `tipoVinculacion`: Planta, Ocasional o Catedrático.
- `dedicacion`: Tiempo Completo, Medio Tiempo o Horas Cátedra.
- `categoriaEscalafon`: Auxiliar, Asistente, Asociado o Titular.
- `posgradoDocente`: Ninguno, Especialización, Maestría o Doctorado.
- `horasCatedraSemanales`: Número entero de horas lectivas (máximo 18).
- `esAdHonorem`: Indicador de prestación voluntaria sin remuneración.
- `aniosExperiencia`, `puntosTitulos`, `puntosProductividad`: Factores de puntos para Planta.
- `categoriaAdministrativa`: Nivel 1, Nivel 2, Nivel 3 o Nivel 4.
- `salarioBaseAdministrativo`: Asignación contractual.
- **Parámetros Institucionales Vigentes 2026:**
  - `VALOR_PUNTO`: **$23.924 COP** (Decreto 318 de 2026).
  - `SMMLV`: **$1.750.905 COP** (Decreto 159 de 2026).
  - `PUNTOS_PREGRADO`: **178 puntos** (Decreto 1279 de 2002).

#### Variables de Salida
- `salarioBruto` (Sueldo Básico mensual).
- `bonificacionPosgrado` (Reconocimiento económico no salarial del Acuerdo 027).
- `totalDevengado`: $\text{Salario Bruto} + \text{Bonificación Posgrado}$.
- `descuentoSalud`: 4% sobre IBC (redondeo a centena según PILA).
- `descuentoPension`: 4% sobre IBC (redondeo a centena según PILA).
- `descuentoFSP`: Fondo de Solidaridad Pensional (1% si $\text{IBC} \ge 4\text{ SMMLV}$).
- `descuentoEstampilla`: 0.2% Pro-UPC sobre sueldo básico.
- `retencionFuente`: Impuesto de renta sobre salarios según Art. 383 Estatuto Tributario.
- `totalDeducciones`: Suma integral de descuentos de nómina.
- `salarioNetoAPagar`: $\text{Total Devengado} - \text{Total Deducciones}$.
- `aportesPatronales`: Desglose institucional de Salud (8.5%), Pensión (12%), ARL (0.522%) y Caja de Compensación (4%).
- `costoTotalEmpleadorUPC`: $\text{Salario Bruto} + \text{Aportes Patronales}$.
- `provisionPrestaciones`: Desglose de Prima de servicios, Cesantías, Intereses de cesantías, Prima de navidad, Vacaciones, Prima de vacaciones y Bonificación por servicios.

---

# 11. Reglas de Negocio y Lógica de Aplicación

### 11.1 Operaciones CRUD Estándar por TAD
En estricta observancia del enunciado (*creación, inclusión, eliminación, desactivación, consulta, modificación y persistencia*):
1. **Creación e Inclusión:** Se instancia el objeto validando unicidad de clave primaria y existencia de entidades padre. Se incluye al final de la colección en memoria ($O(1)$).
2. **Consulta y Búsqueda:** Búsqueda por código/cédula ($O(n)$) con retorno de referencia o puntero al objeto, y despliegue tabular de listas completas con filtros contextuales.
3. **Modificación:** Edición selectiva en memoria de campos descriptivos respetando las claves primarias inmutables.
4. **Desactivación (Borrado Lógico):** Se conmuta la bandera `activo = false`. El registro se mantiene en memoria y en disco para no romper relaciones históricas ni generar punteros colgantes.
5. **Eliminación (Borrado Físico):** Supresión irreversible del registro de la lista con diálogo de confirmación obligatoria al usuario.

### 11.2 Reglas Académicas, Matrícula y Promedio
- **Integridad Curricular:** No es posible inscribir asignaturas a estudiantes inactivos.
- **Unicidad de Inscripción:** Un estudiante no puede inscribir dos veces la misma asignatura de forma simultánea.
- **Rango de Calificaciones:** Las notas registradas se restringen al intervalo institucional válido $[0.0,\, 5.0]$.
- **Cancelación de Cursos:** La cancelación de una materia remueve el registro de la lista de matrículas del estudiante y recalcula de forma inmediata el promedio y la condición EBRA.

### 11.3 Regla Institucional EBRA
- **Definición:** *Evaluación de Bajo Rendimiento Académico*, mecanismo de control y alerta temprana para prevenir la deserción estudiantil en la Universidad Popular del Cesar.
- **Algoritmo de Detección:**
  ```python
  if len(estudiante.matriculas) > 0 and estudiante.calcular_promedio() < 3.25:
      alerta_ebra = True  # Estudiante en riesgo académico
  else:
      alerta_ebra = False
  ```
- **Protección contra Falsos Positivos:** Si el estudiante acaba de ser creado o no cuenta con asignaturas cursadas, el sistema reporta promedio 0.0 pero **no activa la alerta EBRA**.
- **Notificación Visual:** En la consola se imprime un cintillo destacado de advertencia (`*** ALERTA EBRA: estudiante en riesgo ***`); en la interfaz gráfica se ilumina una placa en rojo carmesí con icono de alerta junto a la ficha del estudiante.

---

# 12. Modelo de Liquidación de Nómina y Marco Normativo 2026

### 12.1 Docentes de Planta
*Normativa: Decreto 1279 de 2002 y Decreto Salarial 318 de 2026.*
Aplica a los empleados públicos docentes de carrera universitaria.
- **Fórmula de Salario Básico Mensual:**
  $$\text{Salario Bruto} = \text{round}\left(\text{Total Puntos} \times \text{VALOR\_PUNTO} \times \text{Factor Dedicación}\right)$$
- **Parámetros 2026:** $\text{VALOR\_PUNTO} = \$23.924\text{ COP}$.
- **Puntos Base por Título Universitario de Pregrado:** $178\text{ puntos}$ (Art. 7, regla general).
- **Puntos por Escalafón Universitario (Art. 8):**
  - Profesor Auxiliar: $37\text{ puntos}$
  - Profesor Asistente: $58\text{ puntos}$
  - Profesor Asociado: $74\text{ puntos}$
  - Profesor Titular: $96\text{ puntos}$
- **Puntos Adicionales:** Suma de `puntos_titulos` (especialización, maestría, doctorado reconocidos) y `puntos_productividad` (investigación, patentes, publicaciones indexadas).
- **Factor de Dedicación:** Tiempo Completo $= 1.0$; Medio Tiempo $= 0.5$.

### 12.2 Docentes Ocasionales
*Normativa: Acuerdo UPC 027 del 31 de octubre de 2024, Art. 24.*
Los docentes ocasionales no se rigen por el sistema de puntos del Decreto 1279. Su sueldo se calcula directamente como múltiplo del Salario Mínimo Legal Vigente:
- **SMMLV Vigente 2026:** $\$1.750.905\text{ COP}$ (Decreto 159 de 2026).
- **Factores de Asignación Básica (Art. 24):**
  - Auxiliar: Tiempo Completo $= 2.645\text{ SMMLV}$ ($\$4.631.144$) | Medio Tiempo $= 1.509\text{ SMMLV}$ ($\$2.642.116$)
  - Asistente: Tiempo Completo $= 3.125\text{ SMMLV}$ ($\$5.471.578$) | Medio Tiempo $= 1.749\text{ SMMLV}$ ($\$3.062.333$)
  - Asociado: Tiempo Completo $= 3.606\text{ SMMLV}$ ($\$6.313.763$) | Medio Tiempo $= 1.990\text{ SMMLV}$ ($\$3.484.301$)
  - Titular: Tiempo Completo $= 3.918\text{ SMMLV}$ ($\$6.860.046$) | Medio Tiempo $= 2.146\text{ SMMLV}$ ($\$3.757.442$)
- **Bonificación Mensual por Cualificación en Postgrado (Acuerdo 027/2024):**
  - Especialización ($0.10\text{ SMMLV}$): $\$175.091\text{ COP}$
  - Maestría ($0.45\text{ SMMLV}$): $\$787.907\text{ COP}$
  - Doctorado ($0.90\text{ SMMLV}$): $\$1.575.815\text{ COP}$
  - *Precisión jurídica implementada:* Esta bonificación es un estímulo económico no constitutivo de salario; suma al total devengado pero no incrementa el IBC para seguridad social ni parafiscales.

### 12.3 Docentes Catedráticos
*Normativa: Acuerdo UPC 027 de 2024, Art. 23.*
- La remuneración corresponde a las horas efectivas mensuales asignadas:
  $$\text{Horas Mensuales} = \text{horas\_catedra\_semanales} \times 4.0$$
  $$\text{Salario Bruto} = \text{Horas Mensuales} \times \text{VALOR\_HORA\_CATEDRA}$$
- **Rigor Normativo:** El valor de la hora cátedra debe ser fijado semestralmente por Resolución Rectoral. Si el parámetro no ha sido configurado en el sistema, PITA informa de forma transparente: *"Salario no liquidado: Falta resolución rectoral de hora cátedra"*, evitando generar cifras arbitrarias.
- **Modalidad Ad-Honorem:** Si el contrato es ad-honorem, el sistema asigna salario bruto de $\$0\text{ COP}$ y neto de $\$0\text{ COP}$, respetando la voluntad de servicio institucional honorífico.

### 12.4 Personal Administrativo
*Normativa: Escala Salarial Oficial del Sector Público y Decretos Salariales 2026.*
Para erradicar asignaciones ficticias, el sistema formaliza una escala salarial de 4 niveles institucionales:
- **Nivel 1 (Asistencial / Auxiliar de Servicios / Biblioteca):** $\$1.950.000\text{ COP}$
- **Nivel 2 (Técnico / Secretario Académico de Facultad):** $\$2.800.000\text{ COP}$
- **Nivel 3 (Profesional Universitario / Coordinador de Área):** $\$3.750.000\text{ COP}$
- **Nivel 4 (Asesor de Rectoría / Directivo / Jefe de Departamento):** $\$5.050.000\text{ COP}$
Si al crear un funcionario se indica salario 0, el sistema le asigna automáticamente la asignación de su nivel legal.

### 12.5 Deducciones de Ley del Trabajador
Conforme al Decreto 1990 de 2016 (norma técnica PILA) y el Estatuto Tributario Nacional:
1. **Salud Trabajador (4%):** Calculado sobre el salario básico (IBC) y redondeado al múltiplo de 100 más cercano:
   $$\text{Salud} = \text{round}\left(\frac{\text{IBC} \times 0.04}{100}\right) \times 100$$
2. **Pensión Trabajador (4%):** Calculado sobre el IBC con redondeo a centena PILA:
   $$\text{Pensión} = \text{round}\left(\frac{\text{IBC} \times 0.04}{100}\right) \times 100$$
3. **Fondo de Solidaridad Pensional - FSP (1%):** Se deduce si $\text{IBC} \ge 4\text{ SMMLV}$ ($\$7.003.620\text{ COP}$).
4. **Estampilla Pro-Universidad Popular del Cesar (0.2%):** Gravamen territorial formal del $0.2\%$ sobre el sueldo básico.
5. **Retención en la Fuente por Salarios (Art. 383 Estatuto Tributario):** Sobre la base gravable depurada ($\text{Devengado} - \text{Salud} - \text{Pensión}$ menos el 25% de renta laboral exenta según Art. 206 numeral 10 E.T.), se aplica el 19% sobre el exceso de 95 UVT ($\approx \$4.975.000\text{ COP}$ en 2026), redondeado a miles (norma DIAN).

$$\text{Total Deducciones} = \text{Salud} + \text{Pensión} + \text{FSP} + \text{Estampilla} + \text{Retención}$$
$$\mathbf{Salario\ Neto\ a\ Pagar} = \mathbf{Total\ Devengado} - \mathbf{Total\ Deducciones}$$

### 12.6 Aportes Patronales Institucionales UPC
Costos que asume directamente la Universidad Popular del Cesar como empleador:
- **Pensión Patronal (12%):** $\text{round}(\text{IBC} \times 0.12)$ (Ley 100 de 1993, Art. 20).
- **Salud Patronal (8.5%):** $\text{round}(\text{IBC} \times 0.085)$ (Ley 1122 de 2007, Art. 10; las universidades públicas no están exoneradas por Art. 114-1 E.T.).
- **ARL Riesgos Laborales (0.522%):** $\text{round}(\text{IBC} \times 0.00522)$ (Clase de riesgo I-II, Decreto 1295 de 1994).
- **Caja de Compensación Familiar (4%):** $\text{round}(\text{IBC} \times 0.04)$ (Ley 21 de 1982).
$$\mathbf{Costo\ Total\ Empleador\ UPC} = \mathbf{Salario\ Básico} + \mathbf{Aportes\ Patronales}$$

### 12.7 Provisiones Mensuales de Prestaciones Sociales
Provisiones contables obligatorias para servidores públicos docentes y administrativos:
1. **Prima de Servicios (Decreto 1279/2002, Art. 44):** 30 días de salario por año $\to \frac{\text{Bruto}}{12}$.
2. **Cesantías (Decreto 1279/2002, Art. 45 / Ley 50 de 1990):** 1 mes por año $\to \frac{\text{Bruto}}{12}$.
3. **Intereses a las Cesantías (Ley 52 de 1975):** 12% anual sobre cesantías $\to \frac{\text{Bruto}}{1200}$.
4. **Prima de Navidad (Decreto 1042 de 1978, Art. 33):** 1 mes adicional en diciembre $\to \frac{\text{Bruto}}{12}$.
5. **Vacaciones Remuneradas:** 15 días hábiles remunerados $\to \frac{\text{Bruto}}{24}$.
6. **Prima de Vacaciones (Decreto 1279/2002, Art. 33):** 15 días adicionales al salir a vacaciones $\to \frac{\text{Bruto}}{24}$.
7. **Bonificación por Servicios Prestados (Decreto 1279/2002, Art. 39):** Equivalente a 2 meses por año $\to \frac{\text{Bruto} \times 2}{12}$.

---

# 13. Persistencia de Datos e Interoperabilidad

### 13.1 Formato Pipe-Delimited (`|`)
Se utiliza texto plano estructurado con separador `|` (tubería), sin cabeceras superfluas y con un registro por línea. Se adoptó este formato por las siguientes ventajas técnicas:
- Inmunidad ante comas o espacios presentes en los nombres de las asignaturas o personas.
- Lectura y escritura directa en C++ mediante `std::getline(archivo, campo, '|')` y en Python con `linea.split('|')`.
- Facilidad absoluta para inspección visual y depuración en caliente.

### 13.2 Inventario de Archivos en `data/`

| Archivo | Estructura de Campos por Línea |
| :--- | :--- |
| `facultades.txt` | `codigo\|nombre\|decano\|activo` |
| `programas.txt` | `codigo\|nombre\|nivel\|codigo_facultad\|activo` |
| `cursos.txt` | `codigo\|nombre\|creditos\|codigo_profesor\|codigo_programa\|activo` |
| `estudiantes.txt` | `identificacion\|nombre_completo\|codigo_programa\|estado\|activo` |
| `matriculas.txt` | `identificacion_estudiante\|codigo_curso\|nota` |
| `profesores.txt` | `identificacion\|nombre_completo\|codigo_programa\|tipo_vinculacion\|dedicacion\|categoria_escalafon\|horas_catedra\|ad_honorem\|anios_experiencia\|puntos_titulos\|puntos_productividad\|activo` |
| `administrativos.txt` | `identificacion\|nombre_completo\|cargo\|categoria\|tipo_contratacion\|salario_base\|codigo_facultad\|activo` |

*Normalización de Matrículas:* Los estudiantes se separan en `estudiantes.txt` y `matriculas.txt` para evitar redundancia de datos. Al cargar en memoria, el gestor reconstruye automáticamente la lista anidada en cada objeto `Estudiante`.

### 13.3 Política de Arranque: Carga de Datos vs. Ejecución Limpia (Requisito 11)
En cumplimiento explícito de la **Nota 11 del Taller 1**:
- Al ejecutarse la consola o la GUI, el sistema intercepta el inicio y consulta al usuario:
  `¿Desea cargar los datos existentes? (s/n):`
- **Si el usuario responde 's':** Los 7 archivos son leídos desde `data/`, poblando las colecciones en memoria e informando el número exacto de registros cargados.
- **Si el usuario responde 'n':** El sistema inicia con listas vacías en memoria, permitiendo al evaluador probar la creación de estructuras desde cero sin interferencia de datos previos.

---

# 14. Diseño e Implementación en C++

### 14.1 Estructura del Código Fuente (`cpp/`)
El proyecto en C++ se organiza de forma modular bajo estándares modernos de compilación:
```
cpp/
├── include/
│   ├── entidades.h     # Declaración de structs (TADs) y colecciones vectoriales
│   ├── gestion.h       # Prototipos de operaciones CRUD y reglas académicas
│   ├── nomina.h        # Prototipos de liquidación, aportes y prestaciones
│   ├── persistencia.h  # Prototipos de carga/guardado de texto plano
│   └── interfaz.h      # Utilidades de consola (lectura tecla a tecla, colores)
├── src/
│   ├── gestion.cpp     # Implementación algorítmica del CRUD institucional
│   ├── nomina.cpp      # Motor de cálculo de nómina y desprendibles oficiales
│   ├── persistencia.cpp# Lectura y escritura de flujos fstream
│   ├── interfaz.cpp    # Control multiplataforma de terminal (Windows/Linux)
│   └── main.cpp        # Menú interactivo principal y submenús
├── data/               # Archivos de persistencia (.txt)
└── Makefile            # Automatización de compilación con g++ (C++17)
```

### 14.2 Manejo de Entrada/Salida, Menús y Estética en Consola
Para cumplir con el **criterio estético (Punto 10 del taller)**:
- **Limpieza de Pantalla:** Cada menú limpia la terminal antes de desplegarse (`cls` en Windows, `clear` en POSIX).
- **Pausa Didáctica:** Cada transacción concluye con una pausa (`pausar()`), garantizando que el usuario lea el resultado antes de refrescar el menú.
- **Lectura Directa:** Las opciones se leen al toque de una sola tecla (mediante `_getch()` en Windows con `conio.h` o configuración de terminal en Linux con `termios.h`), sin obligar a digitar ENTER.
- **Confirmación Destructiva:** Cualquier intento de eliminación física exige confirmar con `'s'`/`'n'`.
- **Salida Cómoda:** Presionar ENTER sin digitar opción equivale a *"Volver / Salir"*.

### 14.3 Instrucciones de Compilación y Ejecución
- **Compilar y Ejecutar en Windows (MinGW):**
  ```bash
  cd cpp
  mingw32-make run
  ```
- **Compilar y Ejecutar en Linux / macOS / WSL:**
  ```bash
  cd cpp
  make run
  ```
- **Limpieza de Binarios:** `make clean`

---

# 15. Diseño e Implementación en Python

### 15.1 Estructura del Código Fuente (`python/`)
```
python/
├── src/
│   ├── entidades.py    # Definición de clases (TADs y métodos de cálculo)
│   ├── gestion.py      # Controladores CRUD y validaciones de negocio
│   ├── nomina.py       # Algoritmos de nómina y desprendibles en consola
│   ├── persistencia.py # Serialización y deserialización de archivos .txt
│   ├── interfaz.py     # Manejo de consola interactiva idéntica a C++
│   ├── main.py         # Punto de entrada para consola interactiva
│   ├── gui.py          # Interfaz gráfica de escritorio completa (PitaApp)
│   └── icons/          # Iconos PNG de la suite gráfica institucional
└── data/               # Archivos de persistencia (.txt) sincronizados
```

### 15.2 Interfaz Gráfica de Escritorio (Desktop GUI en Tkinter)
Diseñada como valor agregado de alta calidad para responder al aspecto estético exigido:
- **Pantalla de Bienvenida Dinámica:** Muestra en tiempo real tarjetas con el conteo de facultades, programas, cursos, estudiantes, profesores y administrativos activos.
- **Dock Inferior Institucional:** Barra de navegación rápida con iconos de 64px para acceder a Facultades, Programas, Cursos, Estudiantes, Profesores, Administrativos, Nómina y Salir.
- **Tablas Treeview Modernas:** Despliegue de registros con encabezados en azul marino (`#1F4E79`), selección estilizada y doble clic para consultar.
- **Formularios Modales:** Creación y edición mediante formularios dinámicos con validación de obligatoriedad y chequeo de duplicados en caliente.
- **Desprendible Oficial de Pago Interactivo (`VentanaNomina`):**
  - Selector conmutable **Mensual / Anual**.
  - Tarjetas clasificadas de **Devengados**, **Deducciones de Ley** y **Aportes Patronales UPC**.
  - Banner verde esmeralda con el **Neto a Pagar** destacado.
- **Ejecución:**
  ```bash
  python python/src/gui.py
  ```

### 15.3 Modo Consola Interactivo
Para pruebas en entornos de servidor o terminal pura:
```bash
cd python/src
python main.py
```
Replica exactamente el menú, pausas y flujos de la versión C++.

---

# 16. Casos de Uso Principales (Flujos de Proceso)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   FLUJO DE EJECUCIÓN DEL SISTEMA PITA                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │ ¿Cargar datos previos desde disco? │
                    └─────────────────────────────────────┘
                                  /         \
                             SÍ  /           \  NO
                                ▼             ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │ Carga 7 archivos │  │ Listas en memoria│
                    │   en memoria     │  │ vacías (limpias) │
                    └──────────────────┘  └──────────────────┘
                                \             /
                                 ▼           ▼
                    ┌─────────────────────────────────────┐
                    │      Menú Principal (Consola/GUI)   │
                    │ 1. Facultades     4. Estudiantes    │
                    │ 2. Programas      5. Profesores     │
                    │ 3. Cursos         6. Administrativos│
                    │ 7. Recargar       0. Guardar y Salir│
                    └─────────────────────────────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
 ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
 │ Operaciones CRUD    │    │ Gestión Estudiantil │    │ Gestión Salarial    │
 │ - Crear / Incluir   │    │ - Matricular curso  │    │ - Liquidar docente  │
 │ - Listar / Buscar   │    │ - Registrar nota    │    │ - Liquidar admin    │
 │ - Modificar         │    │ - Calcular promedio │    │ - Desprendible UPC  │
 │ - Desactivar/Borrar │    │ - Alerta EBRA       │    │ - Provisión prestac.│
 └─────────────────────┘    └─────────────────────┘    └─────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │       Guardar Cambios al Salir      │
                    │  (Sobrescritura segura en data/*.txt)│
                    └─────────────────────────────────────┘
```

### CU-01: Matrícula de Curso y Evaluación de Riesgo Académico
1. El usuario selecciona el estudiante mediante su identificación.
2. Ingresa el código del curso a inscribir.
3. El sistema valida que el curso exista y se encuentre activo.
4. El sistema verifica que el estudiante no tenga ya matriculado dicho curso.
5. Se solicita la calificación inicial (o 0.0 si está en curso).
6. El curso se añade a la lista de matrículas del estudiante.
7. El sistema recalcula el promedio aritmético en memoria.
8. Si el nuevo promedio es inferior a 3.25, se genera de inmediato la notificación de **Alerta EBRA**.

### CU-02: Liquidación de Nómina de Docente Ocasional
1. El usuario accede a la ficha del profesor ocasional.
2. El sistema lee su categoría (*Auxiliar, Asistente, Asociado, Titular*) y dedicación (*TC / MT*).
3. Obtiene el factor legal de SMMLV según el Art. 24 del Acuerdo UPC 027 de 2024.
4. Calcula el salario básico multiplicando el factor por el SMMLV 2026 ($1.750.905).
5. Evalúa si posee cualificación de postgrado (Especialización, Maestría o Doctorado) y adiciona la bonificación no salarial del Acuerdo 027.
6. Calcula deducciones de salud (4%) y pensión (4%) con redondeo PILA a centenas.
7. Si el salario supera 4 SMMLV, liquida el 1% de Fondo de Solidaridad Pensional.
8. Aplica el 0.2% de Estampilla Pro-UPC y la Retención en la Fuente si excede 95 UVT.
9. Totaliza los aportes patronales que debe asumir la UPC (Pensión 12%, Salud 8.5%, ARL 0.522%, Caja 4%).
10. Proyecta las provisiones mensuales de cesantías, primas y vacaciones.
11. Despliega el desprendible oficial de pago con el neto a pagar.

---

# 17. Verificación, Pruebas y Resultados

Para certificar el correcto funcionamiento del sistema, se ejecutó una batería completa de pruebas funcionales y de límites con resultados idénticos entre C++ y Python:

| ID | Escenario de Prueba | Datos de Entrada | Comportamiento Esperado | Resultado C++ | Resultado Python | Estado |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **PR-01** | Unicidad de Claves | Crear dos facultades con código `FIS` | Rechazar segundo registro informando código duplicado | Rechazado | Rechazado | **CORRECTO** |
| **PR-02** | Integridad Foránea | Crear curso asignado a programa inexistente `XYZ` | Bloquear creación hasta que el programa padre exista | Bloqueado | Bloqueado | **CORRECTO** |
| **PR-03** | Matrícula Doble | Matricular dos veces el curso `EDD1` al estudiante `1065800001` | Rechazar la segunda matrícula indicando curso ya inscrito | Rechazado | Rechazado | **CORRECTO** |
| **PR-04** | Caso Límite EBRA | Estudiante con notas que dan promedio exacto de **3.25** | **NO activar alerta** (regla estricta: menor que 3.25) | Sin alerta | Sin alerta | **CORRECTO** |
| **PR-05** | Caso Activo EBRA | Estudiante con notas que dan promedio de **3.24** | **Activar alerta EBRA** por riesgo de deserción | Alerta activa | Alerta activa | **CORRECTO** |
| **PR-06** | Estudiante Nuevo | Estudiante recién creado sin ninguna materia cursada | Promedio 0.0 y **sin alerta EBRA** (no es falso positivo) | Sin alerta | Sin alerta | **CORRECTO** |
| **PR-07** | Nómina Planta | Titular TC, 178 pregrado + 96 escalafón + 60 títulos + 20 product. = 354 pts | Bruto: $354 \times 23.924 = \$8.469.096\text{ COP}$; Neto: $\$7.524.858\text{ COP}$ | $\$7.524.858$ | $\$7.524.858$ | **CORRECTO** |
| **PR-08** | Nómina Ocasional | Asistente TC ($3.125\text{ SMMLV}$) con Doctorado ($0.90\text{ SMMLV}$) | Básico: $\$5.471.578$; Bonif: $\$1.575.815$; Devengado: $\$7.047.393\text{ COP}$ | $\$7.047.393$ | $\$7.047.393$ | **CORRECTO** |
| **PR-09** | Catedrático Ad-Honorem | Profesor Catedrático con bandera `adHonorem = true` | Salario bruto y neto exactamente iguales a $\$0\text{ COP}$ | $\$0\text{ COP}$ | $\$0\text{ COP}$ | **CORRECTO** |
| **PR-10** | Escala Administrativa | Administrativo Nivel 2 con salario base ingresado en 0 | Asignación automática por escala legal a $\$2.800.000\text{ COP}$ | $\$2.800.000$ | $\$2.800.000$ | **CORRECTO** |
| **PR-11** | Persistencia Cruzada | Guardar datos desde C++ y cargarlos en Python (y viceversa) | Carga íntegra sin fallos de conversión ni pérdidas de campos | 100% fiel | 100% fiel | **CORRECTO** |
| **PR-12** | Arranque sin Datos | Responder 'n' a la carga inicial | Sistema inicia con listas vacías sin errores | Verificado | Verificado | **CORRECTO** |

---

# 18. Matriz de Cumplimiento de los Parámetros del Taller 1

A continuación se presenta la tabla de auditoría frente a cada uno de los parámetros y directrices dictadas en la guía del Taller 1:

| Ítem del Taller | Parámetro Solicitado en la Guía | Evidencia Concreta en el Proyecto PITA | Estado |
| :---: | :--- | :--- | :---: |
| **1** | Gestionar un conjunto de facultades. | TAD `Facultad`, CRUD en `gestion.cpp` y `gestion.py`, vista dedicada en GUI. | **100% CUMPLIDO** |
| **2** | Para cada facultad gestionar un conjunto de programas. | TAD `Programa` con clave foránea `codigo_facultad` y validación de existencia. | **100% CUMPLIDO** |
| **3** | Para cada programa gestionar cursos, estudiantes y profesores. | Relaciones jerárquicas modeladas y validadas en C++ y Python. | **100% CUMPLIDO** |
| **4** | Gestionar información personal y de nómina de cada profesor. | TAD `Profesor` con escalafón, vinculación, dedicación, posgrado y puntos. | **100% CUMPLIDO** |
| **5** | Nómina de planta, ocasionales y catedráticos (Dec. 1279 y Ac. 027). | Módulos `nomina.cpp` y `nomina.py` con fórmulas exactas por régimen. | **100% CUMPLIDO** |
| **6** | Identificar variables de entrada y salida (académica y nómina). | Capítulo 10 de este documento detalla formalmente cada variable. | **100% CUMPLIDO** |
| **7** | Estructura adaptada a la universidad, Dec. 1279 y Ac. 027/2024. | Entidades con campos para puntos, escalafón, dedicación y posgrados. | **100% CUMPLIDO** |
| **8** | CRUD completo para profesor, estudiante y administrativo (categoría y contratación). | Funciones de crear, incluir, consultar, modificar, desactivar y eliminar en ambos lenguajes. | **100% CUMPLIDO** |
| **9** | Simular cálculo de salario de nómina según normatividad. | Motores de cálculo en C++ y Python con desprendibles auditables UPC. | **100% CUMPLIDO** |
| **10** | Cuidado del aspecto estético. | Consola ergonómica con limpieza de pantalla y GUI desktop profesional en Tkinter. | **100% CUMPLIDO** |
| **11** | Gerenciar información académica de los estudiantes. | Consulta de ficha del estudiante, estado curricular y registro histórico. | **100% CUMPLIDO** |
| **12** | Matricular, cancelar curso, promedios y alerta EBRA. | Métodos `matricularCurso`, `cancelarCurso`, promedio y alerta `< 3.25`. | **100% CUMPLIDO** |
| **13** | Nómina con descuentos de ley y prestaciones sociales. | Deducciones PILA (salud, pensión, FSP, retefuente) y 7 provisiones prestacionales. | **100% CUMPLIDO** |
| **Nota 1** | Entrega de versiones en C++ y Python. | Carpetas independientes `cpp/` y `python/` con código modular equivalente. | **100% CUMPLIDO** |
| **Nota 2** | Documento Word formal con diseño, estrategia y diagramas. | Documentación maestra exportada en formato `.docx` y `.md`. | **100% CUMPLIDO** |
| **Nota 9** | Archivo de texto para persistencia de datos. | 7 archivos `.txt` delimitados por tubería (`\|`) en directorio `data/`. | **100% CUMPLIDO** |
| **Nota 10**| El programa debe cargar y guardar datos en archivo. | Módulos `persistencia.cpp` y `persistencia.py` sincronizados al salir. | **100% CUMPLIDO** |
| **Nota 11**| El usuario decide si cargar datos o iniciar sin datos. | Pregunta obligatoria en arranque en consola y panel inicial en GUI. | **100% CUMPLIDO** |

---

# 19. Conclusiones

1. **Eficacia del Modelo Basado en Listas:** Se demostró que las colecciones dinámicas secuenciales (`std::vector` en C++ y `list` en Python), combinadas con el encapsulamiento de Tipos Abstractos de Datos, son plenamente capaces de resolver la complejidad transaccional de un sistema universitario completo sin depender de motores de bases de datos relacionales externos.
2. **Coherencia e Interoperabilidad Multiplataforma:** La adopción rigurosa de un estándar común de persistencia en texto plano (`|`) y estructuras en espejo permitió que ambas versiones (C++ compilado nativo y Python interpretado) compartan exactamente la misma semántica de negocio y manipulen los mismos archivos de datos de forma indistinta.
3. **Rigor Normativo Institucional:** La traducción algorítmica del Decreto 1279 de 2002, Acuerdo UPC 027 de 2024 y decretos salariales vigentes de 2026 convirtió al módulo de nómina en un simulador fidedigno, distinguiendo con precisión los regímenes salariales de planta, ocasionales, catedráticos y administrativos.
4. **Impacto Académico del Algoritmo EBRA:** La detección preventiva de bajo rendimiento académico basada en el umbral de 3.25 aporta una herramienta de valor directo a la gestión universitaria para mitigar la deserción estudiantil.
5. **Calidad de la Experiencia de Usuario:** La implementación de dos interfaces (una consola interactiva de alta ergonomía y una aplicación gráfica de escritorio con estética moderna) cumple con creces la exigencia estética del taller, facilitando la evaluación técnica y la interacción con el usuario final.

---

# 20. Referencias Documentales y Normativas

1. **Universidad Popular del Cesar.** *Taller 1 de Estructura de Datos: Listas*. Facultad de Ingenierías y Tecnológicas, Programa de Ingeniería de Sistemas, 2026.
2. **Universidad Popular del Cesar.** *Acuerdo No. 027 del 31 de octubre de 2024*. Por el cual se expide el Estatuto del Profesor Universitario de la Universidad Popular del Cesar (Régimen de vinculación de docentes ocasionales y catedráticos).
3. **República de Colombia — Presidencia de la República.** *Decreto 1279 de 2002*. Por el cual se establece el régimen salarial y prestacional de los docentes de las Universidades Estatales.
4. **República de Colombia — Presidencia de la República.** *Decreto 318 de 2026*. Por el cual se fija el valor del punto salarial para los docentes universitarios en la vigencia 2026 ($23.924 COP).
5. **República de Colombia — Presidencia de la República.** *Decreto 159 de 2026*. Por el cual se fija el Salario Mínimo Legal Mensual Vigente ($1.750.905 COP).
6. **República de Colombia — Congreso de la República.** *Ley 100 de 1993*. Por la cual se crea el sistema de seguridad social integral (Aportes a salud y pensión).
7. **República de Colombia — Congreso de la República.** *Ley 52 de 1975*. Régimen de intereses sobre cesantías a favor de los trabajadores.
8. **República de Colombia — Presidencia de la República.** *Decreto 1042 de 1978*. Normas generales sobre administración y remuneración de servidores públicos (Prima de Navidad y Bonificación por servicios).
9. **República de Colombia — Presidencia de la República.** *Decreto 1990 de 2016*. Reglas para el recaudo y redondeo de aportes en la Planilla Integrada de Liquidación de Aportes (PILA).
10. **Ministerio del Trabajo de Colombia.** *Herramienta Mi Calculadora Laboral*. https://www.mintrabajo.gov.co
