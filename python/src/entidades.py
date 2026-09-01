"""Clases de entidades del sistema PITA. Estructura pensada en espejo con
la version de C++ (mismos campos), para que el diseno conceptual sea el mismo
en ambos lenguajes."""


class Facultad:
    def __init__(self, codigo, nombre, decano, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.decano = decano
        self.activo = activo

    def __str__(self):
        estado = "Activa" if self.activo else "Inactiva"
        return f"{self.codigo} | {self.nombre} | Decano: {self.decano} | {estado}"


class Programa:
    def __init__(self, codigo, nombre, nivel, codigo_facultad, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.nivel = nivel  # Tecnologico, Pregrado, Especializacion, Maestria
        self.codigo_facultad = codigo_facultad
        self.activo = activo


class Curso:
    def __init__(self, codigo, nombre, creditos, codigo_profesor, codigo_programa, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.codigo_profesor = codigo_profesor
        self.codigo_programa = codigo_programa
        self.activo = activo


class Estudiante:
    def __init__(self, identificacion, nombre_completo, codigo_programa, estado="Activo", activo=True):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.codigo_programa = codigo_programa
        self.estado = estado
        self.activo = activo
        self.matriculas = []  # lista de dicts: {"codigo_curso": ..., "nota": ...}

    def calcular_promedio(self):
        if not self.matriculas:
            return 0.0
        notas = [m["nota"] for m in self.matriculas]
        return sum(notas) / len(notas)

    def esta_en_riesgo_ebra(self, umbral=3.25):
        return self.calcular_promedio() < umbral


class Profesor:
    def __init__(self, identificacion, nombre_completo, codigo_programa,
                 tipo_vinculacion, dedicacion, categoria_escalafon="",
                 horas_catedra_semanales=0, ad_honorem=False,
                 anios_experiencia=0, puntos_titulos=0, puntos_productividad=0,
                 activo=True):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.codigo_programa = codigo_programa
        self.tipo_vinculacion = tipo_vinculacion    # Planta, Ocasional, Catedratico
        self.dedicacion = dedicacion                # TiempoCompleto, MedioTiempo, HorasCatedra
        self.categoria_escalafon = categoria_escalafon
        self.horas_catedra_semanales = horas_catedra_semanales
        self.ad_honorem = ad_honorem
        self.anios_experiencia = anios_experiencia
        self.puntos_titulos = puntos_titulos
        self.puntos_productividad = puntos_productividad
        self.activo = activo


class Administrativo:
    def __init__(self, identificacion, nombre_completo, cargo, categoria,
                 tipo_contratacion, salario_base, activo=True):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.cargo = cargo
        self.categoria = categoria
        self.tipo_contratacion = tipo_contratacion
        self.salario_base = salario_base
        self.activo = activo
