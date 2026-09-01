"""Persistencia en texto plano delimitado por '|'.
Mismo formato que la version C++ (ver docs/formato_persistencia.md),
para que los archivos de datos sean intercambiables entre ambas versiones."""

import os
from entidades import Facultad


def guardar_facultades(facultades, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for f in facultades:
            archivo.write(f"{f.codigo}|{f.nombre}|{f.decano}|{1 if f.activo else 0}\n")


def cargar_facultades(ruta):
    resultado = []
    if not os.path.exists(ruta):
        return resultado  # no es un error, simplemente no hay datos aun
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 4:
                continue  # linea corrupta, se ignora
            codigo, nombre, decano, activo = campos[0], campos[1], campos[2], campos[3]
            resultado.append(Facultad(codigo, nombre, decano, activo == "1"))
    return resultado


# TODO: implementar guardar/cargar para Programa, Curso, Estudiante
# (con matriculas), Profesor y Administrativo, siguiendo el mismo patron.
