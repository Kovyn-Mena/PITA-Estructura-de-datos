# PITA — Programa Integrado de Transacciones Académicas
## Día 1: Diseño conceptual, entidades y normatividad

---

## 1. Normatividad aplicada (base para el módulo de nómina)

### Acuerdo 027 del 31 de octubre de 2024 (UPC) — define TIPOS DE CONTRATACIÓN
No trae fórmulas salariales; regula cómo se vincula el personal docente no-planta:

| Tipo de profesor | Dedicación | Duración vinculación | Naturaleza |
|---|---|---|---|
| **Planta (carrera)** | Tiempo completo / medio tiempo | Indefinida (concurso de méritos) | Empleado público docente |
| **Ocasional** | Tiempo completo o medio tiempo | Periodos inferiores a 1 año | No es empleado público ni trabajador oficial |
| **Catedrático** | Hasta 18 horas semanales | Periodos semestrales | No es empleado público; puede ser ad-honorem (sin remuneración) |

### Decreto 1279 de 2002 — define el CÁLCULO SALARIAL (aplica a planta; se usa como base simulada también para ocasionales/catedráticos de forma proporcional, tal como indica el propio decreto)

**Fórmula base:**
```
Salario mensual = (Σ puntos del docente) × (valor del punto)
```

**Puntos por categoría en el escalafón (Art. 8):**
| Categoría | Puntos |
|---|---|
| Instructor / Profesor Auxiliar | 37 |
| Profesor Asistente | 58 |
| Profesor Asociado | 74 |
| Profesor Titular | 96 |

**Otros factores que suman puntos (Art. 6-7, simplificables para la simulación):**
- Títulos académicos (pregrado, especialización, maestría, doctorado)
- Experiencia calificada (años de servicio × factor según categoría)
- Productividad académica (publicaciones, investigación)

**Valor del punto:** es un valor fijado anualmente por el Gobierno Nacional (para 2024 fue de $20.895 COP). Para el programa lo dejamos como **parámetro configurable**, no hardcodeado, ya que cambia cada año.

**Proporcionalidad (Parágrafo Art. 6):** para dedicaciones distintas a tiempo completo (medio tiempo, cátedra por horas), el salario se calcula de forma proporcional a la dedicación.

**Deducciones de nómina** (según Mintrabajo — simuladas con porcentajes estándar de ley):
- Salud: 4% (aporte empleado)
- Pensión: 4% (aporte empleado)
- Prestaciones sociales: se calculan aparte (prima, cesantías, intereses de cesantías) — se pueden mostrar como valores informativos, no como descuento del neto.

> **Nota para el video:** aquí es clave decir explícitamente "simulamos un modelo simplificado basado en el Decreto 1279 y el Acuerdo 027, sin pretender replicar el cálculo exacto que hace el Comité Interno de Asignación de Puntaje (CIARP)". Eso demuestra que entendiste la normativa sin sobre-prometer precisión legal.

---

## 2. Entidades del sistema (jerarquía)

```
Universidad
 └── Facultad (N)
      └── Programa Académico (N)
           ├── Curso (N)
           ├── Estudiante (N)  [matriculado en el programa]
           └── Profesor (N)    [asignado a cursos del programa]

Administrativo (N) — asociado a Facultad o a nivel central, no depende de Programa
```

### 2.1 Facultad
| Campo | Tipo |
|---|---|
| codigo_facultad | string (PK) |
| nombre | string |
| decano | string |
| activo | bool |
| lista_programas | lista de Programa |

### 2.2 Programa Académico
| Campo | Tipo |
|---|---|
| codigo_programa | string (PK) |
| nombre | string |
| nivel | enum {Tecnológico, Pregrado, Especialización, Maestría} |
| codigo_facultad | string (FK) |
| activo | bool |
| lista_cursos, lista_estudiantes, lista_profesores | listas |

### 2.3 Curso
| Campo | Tipo |
|---|---|
| codigo_curso | string (PK) |
| nombre | string |
| creditos | int |
| codigo_profesor | string (FK) |
| activo | bool |

### 2.4 Estudiante
| Campo | Tipo |
|---|---|
| identificacion | string (PK) |
| nombre_completo | string |
| codigo_programa | string (FK) |
| cursos_matriculados | lista de {codigo_curso, nota} |
| promedio_acumulado | float (calculado) |
| estado | enum {Activo, Inactivo, Graduado} |
| en_riesgo_ebra | bool (calculado: promedio < 3.25) |

**Regla EBRA:** si `promedio_acumulado < 3.25` → se dispara alerta de riesgo de deserción académica.

### 2.5 Profesor (clase base) → especializado por tipo de vinculación
| Campo | Tipo |
|---|---|
| identificacion | string (PK) |
| nombre_completo | string |
| codigo_programa | string (FK) |
| tipo_vinculacion | enum {Planta, Ocasional, Catedrático} |
| dedicacion | enum {Tiempo completo, Medio tiempo, Horas cátedra} |
| categoria_escalafon | enum {Auxiliar, Asistente, Asociado, Titular} (solo aplica si es Planta u Ocasional con escalafón) |
| horas_catedra_semanales | int (solo si tipo = Catedrático, máx. 18) |
| es_ad_honorem | bool (solo si tipo = Catedrático) |
| titulos | lista {tipo_titulo, puntos_asociados} |
| anios_experiencia | int |
| puntos_productividad | int |
| activo | bool |

### 2.6 Administrativo
| Campo | Tipo |
|---|---|
| identificacion | string (PK) |
| nombre_completo | string |
| cargo | string |
| categoria | string |
| tipo_contratacion | enum {Planta, Provisional, Contrato} |
| salario_base | float |
| codigo_facultad | string (FK, OPCIONAL — vacio = nivel central, ej. Rectoria) |
| activo | bool |

---

## 3. Variables de entrada y salida

### 3.1 Modelo académico (estructura general)
**Entradas:** datos de identificación de facultad/programa/curso/estudiante/profesor/administrativo; matrícula de curso (id estudiante + id curso); notas por curso.
**Salidas:** listados por facultad/programa; promedio del estudiante; alerta EBRA (bool + mensaje); confirmación de operaciones CRUD; archivo persistido.

### 3.2 Modelo salarial (cálculo de nómina)
**Entradas:**
- tipo_vinculacion, categoría del escalafón, dedicación
- puntos por títulos, puntos por experiencia, puntos por productividad
- valor_del_punto (parámetro configurable, ej. $20.895 año base 2024)
- horas_catedra_semanales (si aplica)

**Salidas:**
- total_puntos
- salario_bruto = total_puntos × valor_del_punto (proporcional si no es TC)
- descuento_salud (4%)
- descuento_pension (4%)
- salario_neto
- valores informativos de prestaciones sociales (prima, cesantías)

---

## 4. Operaciones CRUD estándar (por cada TAD)
Para Facultad, Programa, Curso, Estudiante, Profesor y Administrativo, todas deben implementar:
1. Crear
2. Incluir (agregar a la lista contenedora)
3. Eliminar (borrado físico)
4. Desactivar (borrado lógico → campo `activo = false`, se conserva el registro)
5. Consultar (por código/id, y listar todos)
6. Modificar (editar campos)
7. Persistir (guardar/cargar desde archivo)

---

## 5. Decisiones de diseño confirmadas
- **Estructuras de listas:** libres — se usarán vectores/listas nativas de cada lenguaje (no listas enlazadas manuales), documentando la decisión en el Word.
- **Nivel C++:** structs + vectores + funciones, sin punteros manuales, sin plantillas, sin herencia compleja.
- **Python:** clases simples con listas/diccionarios.
- **Persistencia:** archivo de texto plano (más simple de depurar y de explicar en el video) para la primera versión; se puede migrar a binario si sobra tiempo.
- **EBRA:** promedio_acumulado < 3.25 → alerta automática al consultar o actualizar el estudiante.
- **Interfaz de consola:** cada menú limpia la pantalla antes de dibujarse (`system("cls")`/`system("clear")` según el sistema operativo) y hace una pausa ("Presione ENTER para continuar") después de cada acción, para no perder información en pantalla pero mantenerla ordenada. Las confirmaciones tipo s/n se leen con una sola tecla, sin esperar ENTER, usando `conio.h` en Windows y `termios.h` en Linux/Mac. Ver `cpp/include/interfaz.h`.

---

## 6. Pendiente para Día 2
- Diagrama de clases/estructuras (UML simplificado o diagrama de cajas)
- Definir formato exacto del archivo de persistencia (delimitadores, orden de campos)
- Esqueleto de carpetas del proyecto (para ambos lenguajes)
