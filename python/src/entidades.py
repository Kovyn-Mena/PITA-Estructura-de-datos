"""Clases de entidades del sistema PITA (TADs Académicos).
Estructura diseñada en espejo con la versión de C++ (mismos campos y tipos),
garantizando la coherencia conceptual del modelo de datos en ambos lenguajes.
"""


class Facultad:
    """TAD Facultad: Unidad académica mayor que agrupa programas."""
    def __init__(self, codigo, nombre, decano, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.decano = decano
        self.activo = activo  # Control de borrado lógico

    def __str__(self):
        estado = "Activa" if self.activo else "Inactiva"
        return f"{self.codigo} | {self.nombre} | Decano: {self.decano} | {estado}"


class Programa:
    """TAD Programa: Programa académico adscrito a una facultad."""
    def __init__(self, codigo, nombre, nivel, codigo_facultad, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.nivel = nivel  # Tecnológico, Pregrado, Especialización, Maestría
        self.codigo_facultad = codigo_facultad
        self.activo = activo


class Curso:
    """TAD Curso: Asignatura perteneciente a un programa y asignada a un docente."""
    def __init__(self, codigo, nombre, creditos, codigo_profesor, codigo_programa, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.codigo_profesor = codigo_profesor
        self.codigo_programa = codigo_programa
        self.activo = activo


class Estudiante:
    """TAD Estudiante: Alumno matriculado en un programa académico.
    Contiene la lista anidada de asignaturas cursadas y calificaciones.
    """
    def __init__(self, identificacion, nombre_completo, codigo_programa, estado="Activo", activo=True):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.codigo_programa = codigo_programa
        self.estado = estado  # Activo, Inactivo, Graduado
        self.activo = activo
        self.matriculas = []  # Lista anidada de dicts: {"codigo_curso": str, "nota": float}

    def calcular_promedio(self):
        """Calcula el promedio aritmético ponderado simple de las notas registradas."""
        if not self.matriculas:
            return 0.0
        notas = [m["nota"] for m in self.matriculas]
        return sum(notas) / len(notas)

    def esta_en_riesgo_ebra(self, umbral=3.25):
        """Determina si el estudiante se encuentra en Evaluación de Bajo Rendimiento Académico (EBRA).
        Criterio: Promedio acumulado inferior a 3.25 (sin asignaturas no genera alerta).
        """
        if not self.matriculas:
            return False
        return self.calcular_promedio() < umbral


class Profesor:
    """TAD Profesor: Docente universitario con información contractual y salarial.
    Soporta los tres regímenes legales: Planta (Dec. 1279), Ocasional y Catedrático (Acuerdo 027).
    """
    def __init__(self, identificacion, nombre_completo, codigo_programa,
                 tipo_vinculacion, dedicacion, categoria_escalafon="",
                 horas_catedra_semanales=0, ad_honorem=False,
                 anios_experiencia=0, puntos_titulos=0, puntos_productividad=0,
                 activo=True, posgrado=""):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.codigo_programa = codigo_programa
        self.tipo_vinculacion = tipo_vinculacion    # Planta, Ocasional, Catedratico
        self.dedicacion = dedicacion                # TiempoCompleto, MedioTiempo, HorasCatedra
        self.categoria_escalafon = categoria_escalafon  # Auxiliar, Asistente, Asociado, Titular
        self.horas_catedra_semanales = horas_catedra_semanales
        self.ad_honorem = ad_honorem
        self.anios_experiencia = anios_experiencia
        self.puntos_titulos = puntos_titulos
        self.puntos_productividad = puntos_productividad
        self.activo = activo
        self.posgrado = posgrado  # Ninguno, Especializacion, Maestria, Doctorado


class Administrativo:
    """TAD Administrativo: Servidor público o contratista del área administrativa."""
    def __init__(self, identificacion, nombre_completo, cargo, categoria,
                 tipo_contratacion, salario_base, codigo_facultad="", activo=True):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.cargo = cargo
        self.categoria = categoria  # Nivel 1, Nivel 2, Nivel 3, Nivel 4
        self.tipo_contratacion = tipo_contratacion  # Planta, Provisional, Contrato
        self.salario_base = salario_base
        self.codigo_facultad = codigo_facultad  # Vacio = nivel central (ej. Rectoria)
        self.activo = activo
