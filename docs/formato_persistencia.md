# Formato de persistencia — PITA

Se usa **texto plano delimitado por `|`**, un registro por línea, un archivo por entidad.
Se eligió texto plano (no binario) porque es fácil de inspeccionar, depurar y explicar en el video.

Carpeta de datos: `data/` (dentro de cada proyecto, cpp y python). Ambos lenguajes leen/escriben
el **mismo formato**, así que en teoría los archivos de datos son intercambiables entre las dos versiones.

## facultades.txt
```
codigo|nombre|decano|activo
FIS|Facultad de Ingenierías y Tecnológicas|Nombre Decano|1
```

## programas.txt
```
codigo|nombre|nivel|codigo_facultad|activo
SIS|Ingeniería de Sistemas|Pregrado|FIS|1
```
`nivel` ∈ {Tecnologico, Pregrado, Especializacion, Maestria}

## cursos.txt
```
codigo|nombre|creditos|codigo_profesor|codigo_programa|activo
EDD1|Estructura de Datos|3|P001|SIS|1
```

## estudiantes.txt
```
identificacion|nombre_completo|codigo_programa|estado|activo
1065800001|Juan Perez|SIS|Activo|1
```

## matriculas.txt
(relación estudiante–curso con nota; separado para no repetir datos del estudiante)
```
identificacion_estudiante|codigo_curso|nota
1065800001|EDD1|4.2
```
El promedio y la alerta EBRA se calculan en memoria a partir de este archivo, no se guardan
como campo fijo (para evitar inconsistencias si cambian las notas).

## profesores.txt
```
identificacion|nombre_completo|codigo_programa|tipo_vinculacion|dedicacion|categoria_escalafon|horas_catedra|ad_honorem|anios_experiencia|puntos_titulos|puntos_productividad|activo
P001|Maria Lopez|SIS|Planta|TiempoCompleto|Asociado|0|0|8|60|15|1
```
`tipo_vinculacion` ∈ {Planta, Ocasional, Catedratico}
`dedicacion` ∈ {TiempoCompleto, MedioTiempo, HorasCatedra}

## administrativos.txt
```
identificacion|nombre_completo|cargo|categoria|tipo_contratacion|salario_base|activo
A001|Carlos Ruiz|Secretario Academico|Nivel 2|Planta|2500000|1
```

## Reglas comunes
- El campo `activo` es 1/0 y representa el **borrado lógico** (desactivar). El borrado físico
  (eliminar) sí quita la línea del archivo.
- Todas las claves primarias (`codigo`, `identificacion`) deben ser únicas dentro de su archivo.
- Si un archivo no existe al iniciar el programa, se crea vacío (no es un error).
- El programa siempre pregunta al inicio: **cargar datos existentes o iniciar sin datos**
  (requisito explícito del taller).
