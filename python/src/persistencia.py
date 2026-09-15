"""Módulo de Persistencia en Texto Plano delimitado por '|'.
Garantiza que los archivos en data/ sean 100% intercambiables entre Python y C++.
Formato documentado en docs/formato_persistencia.md.
"""

import os
from entidades import Facultad, Programa, Curso, Estudiante, Profesor, Administrativo


# ============================ FACULTADES ============================

def guardar_facultades(facultades, ruta):
    """Serializa la lista de facultades en disco con formato pipe-delimited."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        for f in facultades:
            archivo.write(f"{f.codigo}|{f.nombre}|{f.decano}|{1 if f.activo else 0}\n")


def cargar_facultades(ruta):
    """Deserializa las facultades desde archivo. Si no existe, retorna lista vacía."""
    resultado = []
    if not os.path.exists(ruta):
        return resultado
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 4:
                continue  # Línea corrupta o incompleta, se omite
            codigo, nombre, decano, activo = campos[0], campos[1], campos[2], campos[3]
            resultado.append(Facultad(codigo, nombre, decano, activo == "1"))
    return resultado


# ============================ PROGRAMAS ============================

def guardar_programas(programas, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for p in programas:
            archivo.write(f"{p.codigo}|{p.nombre}|{p.nivel}|{p.codigo_facultad}|"
                          f"{1 if p.activo else 0}\n")


def cargar_programas(ruta):
    resultado = []
    if not os.path.exists(ruta):
        return resultado
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 5:
                continue
            codigo, nombre, nivel, codigo_facultad, activo = campos[0], campos[1], campos[2], campos[3], campos[4]
            resultado.append(Programa(codigo, nombre, nivel, codigo_facultad, activo == "1"))
    return resultado


# ============================ CURSOS ============================

def guardar_cursos(cursos, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for c in cursos:
            dia = getattr(c, "dia", "")
            h_ini = getattr(c, "hora_inicio", 0)
            h_fin = getattr(c, "hora_fin", 0)
            salon = getattr(c, "salon", "")
            archivo.write(f"{c.codigo}|{c.nombre}|{c.creditos}|{c.codigo_profesor}|"
                          f"{c.codigo_programa}|{1 if c.activo else 0}|{dia}|{h_ini}|{h_fin}|{salon}\n")


def cargar_cursos(ruta):
    resultado = []
    if not os.path.exists(ruta):
        return resultado
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 6:
                continue
            codigo, nombre, creditos, codigo_profesor, codigo_programa, activo = campos[:6]
            dia = campos[6] if len(campos) > 6 else ""
            h_ini = int(campos[7]) if len(campos) > 7 and campos[7] else 0
            h_fin = int(campos[8]) if len(campos) > 8 and campos[8] else 0
            salon = campos[9] if len(campos) > 9 else ""
            resultado.append(Curso(codigo, nombre, int(creditos), codigo_profesor,
                                   codigo_programa, activo == "1",
                                   dia=dia, hora_inicio=h_ini, hora_fin=h_fin, salon=salon))
    return resultado


# ============================ ESTUDIANTES ============================
# Se guardan en DOS archivos: uno con los datos del estudiante, otro con
# la relacion estudiante-curso-nota (matriculas). Se separan para no
# repetir el nombre del estudiante en cada linea de matricula.

def guardar_estudiantes(estudiantes, ruta_est, ruta_matriculas):
    with open(ruta_est, "w", encoding="utf-8") as archivo:
        for e in estudiantes:
            archivo.write(f"{e.identificacion}|{e.nombre_completo}|{e.codigo_programa}|"
                          f"{e.estado}|{1 if e.activo else 0}\n")

    with open(ruta_matriculas, "w", encoding="utf-8") as archivo:
        for e in estudiantes:
            for m in e.matriculas:
                archivo.write(f"{e.identificacion}|{m['codigo_curso']}|{m['nota']}\n")


def cargar_estudiantes(ruta_est, ruta_matriculas):
    resultado = []
    if not os.path.exists(ruta_est):
        return resultado

    with open(ruta_est, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 5:
                continue
            identificacion, nombre, codigo_programa, estado, activo = campos
            resultado.append(Estudiante(identificacion, nombre, codigo_programa,
                                         estado, activo == "1"))

    # Segunda pasada: cargar matriculas y asociarlas al estudiante correcto (O(1) por hash map)
    if os.path.exists(ruta_matriculas):
        mapa_estudiantes = {e.identificacion: e for e in resultado}
        with open(ruta_matriculas, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                campos = linea.split("|")
                if len(campos) < 3:
                    continue
                id_estudiante, codigo_curso, nota = campos
                e = mapa_estudiantes.get(id_estudiante)
                if e is not None:
                    e.matriculas.append({"codigo_curso": codigo_curso, "nota": float(nota)})
        del mapa_estudiantes

    return resultado


# ============================ PROFESORES ============================

def guardar_profesores(profesores, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for p in profesores:
            posg = getattr(p, "posgrado", "")
            archivo.write(
                f"{p.identificacion}|{p.nombre_completo}|{p.codigo_programa}|"
                f"{p.tipo_vinculacion}|{p.dedicacion}|{p.categoria_escalafon}|"
                f"{p.horas_catedra_semanales}|{1 if p.ad_honorem else 0}|"
                f"{p.anios_experiencia}|{p.puntos_titulos}|{p.puntos_productividad}|"
                f"{1 if p.activo else 0}|{posg}\n"
            )


def cargar_profesores(ruta):
    resultado = []
    if not os.path.exists(ruta):
        return resultado
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 12:
                continue
            resultado.append(Profesor(
                identificacion=campos[0],
                nombre_completo=campos[1],
                codigo_programa=campos[2],
                tipo_vinculacion=campos[3],
                dedicacion=campos[4],
                categoria_escalafon=campos[5],
                horas_catedra_semanales=int(campos[6]),
                ad_honorem=(campos[7] == "1"),
                anios_experiencia=int(campos[8]),
                puntos_titulos=int(campos[9]),
                puntos_productividad=int(campos[10]),
                activo=(campos[11] == "1"),
                posgrado=campos[12] if len(campos) >= 13 else "",
            ))
    return resultado


# ============================ ADMINISTRATIVOS ============================

def guardar_administrativos(admins, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for a in admins:
            archivo.write(
                f"{a.identificacion}|{a.nombre_completo}|{a.cargo}|{a.categoria}|"
                f"{a.tipo_contratacion}|{a.salario_base}|{a.codigo_facultad}|"
                f"{1 if a.activo else 0}\n"
            )


def cargar_administrativos(ruta):
    resultado = []
    if not os.path.exists(ruta):
        return resultado
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            campos = linea.split("|")
            if len(campos) < 8:
                continue
            identificacion, nombre, cargo, categoria, tipo_contratacion, salario_base, codigo_facultad, activo = campos
            resultado.append(Administrativo(
                identificacion, nombre, cargo, categoria, tipo_contratacion,
                float(salario_base), codigo_facultad, activo == "1"
            ))
    return resultado
