"""PITA - Interfaz grafica (bono y Parcial 1 completo)
Universidad Popular del Cesar

Reutiliza integramente la logica ya probada en entidades.py, persistencia.py,
gestion.py (funciones de busqueda), nomina.py y generador.py. Esta capa SOLO agrega la
presentacion visual y la optimizacion de renderizado; ninguna regla de negocio se reescribe aqui.

Ejecutar con: python gui.py (desde python/src)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import sys

# Habilitar DPI Awareness en Windows para que las fuentes y botones no se recorten
if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

from entidades import Facultad, Programa, Curso, Estudiante, Profesor, Administrativo
from persistencia import (
    guardar_facultades, cargar_facultades,
    guardar_programas, cargar_programas,
    guardar_cursos, cargar_cursos,
    guardar_estudiantes, cargar_estudiantes,
    guardar_profesores, cargar_profesores,
    guardar_administrativos, cargar_administrativos,
)
from gestion import (
    buscar_facultad, buscar_programa, buscar_curso,
    buscar_estudiante, buscar_profesor, buscar_administrativo,
)
from nomina import (
    calcular_salario_bruto, calcular_bonificacion_posgrado, calcular_total_devengado,
    calcular_descuento_salud, calcular_descuento_pension, calcular_descuento_fsp,
    calcular_descuento_estampilla, calcular_retencion_fuente, calcular_total_deducciones,
    calcular_salario_neto, calcular_prima_servicios, calcular_cesantias,
    calcular_intereses_cesantias, calcular_prima_navidad,
    calcular_vacaciones, calcular_prima_vacaciones, calcular_bonificacion_servicios,
    calcular_total_prestaciones, calcular_aportes_patronales, calcular_costo_total_empleador,
    total_puntos, puntos_por_categoria, factor_proporcionalidad, factor_ocasional,
    regimen_nomina, liquidacion_disponible, observacion_normativa,
    VALOR_PUNTO, SMMLV, PUNTOS_PREGRADO, VALOR_HORA_CATEDRA,
    calcular_salario_bruto_admin, calcular_descuento_salud_admin,
    calcular_descuento_pension_admin, calcular_descuento_fsp_admin,
    calcular_salario_neto_admin, calcular_aportes_patronales_admin,
    calcular_costo_total_admin, salario_base_administrativo,
)
from generador import (
    generar_datos_masivos,
    generar_horarios_cursos,
)

# Rutas ABSOLUTAS calculadas a partir de la ubicacion de este archivo, para
# que la GUI funcione sin importar desde que carpeta se ejecute.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "..", "data")

RUTA_FACULTADES = os.path.join(_DATA_DIR, "facultades.txt")
RUTA_PROGRAMAS = os.path.join(_DATA_DIR, "programas.txt")
RUTA_CURSOS = os.path.join(_DATA_DIR, "cursos.txt")
RUTA_ESTUDIANTES = os.path.join(_DATA_DIR, "estudiantes.txt")
RUTA_MATRICULAS = os.path.join(_DATA_DIR, "matriculas.txt")
RUTA_PROFESORES = os.path.join(_DATA_DIR, "profesores.txt")
RUTA_ADMINISTRATIVOS = os.path.join(_DATA_DIR, "administrativos.txt")

C = {
    "bg": "#eef1f5",
    "primary": "#1f4e79",
    "primary_dark": "#163a5c",
    "accent": "#2e7d32",
    "accent_dark": "#1b5e20",
    "danger": "#c0392b",
    "danger_dark": "#922b21",
    "card": "#ffffff",
    "muted": "#6b7280",
    "warn_bg": "#fdecea",
    "warn_fg": "#922b21",
    "ok_bg": "#e8f5e9",
    "ok_fg": "#256029",
}
FONT = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 9, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SUB = ("Segoe UI", 9)


# ============================================================
# Dialogo de formulario generico (crear / editar registros)
# ============================================================

class Formulario(tk.Toplevel):
    """Ventana modal con campos definidos declarativamente.
    campos: lista de dicts {label, key, tipo: entry|combo|check, opciones?, valor?}
    on_guardar: funcion(valores: dict) -> str|None  (retorna mensaje de error, o None si OK)
    """
    def __init__(self, parent, titulo, campos, on_guardar):
        super().__init__(parent)
        self.title(titulo)
        self.configure(bg=C["card"])
        self.resizable(False, False)
        self.on_guardar = on_guardar
        self.vars = {}

        tk.Label(self, text=titulo, font=FONT_BOLD, bg=C["card"], fg=C["primary"]).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 8))

        for i, campo in enumerate(campos, start=1):
            tk.Label(self, text=campo["label"], bg=C["card"], font=FONT).grid(
                row=i, column=0, sticky="w", padx=16, pady=5)
            tipo = campo.get("tipo", "entry")
            if tipo == "combo":
                var = tk.StringVar(value=campo.get("valor", campo["opciones"][0] if campo["opciones"] else ""))
                w = ttk.Combobox(self, textvariable=var, values=campo["opciones"], state="readonly", width=28)
            elif tipo == "check":
                var = tk.BooleanVar(value=campo.get("valor", False))
                w = ttk.Checkbutton(self, variable=var)
            else:
                var = tk.StringVar(value=campo.get("valor", ""))
                w = ttk.Entry(self, textvariable=var, width=30)
                if campo.get("readonly"):
                    w.configure(state="readonly")
            w.grid(row=i, column=1, padx=16, pady=5, sticky="ew")
            self.vars[campo["key"]] = var

        btn_frame = tk.Frame(self, bg=C["card"])
        btn_frame.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(10, 16))
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Guardar", style="Accent.TButton", command=self._guardar).pack(side="left", padx=6)

        self.transient(parent)
        self.grab_set()
        self.bind("<Return>", lambda e: self._guardar())
        self.bind("<Escape>", lambda e: self.destroy())

    def _guardar(self):
        valores = {}
        for k, v in self.vars.items():
            valores[k] = v.get()
        error = self.on_guardar(valores)
        if error:
            messagebox.showerror("No se pudo guardar", error, parent=self)
        else:
            self.destroy()


def confirmar_eliminar(parent, descripcion):
    return messagebox.askyesno(
        "Confirmar eliminación",
        f"Esta acción NO se puede deshacer.\n\n¿Eliminar {descripcion}?",
        icon="warning", parent=parent,
    )


# ============================================================
# Aplicacion principal
# ============================================================

class PitaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PITA — Universidad Popular del Cesar (Parcial 1)")
        self.geometry("1120x680")
        self.minsize(940, 580)
        self.configure(bg=C["bg"])

        self.facultades = []
        self.programas = []
        self.cursos = []
        self.estudiantes = []
        self.profesores = []
        self.administrativos = []
        self.notebook = None
        self.pantalla_inicio = None
        self.icons = {}              # referencias a PhotoImage
        self.secciones = {}          # id_seccion -> Frame de contenido
        self.dock_botones = {}       # id_seccion -> widget boton
        self.seccion_actual = None
        self.titulo_vars = {}        # id_seccion -> StringVar
        self.search_vars = {}        # id_seccion -> StringVar
        self.info_labels = {}        # id_seccion -> Label de estado
        self.refrescos_seccion = {}  # id_seccion -> funcion de refresco

        # Filtros de navegación jerárquica
        self.filtro_facultad_programas = None
        self.filtro_programa_cursos = None
        self.filtro_programa_estudiantes = None
        self.filtro_curso_estudiantes = None

        self._configurar_estilo()
        self._construir_header()
        self._cargar_datos(silencioso=True)
        self._construir_pantalla_inicio()

        self.protocol("WM_DELETE_WINDOW", self._salir)

    # ---------------- Estilo ----------------

    def _configurar_estilo(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TNotebook", background=C["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8), font=FONT_BOLD, background="#dbe4ee")
        style.map("TNotebook.Tab",
                  background=[("selected", C["primary"])],
                  foreground=[("selected", "white")])

        style.configure("Treeview", rowheight=25, font=FONT, background="white",
                        fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=FONT_BOLD, background=C["primary"],
                        foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[("active", C["primary_dark"])])
        style.map("Treeview", background=[("selected", "#cfe0f0")], foreground=[("selected", "black")])

        style.configure("TButton", padding=5, font=FONT)
        style.configure("Accent.TButton", background=C["primary"], foreground="white", font=FONT_BOLD, padding=6)
        style.map("Accent.TButton", background=[("active", C["primary_dark"])])
        style.configure("Danger.TButton", background=C["danger"], foreground="white", font=FONT_BOLD, padding=6)
        style.map("Danger.TButton", background=[("active", C["danger_dark"])])

    def _construir_header(self):
        header = tk.Frame(self, bg=C["primary"], height=76)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=C["primary"])
        left.pack(side="left", padx=18, pady=8)
        tk.Label(left, text="PITA", font=FONT_TITLE, bg=C["primary"], fg="white").pack(anchor="w")
        tk.Label(left, text="Programa Integrado de Transacciones Académicas — UPC (Parcial 1)",
                 font=FONT_SUB, bg=C["primary"], fg="#c9d9e8").pack(anchor="w")

        self.header_actions = tk.Frame(header, bg=C["primary"])
        tk.Button(self.header_actions, text="Recargar datos", command=self._recargar_datos,
                  font=FONT_BOLD, bg="#28405c", fg="white", activebackground="#163a5c", activeforeground="white",
                  relief="flat", bd=0, cursor="hand2", padx=12, pady=5).pack(side="left", padx=4, pady=16)
        tk.Button(self.header_actions, text="Guardar datos", command=self._guardar_datos,
                  font=FONT_BOLD, bg="#2e7d32", fg="white", activebackground="#1b5e20", activeforeground="white",
                  relief="flat", bd=0, cursor="hand2", padx=12, pady=5).pack(side="left", padx=4, pady=16)

        self.status_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.status_var, font=("Segoe UI", 9, "italic"),
                 bg=C["bg"], fg=C["muted"], anchor="w").pack(fill="x", padx=16, pady=(4, 0))

    def _construir_pantalla_inicio(self):
        """Pantalla de bienvenida con dimensiones fluidas."""
        self.pantalla_inicio = tk.Frame(self, bg=C["bg"])
        self.pantalla_inicio.pack(fill="both", expand=True, padx=20, pady=14)

        card = tk.Frame(self.pantalla_inicio, bg=C["card"],
                        highlightbackground="#d8dde3", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78)

        tk.Label(card, text="Bienvenido a PITA", font=("Segoe UI", 22, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(pady=(20, 2))
        tk.Label(card, text="Programa Integrado de Transacciones Académicas — UPC",
                 font=("Segoe UI", 11), bg=C["card"], fg=C["muted"]).pack()
        tk.Label(card, text="Parcial 1: Estructuras Masivas · Nómina · Horarios · ERRA", font=("Segoe UI", 10, "bold"),
                 bg=C["card"], fg="#2e7d32").pack(pady=(2, 14))

        stats = tk.Frame(card, bg="#f4f7fa", highlightbackground="#e1e6eb", highlightthickness=1)
        stats.pack(fill="x", padx=32, pady=(0, 14))
        resumen = [
            ("Facultades", len(self.facultades)),
            ("Programas", len(self.programas)),
            ("Cursos", len(self.cursos)),
            ("Estudiantes", len(self.estudiantes)),
            ("Profesores", len(self.profesores)),
            ("Administrativos", len(self.administrativos)),
        ]
        for i, (nombre, cantidad) in enumerate(resumen):
            fila, columna = divmod(i, 3)
            celda = tk.Frame(stats, bg="#f4f7fa")
            celda.grid(row=fila, column=columna, padx=8, pady=6, sticky="nsew")
            tk.Label(celda, text=f"{cantidad:,}", font=("Segoe UI", 15, "bold"),
                     bg="#f4f7fa", fg=C["primary"]).pack()
            tk.Label(celda, text=nombre, font=("Segoe UI", 8),
                     bg="#f4f7fa", fg=C["muted"]).pack()
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)

        acciones = tk.Frame(card, bg=C["card"])
        acciones.pack(pady=(0, 16))

        tk.Button(acciones, text="Entrar al sistema", command=self._entrar_sistema,
                  font=("Segoe UI", 10, "bold"),
                  bg=C["primary"], fg="white", activebackground=C["primary_dark"],
                  activeforeground="white", relief="flat", cursor="hand2",
                  padx=28, pady=7).pack(pady=(0, 6), fill="x")

        tk.Button(acciones, text="Generar Datos Masivos (Parcial 1)", command=self._generar_datos_masivos_gui,
                  font=("Segoe UI", 10, "bold"),
                  bg="#2e7d32", fg="white", activebackground="#1b5e20",
                  activeforeground="white", relief="flat", cursor="hand2",
                  padx=28, pady=7).pack(pady=(0, 6), fill="x")

        tk.Button(acciones, text="Salir", command=self._salir,
                  font=("Segoe UI", 10, "bold"),
                  bg="#e5e7eb", fg="#374151", activebackground="#d1d5db",
                  activeforeground="#111827", relief="flat", cursor="hand2",
                  padx=28, pady=7).pack(fill="x")

        self._set_status(
            f"Datos actuales en memoria: {len(self.facultades):,} facultades, {len(self.programas):,} programas, "
            f"{len(self.cursos):,} cursos, {len(self.estudiantes):,} estudiantes, "
            f"{len(self.profesores):,} profesores, {len(self.administrativos):,} administrativos."
        )

    def _entrar_sistema(self):
        """Oculta la bienvenida y muestra el menú completo de gestión."""
        if self.pantalla_inicio is not None:
            self.pantalla_inicio.destroy()
            self.pantalla_inicio = None
        self.header_actions.pack(side="right", padx=16)
        self._construir_dock()
        self._set_status(
            f"Sistema listo: {len(self.facultades):,} facultades, {len(self.programas):,} programas, "
            f"{len(self.cursos):,} cursos, {len(self.estudiantes):,} estudiantes, "
            f"{len(self.profesores):,} profesores, {len(self.administrativos):,} administrativos."
        )

    def _set_status(self, texto):
        self.status_var.set(texto)

    # ---------------- Dock inferior de navegación ----------------

    ICONOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

    SECCIONES = [
        ("panel", "Panel", "panel.png"),
        ("facultades", "Facultades", "facultades.png"),
        ("programas", "Programas", "programas.png"),
        ("cursos", "Cursos", "cursos.png"),
        ("estudiantes", "Estudiantes", "estudiantes.png"),
        ("profesores", "Profesores", "profesores.png"),
        ("nomina", "Nómina Docente", "nomina.png"),
        ("administrativos", "Administrativos", "administrativos.png"),
    ]

    def _cargar_icono(self, nombre_archivo):
        ruta = os.path.join(self.ICONOS_DIR, nombre_archivo)
        img = tk.PhotoImage(file=ruta)
        self.icons[nombre_archivo] = img
        return img

    def _construir_dock(self):
        if self.secciones:
            return

        dock = tk.Frame(self, bg="#1b2a3a")
        dock.pack(side="bottom", fill="x")

        izquierda = tk.Frame(dock, bg="#1b2a3a")
        izquierda.pack(side="left", fill="y", padx=(6, 0))

        for sid, etiqueta, archivo in self.SECCIONES:
            icono = self._cargar_icono(archivo)
            btn = tk.Button(
                izquierda, image=icono, text=etiqueta, compound="top",
                font=("Segoe UI", 8, "bold"), fg="#c9d9e8", bg="#1b2a3a",
                activebackground="#28405c", activeforeground="white",
                relief="flat", bd=0, cursor="hand2", padx=8, pady=5,
                command=lambda s=sid: self._mostrar_seccion(s),
            )
            btn.pack(side="left", padx=2, pady=4)
            self.dock_botones[sid] = btn

        icono_salir = self._cargar_icono("salir.png")
        btn_salir = tk.Button(
            dock, image=icono_salir, text="Salir", compound="top",
            font=("Segoe UI", 8, "bold"), fg="#f5b7b1", bg="#1b2a3a",
            activebackground="#922b21", activeforeground="white",
            relief="flat", bd=0, cursor="hand2", padx=12, pady=5,
            command=self._salir,
        )
        btn_salir.pack(side="right", padx=12, pady=4)

        self.content_area = tk.Frame(self, bg=C["bg"])
        self.content_area.pack(side="top", fill="both", expand=True)

        for sid, etiqueta, _archivo in self.SECCIONES:
            frame = tk.Frame(self.content_area, bg=C["bg"])
            self.secciones[sid] = frame

        self._construir_seccion_panel(self.secciones["panel"])
        self._tab_facultades()
        self._tab_programas()
        self._tab_cursos()
        self._tab_estudiantes()
        self._tab_profesores()
        self._tab_administrativos()
        self._tab_nomina()

        self._mostrar_seccion("panel")

    def _mostrar_seccion(self, sid):
        for otro_id, frame in self.secciones.items():
            frame.pack_forget()
            self.dock_botones[otro_id].configure(bg="#1b2a3a", fg="#c9d9e8")
        self.secciones[sid].pack(fill="both", expand=True, padx=14, pady=10)
        self.dock_botones[sid].configure(bg="#28405c", fg="white")
        self.seccion_actual = sid
        if sid in self.refrescos_seccion:
            self.refrescos_seccion[sid]()

    def _construir_seccion_panel(self, frame):
        """Panel de control con diseño en 2 filas de botones masivos sin desbordamiento."""
        for child in frame.winfo_children():
            child.destroy()

        top_bar = tk.Frame(frame, bg=C["bg"])
        top_bar.pack(fill="x", pady=(0, 8))
        tk.Label(top_bar, text="Panel de Control — Parcial 1 (UPC)", font=("Segoe UI", 15, "bold"),
                 bg=C["bg"], fg=C["primary"]).pack(side="left")

        # Centro de operaciones organizado en 2 filas limpias y legibles
        acciones_card = tk.Frame(frame, bg="white", highlightbackground="#d8dde3", highlightthickness=1)
        acciones_card.pack(fill="x", pady=(0, 10), padx=2, ipady=6)

        fila1 = tk.Frame(acciones_card, bg="white")
        fila1.pack(fill="x", padx=10, pady=(6, 3))
        tk.Label(fila1, text="Operaciones del Parcial 1:", font=FONT_BOLD, bg="white", fg=C["primary"], width=24, anchor="w").pack(side="left")
        self._btn(fila1, "Proceso Completo Parcial 1", self._ejecutar_proceso_completo_gui, estilo="accent", lado="left")
        self._btn(fila1, "Generar Datos Masivos", self._generar_datos_masivos_gui, estilo="accent", lado="left")
        self._btn(fila1, "Generar Horarios (42 Slots)", self._generar_horarios_gui, estilo="normal", lado="left")

        fila2 = tk.Frame(acciones_card, bg="white")
        fila2.pack(fill="x", padx=10, pady=(3, 6))
        tk.Label(fila2, text="Auditoría y Persistencia:", font=FONT_BOLD, bg="white", fg="#4b5563", width=24, anchor="w").pack(side="left")
        self._btn(fila2, "Nómina Consolidada (~9k)", self._ver_nomina_masiva_gui, estilo="normal", lado="left")
        self._btn(fila2, "Alertas ERRA (~225k)", self._ver_erra_masivo_gui, estilo="normal", lado="left")
        self._btn(fila2, "Guardar Todo a Disco", self._guardar_datos, estilo="normal", lado="left")

        # Tarjetas de datos principales
        tarjetas = tk.Frame(frame, bg=C["bg"])
        tarjetas.pack(fill="x")
        datos = [
            ("Facultades", len(self.facultades)), ("Programas", len(self.programas)),
            ("Cursos", len(self.cursos)), ("Estudiantes", len(self.estudiantes)),
            ("Profesores", len(self.profesores)), ("Administrativos", len(self.administrativos)),
        ]
        for i, (etiqueta, valor) in enumerate(datos):
            card = tk.Frame(tarjetas, bg=C["card"], highlightbackground="#d8dde3", highlightthickness=1)
            card.grid(row=i // 3, column=i % 3, padx=6, pady=5, sticky="ew")
            tarjetas.grid_columnconfigure(i % 3, weight=1)
            tk.Label(card, text=f"{valor:,}", font=("Segoe UI", 18, "bold"),
                     bg=C["card"], fg=C["primary"]).pack(pady=(8, 0))
            tk.Label(card, text=etiqueta, font=FONT, bg=C["card"], fg=C["muted"]).pack(pady=(0, 8))

        # Métricas secundarias
        total_matriculas = sum(len(e.matriculas) for e in self.estudiantes)
        cursos_con_horario = sum(1 for c in self.cursos if getattr(c, "dia", ""))
        
        sec_frame = tk.Frame(frame, bg="white", highlightbackground="#d8dde3", highlightthickness=1)
        sec_frame.pack(fill="x", pady=(8, 0), padx=2, ipady=6)
        
        info_sub = (
            f"Métricas Globales: {total_matriculas:,} Matrículas/Notas activas  |  "
            f"{cursos_con_horario:,} Cursos con Horario asignado (400 salones, 0 conflictos)  |  "
            f"{len(self.profesores):,} Docentes con nómina auditable"
        )
        tk.Label(sec_frame, text=info_sub, font=("Segoe UI", 9, "bold"), bg="white", fg="#1f4e79").pack(side="left", padx=10)

    # ---------------- Helper de Layout de Pestañas ----------------

    def _crear_shell_tab(self, sid, nombre_seccion, columnas, con_busqueda=True):
        """Crea el contenedor base con buscador y área de botones de 2 filas si es necesario."""
        outer = self.secciones[sid]

        top_header = tk.Frame(outer, bg=C["bg"])
        top_header.pack(fill="x", pady=(0, 4))

        titulo_var = tk.StringVar(value=nombre_seccion)
        self.titulo_vars[sid] = titulo_var
        tk.Label(top_header, textvariable=titulo_var, font=("Segoe UI", 14, "bold"),
                 bg=C["bg"], fg=C["primary"]).pack(side="left")

        search_var = None
        if con_busqueda:
            search_frame = tk.Frame(top_header, bg=C["bg"])
            search_frame.pack(side="right")
            tk.Label(search_frame, text="Buscar:", font=FONT_BOLD, bg=C["bg"], fg="#374151").pack(side="left", padx=(0, 4))
            search_var = tk.StringVar(value="")
            entry = ttk.Entry(search_frame, textvariable=search_var, width=22)
            entry.pack(side="left", padx=(0, 4))
            
            def limpiar():
                search_var.set("")
            tk.Button(search_frame, text="Limpiar", command=limpiar,
                      font=FONT, bg="#e5e7eb", fg="#374151", activebackground="#d1d5db", activeforeground="#111827",
                      relief="flat", bd=0, cursor="hand2", padx=8, pady=2).pack(side="left")
            self.search_vars[sid] = search_var

        card = tk.Frame(outer, bg=C["card"], highlightbackground="#d8dde3", highlightthickness=1)
        card.pack(fill="both", expand=True)

        tree_frame = tk.Frame(card, bg=C["card"])
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(8, 2))

        tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=115, anchor="w")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        info_lbl = tk.Label(card, text="", font=("Segoe UI", 8, "italic"), bg=C["card"], fg=C["muted"], anchor="w")
        info_lbl.pack(fill="x", padx=12, pady=(2, 2))
        self.info_labels[sid] = info_lbl

        btn_frame = tk.Frame(card, bg=C["card"])
        btn_frame.pack(fill="x", padx=10, pady=(2, 8))

        return tree, btn_frame

    def _fila_activo(self, activo):
        return "Activo" if activo else "Inactivo"

    def _btn(self, parent, texto, comando, estilo="normal", lado="left"):
        colores = {
            "normal":  dict(bg="#e5e7eb", fg="#374151", abg="#d1d5db", afg="#111827"),
            "accent":  dict(bg=C["primary"], fg="white",   abg=C["primary_dark"], afg="white"),
            "danger":  dict(bg=C["danger"],  fg="white",   abg=C["danger_dark"],  afg="white"),
            "nav":     dict(bg="#d1d5db",    fg="#374151", abg="#b0b7c3",         afg="#111827"),
        }
        c = colores.get(estilo, colores["normal"])
        b = tk.Button(
            parent, text=texto, command=comando,
            font=FONT_BOLD if estilo in ("accent", "danger") else FONT,
            bg=c["bg"], fg=c["fg"],
            activebackground=c["abg"], activeforeground=c["afg"],
            relief="flat", bd=0, cursor="hand2",
            padx=9, pady=4,
        )
        b.pack(side=lado, padx=3, pady=2)
        return b

    # ---------------- FACULTADES ----------------

    def _tab_facultades(self):
        self.tree_facultades, btns = self._crear_shell_tab(
            "facultades", "Facultades", ["Código", "Nombre", "Decano", "Estado"])

        self._btn(btns, "Nueva",             self._facultad_nueva,    estilo="accent")
        self._btn(btns, "Editar",            self._facultad_editar)
        self._btn(btns, "Activar/Desactivar",self._facultad_toggle)
        self._btn(btns, "Eliminar",          self._facultad_eliminar, estilo="danger")
        self._btn(btns, "Ver programas",     self._ir_a_programas_filtrados)

        if "facultades" in self.search_vars:
            self.search_vars["facultades"].trace_add("write", lambda *_: self._refrescar_facultades())

        self.tree_facultades.bind("<Double-1>", self._doble_click_facultad)
        self._refrescar_facultades()

    def _refrescar_facultades(self):
        self.tree_facultades.delete(*self.tree_facultades.get_children())
        query = self.search_vars.get("facultades", tk.StringVar()).get().strip().lower()
        items = [f for f in self.facultades if not query or (
            query in f.codigo.lower() or query in f.nombre.lower() or query in f.decano.lower()
        )]
        for f in items:
            self.tree_facultades.insert("", "end", iid=f.codigo,
                values=(f.codigo, f.nombre, f.decano, self._fila_activo(f.activo)))
        if "facultades" in self.info_labels:
            self.info_labels["facultades"].config(text=f"Total: {len(items)} de {len(self.facultades)} facultades registradas.")

    def _facultad_seleccionada(self):
        sel = self.tree_facultades.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona una facultad de la lista.")
            return None
        return buscar_facultad(self.facultades, sel[0])

    def _facultad_nueva(self):
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry"},
            {"label": "Nombre", "key": "nombre", "tipo": "entry"},
            {"label": "Decano", "key": "decano", "tipo": "entry"},
        ]
        def guardar(v):
            if not v["codigo"].strip():
                return "El código es obligatorio."
            if buscar_facultad(self.facultades, v["codigo"].strip()):
                return "Ya existe una facultad con ese código."
            self.facultades.append(Facultad(v["codigo"].strip(), v["nombre"].strip(),
                                             v["decano"].strip(), activo=True))
            self._refrescar_facultades()
            self._set_status(f"Facultad {v['codigo']} creada.")
            return None
        Formulario(self, "Nueva facultad", campos, guardar)

    def _facultad_editar(self):
        f = self._facultad_seleccionada()
        if not f:
            return
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry", "valor": f.codigo, "readonly": True},
            {"label": "Nombre", "key": "nombre", "tipo": "entry", "valor": f.nombre},
            {"label": "Decano", "key": "decano", "tipo": "entry", "valor": f.decano},
        ]
        def guardar(v):
            f.nombre = v["nombre"].strip() or f.nombre
            f.decano = v["decano"].strip() or f.decano
            self._refrescar_facultades()
            self._set_status(f"Facultad {f.codigo} modificada.")
            return None
        Formulario(self, "Editar facultad", campos, guardar)

    def _facultad_toggle(self):
        f = self._facultad_seleccionada()
        if not f:
            return
        f.activo = not f.activo
        self._refrescar_facultades()
        self._set_status(f"Facultad {f.codigo} → {self._fila_activo(f.activo)}.")

    def _facultad_eliminar(self):
        f = self._facultad_seleccionada()
        if not f:
            return
        if confirmar_eliminar(self, f"la facultad '{f.nombre}' ({f.codigo})"):
            self.facultades.remove(f)
            self._refrescar_facultades()
            self._set_status(f"Facultad {f.codigo} eliminada.")

    # ---------------- PROGRAMAS ----------------

    def _tab_programas(self):
        self.tree_programas, btns = self._crear_shell_tab(
            "programas", "Programas", ["Código", "Nombre", "Nivel", "Facultad", "Estado"])

        self._btn(btns, "Nuevo",              self._programa_nuevo,              estilo="accent")
        self._btn(btns, "Editar",             self._programa_editar)
        self._btn(btns, "Activar/Desactivar", self._programa_toggle)
        self._btn(btns, "Eliminar",           self._programa_eliminar,           estilo="danger")
        self._btn(btns, "Ver cursos",         self._ir_a_cursos_filtrados)
        self._btn(btns, "Ver estudiantes",    self._ir_a_estudiantes_programa)
        self._btn(btns, "Mostrar todos",      self._mostrar_todos_programas)
        self._btn(btns, "Volver a Facultades", self._volver_a_facultades,        estilo="nav", lado="right")

        if "programas" in self.search_vars:
            self.search_vars["programas"].trace_add("write", lambda *_: self._refrescar_programas())

        self.tree_programas.bind("<Double-1>", self._doble_click_programa)
        self._refrescar_programas()

    def _refrescar_programas(self):
        self.tree_programas.delete(*self.tree_programas.get_children())
        query = self.search_vars.get("programas", tk.StringVar()).get().strip().lower()
        items = []
        for p in self.programas:
            if self.filtro_facultad_programas and p.codigo_facultad != self.filtro_facultad_programas:
                continue
            if query and not (query in p.codigo.lower() or query in p.nombre.lower() or query in p.codigo_facultad.lower()):
                continue
            items.append(p)
        for p in items:
            self.tree_programas.insert("", "end", iid=p.codigo,
                values=(p.codigo, p.nombre, p.nivel, p.codigo_facultad, self._fila_activo(p.activo)))
        if "programas" in self.info_labels:
            self.info_labels["programas"].config(text=f"Total: {len(items)} de {len(self.programas)} programas.")
        self._actualizar_titulo_programas()

    # ---------------- NAVEGACIÓN JERÁRQUICA ----------------

    def _doble_click_facultad(self, event=None):
        self._ir_a_programas_filtrados()

    def _doble_click_programa(self, event=None):
        self._ir_a_cursos_filtrados()

    def _doble_click_curso(self, event=None):
        self._curso_ver_detalle()

    def _doble_click_estudiante(self, event=None):
        self._estudiante_ver_ficha()

    def _ir_a_programas_filtrados(self):
        f = self._facultad_seleccionada()
        if not f:
            return
        self.filtro_facultad_programas = f.codigo
        self.filtro_programa_cursos = None
        self._refrescar_programas()
        self._mostrar_seccion("programas")
        self._set_status(f"Mostrando programas de la facultad: {f.nombre} ({f.codigo}).")

    def _mostrar_todos_programas(self):
        self.filtro_facultad_programas = None
        self._refrescar_programas()
        self._mostrar_seccion("programas")
        self._set_status("Mostrando todos los programas.")

    def _ir_a_cursos_filtrados(self):
        p = self._programa_seleccionado()
        if not p:
            return
        self.filtro_programa_cursos = p.codigo
        self._refrescar_cursos()
        self._mostrar_seccion("cursos")
        self._set_status(f"Mostrando cursos del programa: {p.nombre} ({p.codigo}).")

    def _mostrar_todos_cursos(self):
        self.filtro_programa_cursos = None
        self._refrescar_cursos()
        self._mostrar_seccion("cursos")
        self._set_status("Mostrando todos los cursos.")

    def _ir_a_estudiantes_programa(self):
        p = self._programa_seleccionado()
        if not p:
            return
        self.filtro_programa_estudiantes = p.codigo
        self.filtro_curso_estudiantes = None
        self._refrescar_estudiantes()
        self._mostrar_seccion("estudiantes")
        self._set_status(f"Mostrando estudiantes del programa: {p.nombre} ({p.codigo}).")

    def _ir_a_estudiantes_curso(self):
        c = self._curso_seleccionado()
        if not c:
            return
        self.filtro_curso_estudiantes = c.codigo
        self.filtro_programa_estudiantes = None
        self._refrescar_estudiantes()
        self._mostrar_seccion("estudiantes")
        self._set_status(f"Mostrando estudiantes matriculados en: {c.nombre} ({c.codigo}).")

    def _mostrar_todos_estudiantes(self):
        self.filtro_programa_estudiantes = None
        self.filtro_curso_estudiantes = None
        self._refrescar_estudiantes()
        self._mostrar_seccion("estudiantes")
        self._set_status("Mostrando todos los estudiantes.")

    def _volver_a_facultades(self):
        self._mostrar_seccion("facultades")
        self._set_status("Selecciona una facultad para consultar sus programas.")

    def _volver_a_programas(self):
        self.filtro_programa_cursos = None
        self._refrescar_programas()
        self._mostrar_seccion("programas")
        self._set_status("Selecciona un programa para consultar sus cursos.")

    def _actualizar_titulo_programas(self):
        if "programas" not in self.titulo_vars:
            return
        if self.filtro_facultad_programas:
            f = buscar_facultad(self.facultades, self.filtro_facultad_programas)
            texto = f"Programas — {f.codigo}" if f else "Programas"
        else:
            texto = "Programas"
        self.titulo_vars["programas"].set(texto)

    def _actualizar_titulo_cursos(self):
        if "cursos" not in self.titulo_vars:
            return
        if self.filtro_programa_cursos:
            p = buscar_programa(self.programas, self.filtro_programa_cursos)
            texto = f"Cursos — {p.codigo}" if p else "Cursos"
        else:
            texto = "Cursos"
        self.titulo_vars["cursos"].set(texto)

    def _actualizar_titulo_estudiantes(self):
        if "estudiantes" not in self.titulo_vars:
            return
        if self.filtro_curso_estudiantes:
            c = buscar_curso(self.cursos, self.filtro_curso_estudiantes)
            texto = f"Estudiantes — {c.codigo}" if c else "Estudiantes"
        elif self.filtro_programa_estudiantes:
            p = buscar_programa(self.programas, self.filtro_programa_estudiantes)
            texto = f"Estudiantes — {p.codigo}" if p else "Estudiantes"
        else:
            texto = "Estudiantes"
        self.titulo_vars["estudiantes"].set(texto)

    def _programa_seleccionado(self):
        sel = self.tree_programas.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un programa de la lista.")
            return None
        return buscar_programa(self.programas, sel[0])

    def _codigos_facultades_activas(self):
        return [f.codigo for f in self.facultades if f.activo] or [""]

    def _programa_nuevo(self):
        opciones_facultad = self._codigos_facultades_activas()
        if not self.facultades:
            messagebox.showwarning("Sin facultades", "Primero debes crear al menos una facultad.")
            return
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry"},
            {"label": "Nombre", "key": "nombre", "tipo": "entry"},
            {"label": "Nivel", "key": "nivel", "tipo": "combo",
             "opciones": ["Pregrado", "Tecnologico", "Especializacion", "Maestria"]},
            {"label": "Facultad", "key": "codigo_facultad", "tipo": "combo", "opciones": opciones_facultad},
        ]
        def guardar(v):
            if not v["codigo"].strip():
                return "El código es obligatorio."
            if buscar_programa(self.programas, v["codigo"].strip()):
                return "Ya existe un programa con ese código."
            facultad = buscar_facultad(self.facultades, v["codigo_facultad"])
            if not facultad or not facultad.activo:
                return "Selecciona una facultad válida y activa."
            self.programas.append(Programa(v["codigo"].strip(), v["nombre"].strip(),
                                            v["nivel"], v["codigo_facultad"], activo=True))
            self._refrescar_programas()
            self._set_status(f"Programa {v['codigo']} creado.")
            return None
        Formulario(self, "Nuevo programa", campos, guardar)

    def _programa_editar(self):
        p = self._programa_seleccionado()
        if not p:
            return
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry", "valor": p.codigo, "readonly": True},
            {"label": "Nombre", "key": "nombre", "tipo": "entry", "valor": p.nombre},
            {"label": "Nivel", "key": "nivel", "tipo": "combo",
             "opciones": ["Pregrado", "Tecnologico", "Especializacion", "Maestria"], "valor": p.nivel},
        ]
        def guardar(v):
            p.nombre = v["nombre"].strip() or p.nombre
            p.nivel = v["nivel"]
            self._refrescar_programas()
            self._set_status(f"Programa {p.codigo} modificado.")
            return None
        Formulario(self, "Editar programa", campos, guardar)

    def _programa_toggle(self):
        p = self._programa_seleccionado()
        if not p:
            return
        p.activo = not p.activo
        self._refrescar_programas()
        self._set_status(f"Programa {p.codigo} → {self._fila_activo(p.activo)}.")

    def _programa_eliminar(self):
        p = self._programa_seleccionado()
        if not p:
            return
        if confirmar_eliminar(self, f"el programa '{p.nombre}' ({p.codigo})"):
            self.programas.remove(p)
            self._refrescar_programas()
            self._set_status(f"Programa {p.codigo} eliminado.")

    # ---------------- CURSOS ----------------

    def _tab_cursos(self):
        self.tree_cursos, btns = self._crear_shell_tab(
            "cursos", "Cursos", ["Código", "Nombre", "Créditos", "Programa", "Profesor", "Horario", "Salón", "Estado"])

        # Fila 1 de botones: CRUD
        fila1 = tk.Frame(btns, bg=C["card"])
        fila1.pack(fill="x", pady=(0, 2))
        self._btn(fila1, "Nuevo",              self._curso_nuevo,              estilo="accent")
        self._btn(fila1, "Editar",             self._curso_editar)
        self._btn(fila1, "Ver detalle",        self._curso_ver_detalle)
        self._btn(fila1, "Ver profesor",       self._curso_ver_profesor)
        self._btn(fila1, "Ver estudiantes",    self._ir_a_estudiantes_curso)

        # Fila 2 de botones: Operaciones y navegación
        fila2 = tk.Frame(btns, bg=C["card"])
        fila2.pack(fill="x", pady=(2, 0))
        self._btn(fila2, "Generar Horarios",   self._generar_horarios_gui,     estilo="accent")
        self._btn(fila2, "Mostrar todos",      self._mostrar_todos_cursos)
        self._btn(fila2, "Activar/Desactivar", self._curso_toggle)
        self._btn(fila2, "Eliminar",           self._curso_eliminar,           estilo="danger")
        self._btn(fila2, "Volver a Programas", self._volver_a_programas,       estilo="nav", lado="right")

        if "cursos" in self.search_vars:
            self.search_vars["cursos"].trace_add("write", lambda *_: self._refrescar_cursos())

        self.tree_cursos.bind("<Double-1>", self._doble_click_curso)
        self._refrescar_cursos()

    def _refrescar_cursos(self):
        self.tree_cursos.delete(*self.tree_cursos.get_children())
        query = self.search_vars.get("cursos", tk.StringVar()).get().strip().lower()
        items = []
        for c in self.cursos:
            if self.filtro_programa_cursos and c.codigo_programa != self.filtro_programa_cursos:
                continue
            if query:
                dia = getattr(c, "dia", "")
                h_ini = getattr(c, "hora_inicio", 0)
                salon = getattr(c, "salon", "")
                if not (query in c.codigo.lower() or query in c.nombre.lower() or
                        query in c.codigo_programa.lower() or query in str(c.codigo_profesor).lower() or
                        query in dia.lower() or query in str(h_ini) or query in str(salon).lower()):
                    continue
            items.append(c)

        visibles = items[:300]
        for c in visibles:
            prof = c.codigo_profesor if c.codigo_profesor else "(sin asignar)"
            dia = getattr(c, "dia", "")
            h_ini = getattr(c, "hora_inicio", 0)
            h_fin = getattr(c, "hora_fin", 0)
            if dia and h_ini:
                horario_str = f"{dia} {h_ini}:00-{h_fin}:00"
            elif dia:
                horario_str = dia
            else:
                horario_str = "(sin asignar)"
            salon_str = str(getattr(c, "salon", "")) if getattr(c, "salon", "") else "(sin asignar)"
            self.tree_cursos.insert("", "end", iid=c.codigo,
                values=(c.codigo, c.nombre, c.creditos, c.codigo_programa, prof, horario_str, salon_str, self._fila_activo(c.activo)))

        if "cursos" in self.info_labels:
            if len(items) > 300:
                self.info_labels["cursos"].config(text=f"Mostrando primeros 300 de {len(items):,} cursos (Usa el buscador para filtrar en tiempo real).")
            else:
                self.info_labels["cursos"].config(text=f"Total: {len(items):,} de {len(self.cursos):,} cursos.")
        self._actualizar_titulo_cursos()

    def _curso_seleccionado(self):
        sel = self.tree_cursos.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un curso de la lista.")
            return None
        return buscar_curso(self.cursos, sel[0])

    def _curso_nuevo(self):
        if not self.programas:
            messagebox.showwarning("Sin programas", "Primero debes crear al menos un programa.")
            return
        opciones_programa = [p.codigo for p in self.programas if p.activo] or [""]
        opciones_profesor = [""] + [p.identificacion for p in self.profesores]
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry"},
            {"label": "Nombre", "key": "nombre", "tipo": "entry"},
            {"label": "Créditos", "key": "creditos", "tipo": "entry", "valor": "3"},
            {"label": "Programa", "key": "codigo_programa", "tipo": "combo", "opciones": opciones_programa},
            {"label": "Profesor (opcional)", "key": "codigo_profesor", "tipo": "combo", "opciones": opciones_profesor},
        ]
        def guardar(v):
            if not v["codigo"].strip():
                return "El código es obligatorio."
            if buscar_curso(self.cursos, v["codigo"].strip()):
                return "Ya existe un curso con ese código."
            programa = buscar_programa(self.programas, v["codigo_programa"])
            if not programa or not programa.activo:
                return "Selecciona un programa válido y activo."
            try:
                creditos = int(v["creditos"])
            except ValueError:
                return "Los créditos deben ser un número entero."
            self.cursos.append(Curso(v["codigo"].strip(), v["nombre"].strip(), creditos,
                                      v["codigo_profesor"], v["codigo_programa"], activo=True))
            self._refrescar_cursos()
            self._set_status(f"Curso {v['codigo']} creado.")
            return None
        Formulario(self, "Nuevo curso", campos, guardar)

    def _curso_editar(self):
        c = self._curso_seleccionado()
        if not c:
            return
        campos = [
            {"label": "Código", "key": "codigo", "tipo": "entry", "valor": c.codigo, "readonly": True},
            {"label": "Nombre", "key": "nombre", "tipo": "entry", "valor": c.nombre},
            {"label": "Créditos", "key": "creditos", "tipo": "entry", "valor": str(c.creditos)},
        ]
        def guardar(v):
            c.nombre = v["nombre"].strip() or c.nombre
            try:
                c.creditos = int(v["creditos"])
            except ValueError:
                return "Los créditos deben ser un número entero."
            self._refrescar_cursos()
            self._set_status(f"Curso {c.codigo} modificado.")
            return None
        Formulario(self, "Editar curso", campos, guardar)

    def _curso_toggle(self):
        c = self._curso_seleccionado()
        if not c:
            return
        c.activo = not c.activo
        self._refrescar_cursos()
        self._set_status(f"Curso {c.codigo} → {self._fila_activo(c.activo)}.")

    def _curso_eliminar(self):
        c = self._curso_seleccionado()
        if not c:
            return
        if confirmar_eliminar(self, f"el curso '{c.nombre}' ({c.codigo})"):
            self.cursos.remove(c)
            self._refrescar_cursos()
            self._set_status(f"Curso {c.codigo} eliminado.")

    def _curso_ver_profesor(self):
        c = self._curso_seleccionado()
        if not c:
            return
        if not c.codigo_profesor:
            messagebox.showinfo("Profesor", "Este curso todavía no tiene profesor asignado.")
            return
        p = buscar_profesor(self.profesores, c.codigo_profesor)
        if not p:
            messagebox.showwarning("Profesor no encontrado",
                                   f"El curso referencia al profesor {c.codigo_profesor}, pero no existe en la lista.")
            return
        VentanaProfesorResumen(self, p, c)

    def _curso_ver_detalle(self):
        c = self._curso_seleccionado()
        if not c:
            return
        VentanaCursoDetalle(self, c)

    # ---------------- ESTUDIANTES ----------------

    def _tab_estudiantes(self):
        self.tree_estudiantes, btns = self._crear_shell_tab(
            "estudiantes", "Estudiantes", ["ID", "Nombre", "Programa", "Estado", "Promedio", "ERRA (EBRA)"])

        # Fila 1 de botones: CRUD y Ficha
        fila1 = tk.Frame(btns, bg=C["card"])
        fila1.pack(fill="x", pady=(0, 2))
        self._btn(fila1, "Nuevo",              self._estudiante_nuevo,           estilo="accent")
        self._btn(fila1, "Editar",             self._estudiante_editar)
        self._btn(fila1, "Ver ficha",          self._estudiante_ver_ficha)
        self._btn(fila1, "Matricular curso",   self._estudiante_matricular)
        self._btn(fila1, "Cancelar curso",     self._estudiante_cancelar_curso)

        # Fila 2 de botones: Operaciones y Estado
        fila2 = tk.Frame(btns, bg=C["card"])
        fila2.pack(fill="x", pady=(2, 0))
        self._btn(fila2, "Alertas ERRA",       self._ver_erra_masivo_gui,        estilo="accent")
        self._btn(fila2, "Mostrar todos",      self._mostrar_todos_estudiantes)
        self._btn(fila2, "Activar/Desactivar", self._estudiante_toggle)
        self._btn(fila2, "Eliminar",           self._estudiante_eliminar,        estilo="danger")

        if "estudiantes" in self.search_vars:
            self.search_vars["estudiantes"].trace_add("write", lambda *_: self._refrescar_estudiantes())

        self.tree_estudiantes.bind("<Double-1>", self._doble_click_estudiante)
        self._refrescar_estudiantes()

    def _refrescar_estudiantes(self):
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        query = self.search_vars.get("estudiantes", tk.StringVar()).get().strip().lower()
        items = []
        for e in self.estudiantes:
            if self.filtro_programa_estudiantes and e.codigo_programa != self.filtro_programa_estudiantes:
                continue
            if self.filtro_curso_estudiantes and not any(
                    m["codigo_curso"] == self.filtro_curso_estudiantes for m in e.matriculas):
                continue
            if query:
                if not (query in e.identificacion.lower() or query in e.nombre_completo.lower() or
                        query in e.codigo_programa.lower()):
                    continue
            items.append(e)

        visibles = items[:300]
        self.tree_estudiantes.tag_configure("riesgo", foreground=C["danger"])
        for e in visibles:
            promedio = e.calcular_promedio()
            en_riesgo = e.esta_en_riesgo_ebra()
            ebra = "EN RIESGO (<3.25)" if en_riesgo else "Satisfactorio"
            iid = e.identificacion
            tags = ("riesgo",) if en_riesgo else ()
            self.tree_estudiantes.insert("", "end", iid=iid,
                values=(e.identificacion, e.nombre_completo, e.codigo_programa, e.estado,
                        f"{promedio:.2f}", ebra), tags=tags)

        if "estudiantes" in self.info_labels:
            if len(items) > 300:
                self.info_labels["estudiantes"].config(
                    text=f"Mostrando primeros 300 de {len(items):,} estudiantes (Escribe en el buscador para filtrar en tiempo real).")
            else:
                self.info_labels["estudiantes"].config(text=f"Total: {len(items):,} de {len(self.estudiantes):,} estudiantes.")
        self._actualizar_titulo_estudiantes()

    def _estudiante_seleccionado(self):
        sel = self.tree_estudiantes.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un estudiante de la lista.")
            return None
        return buscar_estudiante(self.estudiantes, sel[0])

    def _estudiante_nuevo(self):
        if not self.programas:
            messagebox.showwarning("Sin programas", "Primero debes crear al menos un programa.")
            return
        opciones_programa = [p.codigo for p in self.programas if p.activo] or [""]
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry"},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry"},
            {"label": "Programa", "key": "codigo_programa", "tipo": "combo", "opciones": opciones_programa},
        ]
        def guardar(v):
            if not v["identificacion"].strip():
                return "La identificación es obligatoria."
            if buscar_estudiante(self.estudiantes, v["identificacion"].strip()):
                return "Ya existe un estudiante con esa identificación."
            programa = buscar_programa(self.programas, v["codigo_programa"])
            if not programa:
                return "Selecciona un programa válido."
            self.estudiantes.append(Estudiante(v["identificacion"].strip(), v["nombre"].strip(),
                                                v["codigo_programa"], estado="Activo", activo=True))
            self._refrescar_estudiantes()
            self._set_status(f"Estudiante {v['identificacion']} creado.")
            return None
        Formulario(self, "Nuevo estudiante", campos, guardar)

    def _estudiante_editar(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry",
             "valor": e.identificacion, "readonly": True},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry", "valor": e.nombre_completo},
            {"label": "Estado", "key": "estado", "tipo": "combo",
             "opciones": ["Activo", "Inactivo", "Graduado"], "valor": e.estado},
        ]
        def guardar(v):
            e.nombre_completo = v["nombre"].strip() or e.nombre_completo
            e.estado = v["estado"]
            self._refrescar_estudiantes()
            self._set_status(f"Estudiante {e.identificacion} modificado.")
            return None
        Formulario(self, "Editar estudiante", campos, guardar)

    def _estudiante_toggle(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        e.activo = not e.activo
        e.estado = "Activo" if e.activo else "Inactivo"
        self._refrescar_estudiantes()
        self._set_status(f"Estudiante {e.identificacion} → {self._fila_activo(e.activo)}.")

    def _estudiante_eliminar(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        if confirmar_eliminar(self, f"al estudiante '{e.nombre_completo}' ({e.identificacion})"):
            self.estudiantes.remove(e)
            self._refrescar_estudiantes()
            self._set_status(f"Estudiante {e.identificacion} eliminado.")

    def _estudiante_matricular(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        ya_matriculados = {m["codigo_curso"] for m in e.matriculas}
        opciones_curso = [c.codigo for c in self.cursos
                          if c.activo and c.codigo_programa == e.codigo_programa
                          and c.codigo not in ya_matriculados]
        if not opciones_curso:
            messagebox.showwarning("Sin cursos disponibles",
                f"No hay cursos activos del programa {e.codigo_programa} pendientes por matricular.")
            return
        campos = [
            {"label": "Curso", "key": "codigo_curso", "tipo": "combo", "opciones": opciones_curso},
            {"label": "Nota (0.0 si aún no tiene)", "key": "nota", "tipo": "entry", "valor": "0.0"},
        ]
        def guardar(v):
            curso = buscar_curso(self.cursos, v["codigo_curso"])
            if not curso or not curso.activo:
                return "Selecciona un curso válido y activo."
            if any(m["codigo_curso"] == v["codigo_curso"] for m in e.matriculas):
                return "El estudiante ya está matriculado en ese curso."
            try:
                nota = float(v["nota"])
            except ValueError:
                return "La nota debe ser un número."
            e.matriculas.append({"codigo_curso": v["codigo_curso"], "nota": nota})
            self._refrescar_estudiantes()
            self._set_status(f"{e.identificacion} matriculado en {v['codigo_curso']}.")
            return None
        Formulario(self, f"Matricular a {e.nombre_completo}", campos, guardar)

    def _estudiante_cancelar_curso(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        if not e.matriculas:
            messagebox.showinfo("Sin matrículas", "Este estudiante no tiene cursos matriculados.")
            return
        opciones_curso = [m["codigo_curso"] for m in e.matriculas]
        campos = [{"label": "Curso a cancelar", "key": "codigo_curso", "tipo": "combo", "opciones": opciones_curso}]
        def guardar(v):
            e.matriculas = [m for m in e.matriculas if m["codigo_curso"] != v["codigo_curso"]]
            self._refrescar_estudiantes()
            self._set_status(f"Matrícula de {v['codigo_curso']} cancelada para {e.identificacion}.")
            return None
        Formulario(self, f"Cancelar curso — {e.nombre_completo}", campos, guardar)

    def _estudiante_ver_ficha(self):
        e = self._estudiante_seleccionado()
        if not e:
            return
        VentanaEstudiante(self, e)

    # ---------------- PROFESORES ----------------

    def _tab_profesores(self):
        self.tree_profesores, btns = self._crear_shell_tab(
            "profesores", "Profesores", ["ID", "Nombre", "Vinculación", "Dedicación", "Categoría", "Programa", "Estado"])

        self._btn(btns, "Nuevo",              self._profesor_nuevo,    estilo="accent")
        self._btn(btns, "Editar",             self._profesor_editar)
        self._btn(btns, "Ver nómina",         self._profesor_ver_nomina)
        self._btn(btns, "Nómina Consolidada", self._ver_nomina_masiva_gui, estilo="accent")
        self._btn(btns, "Activar/Desactivar", self._profesor_toggle)
        self._btn(btns, "Eliminar",           self._profesor_eliminar, estilo="danger")

        if "profesores" in self.search_vars:
            self.search_vars["profesores"].trace_add("write", lambda *_: self._refrescar_profesores())

        self._refrescar_profesores()

    def _refrescar_profesores(self):
        self.tree_profesores.delete(*self.tree_profesores.get_children())
        query = self.search_vars.get("profesores", tk.StringVar()).get().strip().lower()
        items = []
        for p in self.profesores:
            if query:
                cat = str(p.categoria_escalafon or "")
                if not (query in p.identificacion.lower() or query in p.nombre_completo.lower() or
                        query in p.tipo_vinculacion.lower() or query in cat.lower() or
                        query in p.codigo_programa.lower()):
                    continue
            items.append(p)

        visibles = items[:300]
        for p in visibles:
            self.tree_profesores.insert("", "end", iid=p.identificacion,
                values=(p.identificacion, p.nombre_completo, p.tipo_vinculacion, p.dedicacion,
                        p.categoria_escalafon or "—", p.codigo_programa, self._fila_activo(p.activo)))

        if "profesores" in self.info_labels:
            if len(items) > 300:
                self.info_labels["profesores"].config(
                    text=f"Mostrando primeros 300 de {len(items):,} profesores (Usa el buscador para filtrar en tiempo real).")
            else:
                self.info_labels["profesores"].config(text=f"Total: {len(items):,} de {len(self.profesores):,} profesores.")

    def _profesor_seleccionado(self):
        sel = self.tree_profesores.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un profesor de la lista.")
            return None
        return buscar_profesor(self.profesores, sel[0])

    def _profesor_nuevo(self):
        if not self.programas:
            messagebox.showwarning("Sin programas", "Primero debes crear al menos un programa.")
            return
        opciones_programa = [p.codigo for p in self.programas if p.activo] or [""]
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry"},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry"},
            {"label": "Programa", "key": "codigo_programa", "tipo": "combo", "opciones": opciones_programa},
            {"label": "Tipo de vinculación", "key": "tipo_vinculacion", "tipo": "combo",
             "opciones": ["Planta", "Ocasional", "Catedratico"]},
            {"label": "Dedicación", "key": "dedicacion", "tipo": "combo",
             "opciones": ["TiempoCompleto", "MedioTiempo", "HorasCatedra"]},
            {"label": "Categoría escalafón (vacío si Catedrático)", "key": "categoria_escalafon", "tipo": "combo",
             "opciones": ["", "Auxiliar", "Asistente", "Asociado", "Titular"]},
            {"label": "Horas cátedra semanales (máx. 18)", "key": "horas_catedra", "tipo": "entry", "valor": "0"},
            {"label": "Ad-honorem (sin remuneración)", "key": "ad_honorem", "tipo": "check", "valor": False},
            {"label": "Posgrado (Acuerdo 027/2024)", "key": "posgrado", "tipo": "combo",
             "opciones": ["", "Especializacion", "Maestria", "Doctorado"]},
            {"label": "Años de experiencia", "key": "anios_experiencia", "tipo": "entry", "valor": "0"},
            {"label": "Puntos por títulos", "key": "puntos_titulos", "tipo": "entry", "valor": "0"},
            {"label": "Puntos por productividad", "key": "puntos_productividad", "tipo": "entry", "valor": "0"},
        ]
        def guardar(v):
            if not v["identificacion"].strip():
                return "La identificación es obligatoria."
            if buscar_profesor(self.profesores, v["identificacion"].strip()):
                return "Ya existe un profesor con esa identificación."
            if v["tipo_vinculacion"] == "Catedratico":
                try:
                    horas = int(v["horas_catedra"])
                except ValueError:
                    return "Las horas de cátedra deben ser un número entero."
                if horas > 18:
                    return "El Acuerdo 027 de 2024 limita a 18 horas semanales para catedráticos."
            try:
                horas_catedra = int(v["horas_catedra"] or 0)
                anios = int(v["anios_experiencia"] or 0)
                pt = int(v["puntos_titulos"] or 0)
                pp = int(v["puntos_productividad"] or 0)
            except ValueError:
                return "Los campos numéricos deben ser números enteros."
            self.profesores.append(Profesor(
                v["identificacion"].strip(), v["nombre"].strip(), v["codigo_programa"],
                v["tipo_vinculacion"], v["dedicacion"], v["categoria_escalafon"],
                horas_catedra, bool(v["ad_honorem"]), anios, pt, pp, activo=True,
                posgrado=v.get("posgrado", ""),
            ))
            self._refrescar_profesores()
            self._set_status(f"Profesor {v['identificacion']} creado.")
            return None
        Formulario(self, "Nuevo profesor", campos, guardar)

    def _profesor_editar(self):
        p = self._profesor_seleccionado()
        if not p:
            return
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry",
             "valor": p.identificacion, "readonly": True},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry", "valor": p.nombre_completo},
            {"label": "Tipo de vinculación", "key": "tipo_vinculacion", "tipo": "combo",
             "opciones": ["Planta", "Ocasional", "Catedratico"], "valor": p.tipo_vinculacion},
            {"label": "Dedicación", "key": "dedicacion", "tipo": "combo",
             "opciones": ["TiempoCompleto", "MedioTiempo", "HorasCatedra"], "valor": p.dedicacion},
            {"label": "Categoría escalafón (vacío si Catedrático)", "key": "categoria_escalafon", "tipo": "combo",
             "opciones": ["", "Auxiliar", "Asistente", "Asociado", "Titular"], "valor": p.categoria_escalafon},
            {"label": "Horas cátedra semanales (máx. 18)", "key": "horas_catedra", "tipo": "entry",
             "valor": str(p.horas_catedra_semanales)},
            {"label": "Ad-honorem (sin remuneración)", "key": "ad_honorem", "tipo": "check",
             "valor": p.ad_honorem},
            {"label": "Posgrado (Acuerdo 027/2024)", "key": "posgrado", "tipo": "combo",
             "opciones": ["", "Especializacion", "Maestria", "Doctorado"],
             "valor": getattr(p, "posgrado", "")},
            {"label": "Años de experiencia", "key": "anios_experiencia", "tipo": "entry",
             "valor": str(p.anios_experiencia)},
            {"label": "Puntos por títulos", "key": "puntos_titulos", "tipo": "entry",
             "valor": str(p.puntos_titulos)},
            {"label": "Puntos por productividad", "key": "puntos_productividad", "tipo": "entry",
             "valor": str(p.puntos_productividad)},
        ]
        def guardar(v):
            if v["tipo_vinculacion"] == "Catedratico":
                try:
                    horas = int(v["horas_catedra"])
                except ValueError:
                    return "Las horas de cátedra deben ser un número entero."
                if horas > 18:
                    return "El Acuerdo 027 de 2024 limita a 18 horas semanales para catedráticos."
            try:
                p.anios_experiencia = int(v["anios_experiencia"])
                p.puntos_titulos = int(v["puntos_titulos"])
                p.puntos_productividad = int(v["puntos_productividad"])
                p.horas_catedra_semanales = int(v["horas_catedra"] or 0)
            except ValueError:
                return "Los campos numéricos deben ser números enteros."
            p.nombre_completo = v["nombre"].strip() or p.nombre_completo
            p.tipo_vinculacion = v["tipo_vinculacion"]
            p.dedicacion = v["dedicacion"]
            p.categoria_escalafon = v["categoria_escalafon"]
            p.ad_honorem = bool(v["ad_honorem"])
            p.posgrado = v.get("posgrado", "")
            self._refrescar_profesores()
            self._set_status(f"Profesor {p.identificacion} modificado.")
            return None
        Formulario(self, "Editar profesor", campos, guardar)

    def _profesor_toggle(self):
        p = self._profesor_seleccionado()
        if not p:
            return
        p.activo = not p.activo
        self._refrescar_profesores()
        self._set_status(f"Profesor {p.identificacion} → {self._fila_activo(p.activo)}.")

    def _profesor_eliminar(self):
        p = self._profesor_seleccionado()
        if not p:
            return
        if confirmar_eliminar(self, f"al profesor '{p.nombre_completo}' ({p.identificacion})"):
            self.profesores.remove(p)
            self._refrescar_profesores()
            self._set_status(f"Profesor {p.identificacion} eliminado.")

    def _profesor_ver_nomina(self):
        p = self._profesor_seleccionado()
        if not p:
            return
        VentanaNomina(self, p)

    # ---------------- ADMINISTRATIVOS ----------------

    def _tab_administrativos(self):
        self.tree_admins, btns = self._crear_shell_tab(
            "administrativos", "Administrativos", ["ID", "Nombre", "Cargo", "Contratación", "Facultad", "Salario", "Estado"])

        self._btn(btns, "Nuevo",              self._admin_nuevo,    estilo="accent")
        self._btn(btns, "Editar",             self._admin_editar)
        self._btn(btns, "Ver salario",        self._admin_ver_salario)
        self._btn(btns, "Activar/Desactivar", self._admin_toggle)
        self._btn(btns, "Eliminar",           self._admin_eliminar, estilo="danger")

        if "administrativos" in self.search_vars:
            self.search_vars["administrativos"].trace_add("write", lambda *_: self._refrescar_administrativos())

        self._refrescar_administrativos()

    def _admin_ver_salario(self):
        a = self._admin_seleccionado()
        if not a:
            return
        VentanaSalarioAdmin(self, a)

    def _refrescar_administrativos(self):
        self.tree_admins.delete(*self.tree_admins.get_children())
        query = self.search_vars.get("administrativos", tk.StringVar()).get().strip().lower()
        items = []
        for a in self.administrativos:
            if query:
                if not (query in a.identificacion.lower() or query in a.nombre_completo.lower() or
                        query in a.cargo.lower() or query in a.tipo_contratacion.lower()):
                    continue
            items.append(a)

        for a in items:
            facultad = a.codigo_facultad if a.codigo_facultad else "(nivel central)"
            self.tree_admins.insert("", "end", iid=a.identificacion,
                values=(a.identificacion, a.nombre_completo, a.cargo, a.tipo_contratacion,
                        facultad, f"${a.salario_base:,.0f}", self._fila_activo(a.activo)))

        if "administrativos" in self.info_labels:
            self.info_labels["administrativos"].config(text=f"Total: {len(items)} de {len(self.administrativos)} administrativos.")

    def _admin_seleccionado(self):
        sel = self.tree_admins.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un administrativo de la lista.")
            return None
        return buscar_administrativo(self.administrativos, sel[0])

    def _admin_nuevo(self):
        opciones_facultad = [""] + [f.codigo for f in self.facultades]
        niveles = ["Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4"]
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry"},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry"},
            {"label": "Cargo", "key": "cargo", "tipo": "entry"},
            {"label": "Categoría (Escala Salarial)", "key": "categoria", "tipo": "combo", "opciones": niveles},
            {"label": "Tipo de contratación", "key": "tipo_contratacion", "tipo": "combo",
             "opciones": ["Planta", "Provisional", "Contrato"]},
            {"label": "Salario base (0 = según escala)", "key": "salario_base", "tipo": "entry", "valor": "0"},
            {"label": "Facultad (vacío = nivel central)", "key": "codigo_facultad", "tipo": "combo",
             "opciones": opciones_facultad},
        ]
        def guardar(v):
            if not v["identificacion"].strip():
                return "La identificación es obligatoria."
            if buscar_administrativo(self.administrativos, v["identificacion"].strip()):
                return "Ya existe un administrativo con esa identificación."
            if v["codigo_facultad"] and not buscar_facultad(self.facultades, v["codigo_facultad"]):
                return "Esa facultad no existe."
            try:
                salario = float(v["salario_base"])
            except ValueError:
                return "El salario debe ser un número."
            if salario <= 0:
                salario = salario_base_administrativo(v["categoria"])
            self.administrativos.append(Administrativo(
                v["identificacion"].strip(), v["nombre"].strip(), v["cargo"].strip(),
                v["categoria"].strip(), v["tipo_contratacion"], salario,
                v["codigo_facultad"], activo=True,
            ))
            self._refrescar_administrativos()
            self._set_status(f"Administrativo {v['identificacion']} creado.")
            return None
        Formulario(self, "Nuevo administrativo", campos, guardar)

    def _admin_editar(self):
        a = self._admin_seleccionado()
        if not a:
            return
        niveles = ["Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4"]
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry",
             "valor": a.identificacion, "readonly": True},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry", "valor": a.nombre_completo},
            {"label": "Cargo", "key": "cargo", "tipo": "entry", "valor": a.cargo},
            {"label": "Categoría (Escala Salarial)", "key": "categoria", "tipo": "combo",
             "opciones": niveles, "valor": a.categoria if a.categoria in niveles else "Nivel 1"},
            {"label": "Tipo de contratación", "key": "tipo_contratacion", "tipo": "combo",
             "opciones": ["Planta", "Provisional", "Contrato"], "valor": a.tipo_contratacion},
            {"label": "Salario base", "key": "salario_base", "tipo": "entry", "valor": str(int(a.salario_base))},
        ]
        def guardar(v):
            a.nombre_completo = v["nombre"].strip() or a.nombre_completo
            a.cargo = v["cargo"].strip() or a.cargo
            a.categoria = v["categoria"]
            a.tipo_contratacion = v["tipo_contratacion"]
            try:
                salario = float(v["salario_base"])
                if salario <= 0:
                    salario = salario_base_administrativo(a.categoria)
                a.salario_base = salario
            except ValueError:
                return "El salario debe ser un número."
            self._refrescar_administrativos()
            self._set_status(f"Administrativo {a.identificacion} modificado.")
            return None
        Formulario(self, "Editar administrativo", campos, guardar)

    def _admin_toggle(self):
        a = self._admin_seleccionado()
        if not a:
            return
        a.activo = not a.activo
        self._refrescar_administrativos()
        self._set_status(f"Administrativo {a.identificacion} → {self._fila_activo(a.activo)}.")

    def _admin_eliminar(self):
        a = self._admin_seleccionado()
        if not a:
            return
        if confirmar_eliminar(self, f"a '{a.nombre_completo}' ({a.identificacion})"):
            self.administrativos.remove(a)
            self._refrescar_administrativos()
            self._set_status(f"Administrativo {a.identificacion} eliminado.")

    # ---------------- NÓMINA DOCENTE (solo consulta, sin CRUD) ----------------

    def _tab_nomina(self):
        self.tree_nomina, btns = self._crear_shell_tab(
            "nomina", "Nómina Docente", ["ID", "Nombre", "Vinculación", "Dedicación", "Programa", "Devengado Est.", "Neto Est."])

        self._btn(btns, "Ver desprendible", self._nomina_ver_seleccionado, estilo="accent")
        self._btn(btns, "Nómina Consolidada (~9k)", self._ver_nomina_masiva_gui, estilo="accent")
        tk.Label(btns, text="Consulta y auditoría salarial UPC.",
                 font=("Segoe UI", 8, "italic"), bg=C["card"], fg=C["muted"]).pack(side="left", padx=8)

        if "nomina" in self.search_vars:
            self.search_vars["nomina"].trace_add("write", lambda *_: self._refrescar_nomina())

        self.tree_nomina.bind("<Double-1>", lambda e: self._nomina_ver_seleccionado())
        self.refrescos_seccion["nomina"] = self._refrescar_nomina
        self._refrescar_nomina()

    def _refrescar_nomina(self):
        self.tree_nomina.delete(*self.tree_nomina.get_children())
        query = self.search_vars.get("nomina", tk.StringVar()).get().strip().lower()
        items = []
        for p in self.profesores:
            if query:
                if not (query in p.identificacion.lower() or query in p.nombre_completo.lower() or
                        query in p.tipo_vinculacion.lower() or query in p.codigo_programa.lower()):
                    continue
            items.append(p)

        visibles = items[:300]
        for p in visibles:
            if liquidacion_disponible(p):
                dev = calcular_total_devengado(p)
                bruto = calcular_salario_bruto(p)
                salud = calcular_descuento_salud(bruto)
                pension = calcular_descuento_pension(bruto)
                fsp = calcular_descuento_fsp(bruto)
                estampilla = calcular_descuento_estampilla(bruto)
                ret = calcular_retencion_fuente(dev, salud, pension)
                neto = dev - (salud + pension + fsp + estampilla + ret)
                dev_str = f"${dev:,.0f}"
                neto_str = f"${neto:,.0f}"
            else:
                dev_str = "No liquidable"
                neto_str = "—"

            self.tree_nomina.insert("", "end", iid=p.identificacion,
                values=(p.identificacion, p.nombre_completo, p.tipo_vinculacion,
                        p.dedicacion, p.codigo_programa, dev_str, neto_str))

        if "nomina" in self.info_labels:
            if len(items) > 300:
                self.info_labels["nomina"].config(
                    text=f"Mostrando primeros 300 de {len(items):,} docentes (Usa el buscador para filtrar en tiempo real).")
            else:
                self.info_labels["nomina"].config(text=f"Total: {len(items):,} de {len(self.profesores):,} docentes.")

    def _nomina_ver_seleccionado(self):
        sel = self.tree_nomina.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un profesor de la lista.")
            return
        p = buscar_profesor(self.profesores, sel[0])
        if p:
            VentanaNomina(self, p)

    # ---------------- OPERACIONES MASIVAS PARCIAL 1 ----------------

    def _generar_datos_masivos_gui(self):
        """Generador masivo del Parcial 1 con confirmación y cronometraje."""
        if not messagebox.askyesno(
            "Generación Masiva Parcial 1",
            "¿Deseas generar los datos masivos de la Universidad Popular del Cesar?\n\n"
            "Dimensiones del dataset:\n"
            "• 10 Facultades\n"
            "• 150 Programas (15 por facultad)\n"
            "• 9.000 Profesores (60 por programa)\n"
            "• 7.500 Cursos (50 por programa)\n"
            "• 225.000 Estudiantes (1.500 por programa)\n"
            "• ~850.000+ Calificaciones/Matrículas\n\n"
            "Este proceso toma entre 2 y 4 segundos.",
            icon="question", parent=self
        ):
            return

        self._set_status("Generando datos masivos... Por favor espera...")
        self.update_idletasks()
        t0 = time.perf_counter()

        facs, progs, profs, curs, ests = generar_datos_masivos()
        t_gen = time.perf_counter() - t0

        self.facultades = facs
        self.programas = progs
        self.profesores = profs
        self.cursos = curs
        self.estudiantes = ests

        self._refrescar_todas_las_vistas()
        if "panel" in self.secciones:
            self._construir_seccion_panel(self.secciones["panel"])

        total_notas = sum(len(e.matriculas) for e in self.estudiantes)
        msg = (
            f"¡Generación masiva completada con éxito en {t_gen:.2f} s!\n\n"
            f"• Facultades: {len(self.facultades):,}\n"
            f"• Programas: {len(self.programas):,}\n"
            f"• Profesores: {len(self.profesores):,}\n"
            f"• Cursos: {len(self.cursos):,}\n"
            f"• Estudiantes: {len(self.estudiantes):,}\n"
            f"• Matrículas/Notas: {total_notas:,}\n"
            f"• Administrativos: {len(self.administrativos):,}"
        )
        self._set_status(f"Datos masivos generados en {t_gen:.2f} s. Memoria lista.")
        messagebox.showinfo("Generación Masiva Completada", msg, parent=self)

    def _generar_horarios_gui(self):
        """Asignación masiva de horarios sin conflictos (42 slots, 400 salones)."""
        if not self.cursos:
            messagebox.showwarning("Sin cursos", "No hay cursos en memoria para asignar horarios.", parent=self)
            return

        t0 = time.perf_counter()
        asignados = generar_horarios_cursos(self.cursos)
        t_hor = time.perf_counter() - t0

        self._refrescar_cursos()
        if "panel" in self.secciones:
            self._construir_seccion_panel(self.secciones["panel"])

        resultado = {"total_cursos": asignados, "salones_utilizados": 400}
        self._set_status(f"Horarios generados en {t_hor:.2f} s. {asignados:,} cursos asignados.")
        VentanaHorariosResultado(self, resultado, t_hor)

    def _ver_nomina_masiva_gui(self):
        """Abre la ventana de nómina docente consolidada para toda la planta docente."""
        if not self.profesores:
            messagebox.showwarning("Sin profesores", "No hay profesores cargados en memoria.", parent=self)
            return
        VentanaNominaConsolidada(self, self.profesores)

    def _ver_erra_masivo_gui(self):
        """Abre la ventana de evaluación masiva de alertas académicas ERRA."""
        if not self.estudiantes:
            messagebox.showwarning("Sin estudiantes", "No hay estudiantes cargados en memoria.", parent=self)
            return
        VentanaErraConsolidado(self, self.estudiantes)

    def _ejecutar_proceso_completo_gui(self):
        """Ejecuta el pipeline completo del Parcial 1: Generación -> Horarios -> Nómina -> ERRA -> Guardar."""
        if not messagebox.askyesno(
            "Proceso Completo Parcial 1",
            "¿Deseas ejecutar el flujo integral del Parcial 1?\n\n"
            "1. Generación masiva (10 Fac, 150 Prog, 9k Prof, 7.5k Cursos, 225k Est, 850k Notas)\n"
            "2. Asignación algorítmica de horarios (42 slots, 400 salones, 0 conflictos)\n"
            "3. Evaluación académica ERRA institucional\n"
            "4. Liquidación consolidada de nómina docente\n"
            "5. Persistencia completa a archivos de texto plano (.txt)\n\n"
            "¿Continuar?", icon="question", parent=self
        ):
            return

        self._set_status("Ejecutando proceso integral del Parcial 1...")
        self.update_idletasks()
        t_inicio = time.perf_counter()

        # 1. Generación
        t0 = time.perf_counter()
        facs, progs, profs, curs, ests = generar_datos_masivos()
        t_gen = time.perf_counter() - t0
        self.facultades = facs
        self.programas = progs
        self.profesores = profs
        self.cursos = curs
        self.estudiantes = ests

        # 2. Horarios
        t0 = time.perf_counter()
        asignados = generar_horarios_cursos(self.cursos)
        t_hor = time.perf_counter() - t0
        res_hor = {"total_cursos": asignados, "salones_utilizados": 400}

        # 3. Nómina
        t0 = time.perf_counter()
        docentes_liq = 0
        total_dev = 0.0
        total_costo = 0.0
        for p in self.profesores:
            if liquidacion_disponible(p):
                docentes_liq += 1
                b = calcular_salario_bruto(p)
                dev = calcular_total_devengado(p)
                costo = calcular_costo_total_empleador(p)
                total_dev += dev
                total_costo += costo
        t_nom = time.perf_counter() - t0

        # 4. ERRA
        t0 = time.perf_counter()
        en_riesgo = 0
        satisfactorios = 0
        suma_promedios = 0.0
        for e in self.estudiantes:
            prom = e.calcular_promedio()
            suma_promedios += prom
            if e.esta_en_riesgo_ebra():
                en_riesgo += 1
            else:
                satisfactorios += 1
        t_erra = time.perf_counter() - t0
        prom_global = suma_promedios / len(self.estudiantes) if self.estudiantes else 0.0

        # 5. Persistencia
        t0 = time.perf_counter()
        self._guardar_datos()
        t_per = time.perf_counter() - t0

        t_total = time.perf_counter() - t_inicio
        self._refrescar_todas_las_vistas()
        if "panel" in self.secciones:
            self._construir_seccion_panel(self.secciones["panel"])

        resumen_msg = (
            f"¡Proceso Integral del Parcial 1 finalizado con éxito en {t_total:.2f} s!\n\n"
            f"1. Generación de datos: {t_gen:.2f} s\n"
            f"   • {len(self.facultades):,} Facultades | {len(self.programas):,} Programas\n"
            f"   • {len(self.profesores):,} Profesores | {len(self.cursos):,} Cursos\n"
            f"   • {len(self.estudiantes):,} Estudiantes | {sum(len(e.matriculas) for e in self.estudiantes):,} Notas\n\n"
            f"2. Horarios y Salones: {t_hor:.2f} s\n"
            f"   • {res_hor['total_cursos']:,} Cursos asignados en {res_hor['salones_utilizados']} salones (0 conflictos)\n\n"
            f"3. Nómina Consolidada: {t_nom:.2f} s\n"
            f"   • {docentes_liq:,} Docentes liquidados\n"
            f"   • Total Devengado: ${total_dev:,.0f} COP\n"
            f"   • Costo Institucional UPC: ${total_costo:,.0f} COP\n\n"
            f"4. Evaluación ERRA: {t_erra:.2f} s\n"
            f"   • {en_riesgo:,} en riesgo ({(en_riesgo/len(self.estudiantes))*100:.1f}%)\n"
            f"   • Promedio global UPC: {prom_global:.2f}\n\n"
            f"5. Persistencia a disco: {t_per:.2f} s"
        )
        self._set_status(f"Proceso completo finalizado en {t_total:.2f} s.")
        messagebox.showinfo("Proceso Completo Parcial 1", resumen_msg, parent=self)

    def _refrescar_todas_las_vistas(self):
        for refrescar in (self._refrescar_facultades, self._refrescar_programas, self._refrescar_cursos,
                          self._refrescar_estudiantes, self._refrescar_profesores, self._refrescar_administrativos,
                          self._refrescar_nomina):
            try:
                refrescar()
            except AttributeError:
                pass

    # ---------------- Persistencia (cargar / guardar / recargar) ----------------

    def _cargar_datos(self, silencioso=False):
        self.facultades = cargar_facultades(RUTA_FACULTADES)
        self.programas = cargar_programas(RUTA_PROGRAMAS)
        self.cursos = cargar_cursos(RUTA_CURSOS)
        self.estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
        self.profesores = cargar_profesores(RUTA_PROFESORES)
        self.administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
        self._refrescar_todas_las_vistas()
        msg = (f"Datos cargados: {len(self.facultades):,} facultades, {len(self.programas):,} programas, "
               f"{len(self.cursos):,} cursos, {len(self.estudiantes):,} estudiantes, "
               f"{len(self.profesores):,} profesores, {len(self.administrativos):,} administrativos.")
        self._set_status(msg)
        if not silencioso:
            messagebox.showinfo("Datos cargados", msg)

    def _recargar_datos(self):
        if messagebox.askyesno("Recargar datos", "Se perderá lo que no hayas guardado. ¿Continuar?"):
            self._cargar_datos()

    def _guardar_datos(self):
        guardar_facultades(self.facultades, RUTA_FACULTADES)
        guardar_programas(self.programas, RUTA_PROGRAMAS)
        guardar_cursos(self.cursos, RUTA_CURSOS)
        guardar_estudiantes(self.estudiantes, RUTA_ESTUDIANTES, RUTA_MATRICULAS)
        guardar_profesores(self.profesores, RUTA_PROFESORES)
        guardar_administrativos(self.administrativos, RUTA_ADMINISTRATIVOS)
        self._set_status("Datos guardados correctamente en disco.")

    def _salir(self):
        if messagebox.askyesno("Guardar antes de salir", "¿Deseas guardar los datos antes de salir?"):
            self._guardar_datos()
        self.destroy()


# ============================================================
# Ventanas modales y desprendibles de liquidación
# ============================================================

class VentanaEstudiante(tk.Toplevel):
    """Ficha académica compacta y auditable del estudiante."""
    def __init__(self, parent, estudiante):
        super().__init__(parent)
        self.title(f"Ficha estudiante — {estudiante.nombre_completo}")
        self.configure(bg=C["card"])
        self.geometry("600x480")
        self.minsize(540, 420)

        programa = buscar_programa(parent.programas, estudiante.codigo_programa)
        tk.Label(self, text=estudiante.nombre_completo, font=("Segoe UI", 13, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=16, pady=(14, 2))
        tk.Label(self, text=f"ID {estudiante.identificacion} · Programa: "
                            f"{programa.nombre if programa else estudiante.codigo_programa}",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=16, pady=(0, 8))

        promedio = estudiante.calcular_promedio()
        riesgo = estudiante.esta_en_riesgo_ebra()
        resumen = tk.Frame(self, bg=C["warn_bg"] if riesgo else C["ok_bg"])
        resumen.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(resumen, text=f"Estado: {estudiante.estado}", font=FONT_BOLD,
                 bg=resumen["bg"], fg=C["warn_fg"] if riesgo else C["ok_fg"]).pack(side="left", padx=10, pady=6)
        tk.Label(resumen, text=f"Promedio: {promedio:.2f}  ·  ERRA: {'EN RIESGO (<3.25)' if riesgo else 'Satisfactorio'}",
                 font=FONT_BOLD, bg=resumen["bg"],
                 fg=C["warn_fg"] if riesgo else C["ok_fg"]).pack(side="right", padx=10, pady=6)

        tk.Label(self, text=f"Cursos matriculados ({len(estudiante.matriculas)})", font=FONT_BOLD,
                 bg=C["card"], fg="#1a1a1a").pack(anchor="w", padx=16, pady=(2, 4))
        frame = tk.Frame(self, bg=C["card"])
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        tree = ttk.Treeview(frame, columns=("Código", "Curso", "Nota", "Profesor", "Horario"), show="headings")
        for col, width in (("Código", 75), ("Curso", 170), ("Nota", 60), ("Profesor", 105), ("Horario", 130)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="w")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        for m in estudiante.matriculas:
            curso = buscar_curso(parent.cursos, m["codigo_curso"])
            nombre = curso.nombre if curso else "(curso no encontrado)"
            profesor = curso.codigo_profesor if curso and curso.codigo_profesor else "—"
            horario_str = "—"
            if curso:
                dia = getattr(curso, "dia", "")
                h_ini = getattr(curso, "hora_inicio", 0)
                h_fin = getattr(curso, "hora_fin", 0)
                sal = getattr(curso, "salon", "")
                if dia and h_ini:
                    horario_str = f"{dia} {h_ini}:00-{h_fin}:00 (S.{sal})"
                elif dia:
                    horario_str = dia
            tree.insert("", "end", values=(m["codigo_curso"], nombre, f"{m['nota']:.2f}", profesor, horario_str))

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 12))
        self.transient(parent)
        self.grab_set()


class VentanaProfesorResumen(tk.Toplevel):
    def __init__(self, parent, profesor, curso=None):
        super().__init__(parent)
        self.title(f"Profesor — {profesor.nombre_completo}")
        self.configure(bg=C["card"])
        self.geometry("480x330")
        self.resizable(False, False)

        programa = buscar_programa(parent.programas, profesor.codigo_programa)
        tk.Label(self, text=profesor.nombre_completo, font=("Segoe UI", 13, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=16, pady=(14, 2))
        if curso:
            tk.Label(self, text=f"Asignado a: {curso.nombre} ({curso.codigo})", font=FONT,
                     bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=16, pady=(0, 8))

        datos = [
            ("Identificación", profesor.identificacion),
            ("Programa", programa.nombre if programa else profesor.codigo_programa),
            ("Vinculación", profesor.tipo_vinculacion),
            ("Dedicación", profesor.dedicacion),
            ("Categoría", profesor.categoria_escalafon or "Sin categoría"),
            ("Experiencia", f"{profesor.anios_experiencia} años"),
            ("Estado", "Activo" if profesor.activo else "Inactivo"),
        ]
        cuerpo = tk.Frame(self, bg=C["card"])
        cuerpo.pack(fill="x", padx=16, pady=2)
        for etiqueta, valor in datos:
            f = tk.Frame(cuerpo, bg=C["card"])
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"{etiqueta}:", font=FONT_BOLD, bg=C["card"]).pack(side="left")
            tk.Label(f, text=str(valor), font=FONT, bg=C["card"]).pack(side="right")

        acciones = tk.Frame(self, bg=C["card"])
        acciones.pack(pady=12)
        ttk.Button(acciones, text="Ver nómina", command=lambda: VentanaNomina(parent, profesor)).pack(side="left", padx=5)
        ttk.Button(acciones, text="Cerrar", command=self.destroy).pack(side="left", padx=5)
        self.transient(parent)
        self.grab_set()


class VentanaCursoDetalle(tk.Toplevel):
    def __init__(self, parent, curso):
        super().__init__(parent)
        self.title(f"Curso — {curso.nombre}")
        self.configure(bg=C["card"])
        self.geometry("660x480")
        self.minsize(580, 420)

        programa = buscar_programa(parent.programas, curso.codigo_programa)
        profesor = buscar_profesor(parent.profesores, curso.codigo_profesor) if curso.codigo_profesor else None
        matriculados = [e for e in parent.estudiantes
                        if any(m["codigo_curso"] == curso.codigo for m in e.matriculas)]

        tk.Label(self, text=curso.nombre, font=("Segoe UI", 13, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=16, pady=(14, 2))
        tk.Label(self, text=f"{curso.codigo} · {curso.creditos} créditos · "
                            f"{programa.nombre if programa else curso.codigo_programa}",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=16, pady=(0, 6))

        # Información de Horario y Salón
        dia = getattr(curso, "dia", "")
        h_ini = getattr(curso, "hora_inicio", 0)
        h_fin = getattr(curso, "hora_fin", 0)
        salon = getattr(curso, "salon", "")
        horario_box = tk.Frame(self, bg="#f4f7fa", highlightbackground="#d8dde3", highlightthickness=1)
        horario_box.pack(fill="x", padx=16, pady=(0, 8))
        
        if dia and h_ini:
            horario_txt = f"Horario asignado: {dia} {h_ini}:00-{h_fin}:00   |   Salón: {salon}"
        elif dia:
            horario_txt = f"Horario asignado: {dia}   |   Salón: {salon}"
        else:
            horario_txt = "Horario: Sin asignar"
        tk.Label(horario_box, text=horario_txt, font=FONT_BOLD, bg="#f4f7fa", fg=C["primary"]).pack(anchor="w", padx=8, pady=5)

        profbox = tk.Frame(self, bg="#f4f7fa", highlightbackground="#d8dde3", highlightthickness=1)
        profbox.pack(fill="x", padx=16, pady=(0, 8))
        tk.Label(profbox, text="Profesor asignado", font=FONT_BOLD,
                 bg="#f4f7fa", fg=C["primary"]).pack(anchor="w", padx=8, pady=(5, 1))
        texto_prof = profesor.nombre_completo if profesor else "Sin profesor asignado"
        tk.Label(profbox, text=texto_prof, font=FONT, bg="#f4f7fa", fg="#1a1a1a").pack(anchor="w", padx=8)
        if profesor:
            ttk.Button(profbox, text="Ver profesor", command=lambda: VentanaProfesorResumen(parent, profesor, curso)).pack(anchor="e", padx=8, pady=(3, 5))
        else:
            tk.Frame(profbox, bg="#f4f7fa", height=4).pack()

        tk.Label(self, text=f"Estudiantes matriculados ({len(matriculados)})", font=FONT_BOLD,
                 bg=C["card"], fg="#1a1a1a").pack(anchor="w", padx=16, pady=(2, 4))
        frame = tk.Frame(self, bg=C["card"])
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Programa", "Nota"), show="headings")
        for col, width in (("ID", 100), ("Nombre", 240), ("Programa", 85), ("Nota", 65)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="w")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        for e in matriculados[:300]:
            nota = next((m["nota"] for m in e.matriculas if m["codigo_curso"] == curso.codigo), 0.0)
            tree.insert("", "end", iid=e.identificacion,
                        values=(e.identificacion, e.nombre_completo, e.codigo_programa, f"{nota:.2f}"))

        def ver_estudiante(event=None):
            sel = tree.selection()
            if sel:
                est = buscar_estudiante(parent.estudiantes, sel[0])
                if est:
                    VentanaEstudiante(parent, est)
        tree.bind("<Double-1>", ver_estudiante)

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 10))
        self.transient(parent)
        self.grab_set()


class VentanaHorariosResultado(tk.Toplevel):
    """Resumen de la asignación algorítmica de horarios y salones."""
    def __init__(self, parent, resultado, tiempo_segundos):
        super().__init__(parent)
        self.title("Asignación de Horarios — Parcial 1 (UPC)")
        self.configure(bg=C["card"])
        self.geometry("540x380")
        self.resizable(False, False)

        tk.Label(self, text="Asignación Algorítmica de Horarios", font=("Segoe UI", 13, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=18, pady=(14, 2))
        tk.Label(self, text="Distribución en 42 franjas semanales (Lunes a Sábado, 6:00 - 20:00)",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=18, pady=(0, 10))

        card = tk.Frame(self, bg="#f4f7fa", highlightbackground="#d8dde3", highlightthickness=1)
        card.pack(fill="x", padx=18, pady=(0, 12))

        metricas = [
            ("Total Cursos Procesados", f"{resultado.get('total_cursos', 0):,}"),
            ("Total Cursos con Horario", f"{resultado.get('total_cursos', 0):,}"),
            ("Salones Utilizados", f"{resultado.get('salones_utilizados', 400)} (1 a 400)"),
            ("Franjas Horarias Disponibles", "42 slots (7 franjas × 6 días)"),
            ("Conflictos de Horario/Salón", "0 (Garantizado por algoritmo)"),
            ("Tiempo de Ejecución", f"{tiempo_segundos:.3f} s"),
        ]
        for lab, val in metricas:
            f = tk.Frame(card, bg="#f4f7fa")
            f.pack(fill="x", padx=12, pady=3)
            tk.Label(f, text=f"{lab}:", font=FONT_BOLD, bg="#f4f7fa", fg="#1f4e79").pack(side="left")
            color_val = C["accent"] if "0" in val and "Conflictos" in lab else "#111827"
            tk.Label(f, text=val, font=FONT_BOLD, bg="#f4f7fa", fg=color_val).pack(side="right")

        tk.Label(self, text="Todos los cursos tienen aula y horario asignados sin colisiones.",
                 font=FONT_BOLD, bg=C["card"], fg=C["accent"]).pack(pady=4)

        ttk.Button(self, text="Aceptar", command=self.destroy).pack(pady=(4, 14))
        self.transient(parent)
        self.grab_set()


class VentanaNominaConsolidada(tk.Toplevel):
    """Auditoría y reporte consolidado de nómina docente institucional UPC."""
    def __init__(self, parent, profesores):
        super().__init__(parent)
        self.title("Nómina Docente Consolidada — UPC (Parcial 1)")
        self.configure(bg="#eef2f6")
        self.geometry("680x560")
        self.minsize(600, 480)

        t0 = time.perf_counter()
        count_planta = 0
        count_ocasional = 0
        count_catedra = 0
        count_liq = 0

        tot_dev = 0.0
        tot_salud = 0.0
        tot_pension = 0.0
        tot_fsp = 0.0
        tot_estampilla = 0.0
        tot_ret = 0.0
        tot_ded = 0.0
        tot_neto = 0.0
        tot_costo = 0.0
        tot_ps = 0.0

        for p in profesores:
            if p.tipo_vinculacion == "Planta":
                count_planta += 1
            elif p.tipo_vinculacion == "Ocasional":
                count_ocasional += 1
            else:
                count_catedra += 1

            if liquidacion_disponible(p):
                count_liq += 1
                b = calcular_salario_bruto(p)
                dev = calcular_total_devengado(p)
                s_e = calcular_descuento_salud(b)
                p_e = calcular_descuento_pension(b)
                f_e = calcular_descuento_fsp(b)
                est = calcular_descuento_estampilla(b)
                ret = calcular_retencion_fuente(dev, s_e, p_e)
                ded = s_e + p_e + f_e + est + ret
                net = dev - ded
                costo = calcular_costo_total_empleador(p)
                ps = calcular_total_prestaciones(b)

                tot_dev += dev
                tot_salud += s_e
                tot_pension += p_e
                tot_fsp += f_e
                tot_estampilla += est
                tot_ret += ret
                tot_ded += ded
                tot_neto += net
                tot_costo += costo
                tot_ps += ps

        t_calc = time.perf_counter() - t0

        top = tk.Frame(self, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        top.pack(fill="x", padx=16, pady=(12, 8))
        tk.Label(top, text="Consolidado de Nómina Docente Institucional",
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#1f4e79").pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(top, text=f"Total Docentes: {len(profesores):,} ({count_planta:,} Planta, {count_ocasional:,} Ocasionales, {count_catedra:,} Cátedra)  ·  Calculado en {t_calc*1000:.1f} ms",
                 font=FONT, bg="white", fg="#6b7280").pack(anchor="w", padx=14, pady=(0, 10))

        card_dev = tk.Frame(self, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_dev.pack(fill="x", padx=16, pady=(0, 6))
        
        def fila(par, label, valor, color="#111827", bold=False):
            f = tk.Frame(par, bg="white")
            f.pack(fill="x", padx=14, pady=2)
            tk.Label(f, text=label, font=FONT_BOLD if bold else FONT, bg="white", fg="#374151" if not bold else "#111827").pack(side="left")
            tk.Label(f, text=valor, font=FONT_BOLD if bold else FONT, bg="white", fg=color).pack(side="right")

        fila(card_dev, "TOTAL DEVENGADOS MENSUALES (+)", f"$ {tot_dev:,.0f} COP", color="#1d4ed8", bold=True)
        fila(card_dev, "TOTAL DEDUCCIONES DE LEY (-)", f"- $ {tot_ded:,.0f} COP", color="#dc2626", bold=True)
        fila(card_dev, "  • Salud Empleado (4%)", f"- $ {tot_salud:,.0f} COP", color="#6b7280")
        fila(card_dev, "  • Pensión Empleado (4%)", f"- $ {tot_pension:,.0f} COP", color="#6b7280")
        fila(card_dev, "  • Fondo Solidaridad Pensional (1%)", f"- $ {tot_fsp:,.0f} COP", color="#6b7280")
        fila(card_dev, "  • Estampilla Pro-UPC (0.2%)", f"- $ {tot_estampilla:,.0f} COP", color="#6b7280")
        fila(card_dev, "  • Retención en la Fuente (Art. 383 E.T.)", f"- $ {tot_ret:,.0f} COP", color="#6b7280")
        tk.Frame(card_dev, bg="white", height=3).pack()

        neto_frame = tk.Frame(self, bg="white", highlightbackground="#10b981", highlightthickness=2)
        neto_frame.pack(fill="x", padx=16, pady=(0, 6))
        fila(neto_frame, "TOTAL NETO A GIRAR A DOCENTES:", f"$ {tot_neto:,.0f} COP", color="#059669", bold=True)

        card_costo = tk.Frame(self, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_costo.pack(fill="x", padx=16, pady=(0, 8))
        fila(card_costo, "COSTO TOTAL EMPLEADOR UPC (Nómina + Aportes Patronales):", f"$ {tot_costo:,.0f} COP", color="#d97706", bold=True)
        fila(card_costo, "Provisión Mensual Prestaciones Sociales (Ley 52 / Dto 1279):", f"$ {tot_ps:,.0f} COP", color="#059669")

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(2, 12))
        self.transient(parent)
        self.grab_set()


class VentanaErraConsolidado(tk.Toplevel):
    """Auditoría y estadísticas globales de alertas tempranas académicas ERRA."""
    def __init__(self, parent, estudiantes):
        super().__init__(parent)
        self.title("Alertas Académicas ERRA / EBRA — Parcial 1 (UPC)")
        self.configure(bg="#eef2f6")
        self.geometry("700x560")
        self.minsize(620, 480)

        t0 = time.perf_counter()
        total = len(estudiantes)
        en_riesgo = []
        satisfactorios = 0
        suma_promedios = 0.0

        for e in estudiantes:
            prom = e.calcular_promedio()
            suma_promedios += prom
            if e.esta_en_riesgo_ebra():
                en_riesgo.append(e)
            else:
                satisfactorios += 1

        t_calc = time.perf_counter() - t0
        prom_global = suma_promedios / total if total > 0 else 0.0
        pct_riesgo = (len(en_riesgo) / total * 100) if total > 0 else 0.0
        pct_sat = (satisfactorios / total * 100) if total > 0 else 0.0

        top = tk.Frame(self, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        top.pack(fill="x", padx=16, pady=(12, 8))
        tk.Label(top, text="Evaluación Académica ERRA (Regla: Promedio < 3.25)",
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#1f4e79").pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(top, text=f"Total Estudiantes Evaluados: {total:,}  ·  Evaluado en {t_calc*1000:.1f} ms",
                 font=FONT, bg="white", fg="#6b7280").pack(anchor="w", padx=14, pady=(0, 8))

        stats_frame = tk.Frame(self, bg="#eef2f6")
        stats_frame.pack(fill="x", padx=16, pady=(0, 8))

        def card_stat(par, col, tit, val, sub, bg_c, fg_c):
            c = tk.Frame(par, bg=bg_c, highlightbackground="#dce2ea", highlightthickness=1)
            c.grid(row=0, column=col, padx=4, sticky="nsew")
            par.grid_columnconfigure(col, weight=1)
            tk.Label(c, text=tit, font=("Segoe UI", 8, "bold"), bg=bg_c, fg="#6b7280").pack(pady=(6, 0))
            tk.Label(c, text=val, font=("Segoe UI", 14, "bold"), bg=bg_c, fg=fg_c).pack()
            tk.Label(c, text=sub, font=("Segoe UI", 8), bg=bg_c, fg="#6b7280").pack(pady=(0, 6))

        card_stat(stats_frame, 0, "EN RIESGO (<3.25)", f"{len(en_riesgo):,}", f"{pct_riesgo:.1f}% de la población", "#fdecea", "#c0392b")
        card_stat(stats_frame, 1, "SATISFACTORIOS (≥3.25)", f"{satisfactorios:,}", f"{pct_sat:.1f}% de la población", "#e8f5e9", "#2e7d32")
        card_stat(stats_frame, 2, "PROMEDIO GLOBAL", f"{prom_global:.2f}", "Promedio UPC", "white", "#1f4e79")

        tk.Label(self, text=f"Muestra de Estudiantes en Riesgo Académico ({len(en_riesgo):,} total):",
                 font=FONT_BOLD, bg="#eef2f6", fg="#111827").pack(anchor="w", padx=16, pady=(3, 3))

        tree_frame = tk.Frame(self, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Programa", "Promedio", "Cursos"), show="headings")
        for col, width in (("ID", 95), ("Nombre", 220), ("Programa", 90), ("Promedio", 75), ("Cursos", 65)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="w")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        for e in en_riesgo[:300]:
            tree.insert("", "end", iid=e.identificacion,
                        values=(e.identificacion, e.nombre_completo, e.codigo_programa,
                                f"{e.calcular_promedio():.2f}", len(e.matriculas)))

        def ver_ficha(e=None):
            sel = tree.selection()
            if sel:
                est = buscar_estudiante(parent.estudiantes, sel[0])
                if est:
                    VentanaEstudiante(parent, est)
        tree.bind("<Double-1>", ver_ficha)

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 10))
        self.transient(parent)
        self.grab_set()


class VentanaNomina(tk.Toplevel):
    """Desprendible Oficial de Pago de Nómina (formato institucional auditable UPC)."""
    def __init__(self, parent, profesor):
        super().__init__(parent)
        self.title(f"Desprendible de Liquidación - {profesor.nombre_completo}")
        self.configure(bg="#eef2f6")
        self.resizable(True, True)
        self.geometry("620x780")
        self.minsize(560, 640)
        self.periodo = "mensual"

        canvas = tk.Canvas(self, bg="#eef2f6", highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#eef2f6")
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        card_header = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_header.pack(fill="x", padx=16, pady=(14, 10))

        top_h = tk.Frame(card_header, bg="white")
        top_h.pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(top_h, text="Desprendible Oficial de Pago de Nómina",
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#111827").pack(side="left")
        self.btn_periodo = ttk.Button(top_h, text="Ver anual", command=self._alternar_periodo)
        self.btn_periodo.pack(side="right")

        liq_num = abs(hash(profesor.identificacion)) % 900 + 100
        sub_info = f"Docente: {profesor.nombre_completo}  |  Modalidad: {profesor.tipo_vinculacion.upper()}  |  Liquidación N° {liq_num}"
        tk.Label(card_header, text=sub_info, font=("Segoe UI", 8), bg="white", fg="#6b7280").pack(anchor="w", padx=14, pady=(0, 4))

        self.lbl_periodo_fechas = tk.Label(card_header, text="Período Liquidado: Marzo 2026 · 01/03/2026 - 31/03/2026",
                                            font=("Segoe UI", 8, "bold"), bg="white", fg="#1d4ed8")
        self.lbl_periodo_fechas.pack(anchor="w", padx=14, pady=(0, 12))

        bruto = calcular_salario_bruto(profesor)
        disponible = liquidacion_disponible(profesor)

        if not disponible:
            self.btn_periodo.pack_forget()
            aviso = tk.Frame(inner, bg=C["warn_bg"], highlightbackground="#fca5a5", highlightthickness=1)
            aviso.pack(fill="x", padx=16, pady=8)
            tk.Label(aviso, text="NO SE LIQUIDA UN SALARIO INVENTADO",
                     font=FONT_BOLD, bg=C["warn_bg"], fg=C["warn_fg"]).pack(padx=12, pady=(8, 2))
            tk.Label(aviso, text="Falta el valor de hora cátedra fijado por resolución rectoral vigente.",
                     font=("Segoe UI", 8), bg=C["warn_bg"], fg=C["warn_fg"], wraplength=460).pack(padx=12, pady=(0, 8))
            return

        bonif_posg = calcular_bonificacion_posgrado(profesor)
        devengado  = calcular_total_devengado(profesor)

        salud_e    = calcular_descuento_salud(bruto)
        pension_e  = calcular_descuento_pension(bruto)
        fsp_e      = calcular_descuento_fsp(bruto)
        estampilla = calcular_descuento_estampilla(bruto)
        retencion  = calcular_retencion_fuente(devengado, salud_e, pension_e)
        total_ded  = salud_e + pension_e + fsp_e + estampilla + retencion
        neto       = devengado - total_ded

        ap = calcular_aportes_patronales(bruto)
        costo_upc = bruto + ap["total"]

        def crear_tarjeta(titulo, subtotal_txt="", color_titulo="#1f4e79"):
            card = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
            card.pack(fill="x", padx=16, pady=(0, 10))

            header_t = tk.Frame(card, bg="white")
            header_t.pack(fill="x", padx=14, pady=(10, 6))
            tk.Label(header_t, text=titulo, font=("Segoe UI", 9, "bold"),
                     bg="white", fg=color_titulo).pack(side="left")
            lbl_sub = None
            if subtotal_txt:
                lbl_sub = tk.Label(header_t, text=subtotal_txt, font=("Segoe UI", 9, "bold"),
                                   bg="white", fg=color_titulo)
                lbl_sub.pack(side="right")
            return card, lbl_sub

        def fila_card(parent, label, valor, bold=False, color="#111827"):
            f = tk.Frame(parent, bg="white")
            f.pack(fill="x", padx=14, pady=2)
            tk.Label(f, text=label, font=FONT_BOLD if bold else FONT,
                     bg="white", fg="#374151" if not bold else "#111827").pack(side="left")
            lbl = tk.Label(f, text=valor, font=FONT_BOLD if bold else FONT,
                           bg="white", fg=color)
            lbl.pack(side="right")
            return lbl

        # 1. DEVENGADOS Y ASIGNACIONES (+)
        card_dev, self.lbl_sub_dev = crear_tarjeta(
            "DEVENGADOS Y ASIGNACIONES (+)", f"$ {devengado:,.0f} COP", color_titulo="#1d4ed8")
        if profesor.tipo_vinculacion == "Planta":
            pts = total_puntos(profesor)
            desc_asig = f"Sueldo Básico ({pts} pts × ${VALOR_PUNTO:,.0f})"
        elif profesor.tipo_vinculacion == "Ocasional":
            fact = factor_ocasional(profesor) or 0.0
            desc_asig = f"Sueldo Básico ({fact:.3f} SMMLV × ${SMMLV:,.0f})"
        else:
            desc_asig = "Sueldo Básico"
        self.lbl_asig_val = fila_card(card_dev, desc_asig, f"+ $ {bruto:,.0f} COP", bold=True, color="#1d4ed8")

        self.lbl_bonif_posg = None
        if bonif_posg > 0:
            posg_nombre = getattr(profesor, "posgrado", "Postgrado")
            self.lbl_bonif_posg = fila_card(
                card_dev, f"Bonificación Cualificación {posg_nombre} (Acuerdo 027/2024)",
                f"+ $ {bonif_posg:,.0f} COP", color="#1d4ed8"
            )
        tk.Frame(card_dev, bg="white", height=4).pack()

        # 2. DEDUCCIONES OBLIGATORIAS DE LEY (-)
        card_ded, self.lbl_sub_ded = crear_tarjeta(
            "DEDUCCIONES OBLIGATORIAS DE LEY (-)", f"$ {total_ded:,.0f} COP", color_titulo="#dc2626")
        self.lbl_ibc_ded = fila_card(card_ded, "IBC Seguridad Social (Base Cotización):", f"$ {bruto:,.0f} COP", bold=True)
        tk.Frame(card_ded, bg="white", height=3).pack()
        self.lbl_estampilla_val = fila_card(card_ded, "Descuento Estampilla Pro-UPC (0.2%)", f"- $ {estampilla:,} COP", color="#dc2626")
        self.lbl_retencion_val = fila_card(card_ded, "Retención en la Fuente por Salario (Art. 383 E.T.)",
                                          f"- $ {retencion:,} COP" if retencion > 0 else "$ 0 COP",
                                          color="#dc2626" if retencion > 0 else "#6b7280")
        self.lbl_pension_val = fila_card(card_ded, "Aporte Pensión Empleado (4% PILA)", f"- $ {pension_e:,} COP", color="#dc2626")
        self.lbl_salud_val = fila_card(card_ded, "Aporte Salud Empleado (4% PILA)", f"- $ {salud_e:,} COP", color="#dc2626")
        self.lbl_fsp_val = fila_card(card_ded, "Fondo de Solidaridad Pensional (1%)", f"- $ {fsp_e:,} COP" if fsp_e > 0 else "$ 0 COP", color="#dc2626" if fsp_e > 0 else "#6b7280")
        tk.Frame(card_ded, bg="white", height=4).pack()

        # 3. COSTO TOTAL EMPLEADOR (UPC)
        card_costo, self.lbl_sub_costo = crear_tarjeta(
            "COSTO TOTAL EMPLEADOR (UPC)", f"$ {costo_upc:,.0f} COP", color_titulo="#d97706")
        self.lbl_costo_asig = fila_card(card_costo, "Asignación Básica", f"$ {bruto:,.0f} COP", bold=True, color="#1d4ed8")
        self.lbl_ap_salud = fila_card(card_costo, "Salud Patronal (8.5%)", f"$ {ap['salud']:,} COP", color="#4b5563")
        self.lbl_ap_pension = fila_card(card_costo, "Pensión Patronal (12%)", f"$ {ap['pension']:,} COP", color="#4b5563")
        self.lbl_ap_arl = fila_card(card_costo, "Aporte Riesgos Laborales (ARL)", f"$ {ap['arl']:,} COP", color="#4b5563")
        self.lbl_ap_caja = fila_card(card_costo, "Caja de Compensación Familiar (4%)", f"$ {ap['caja']:,} COP", color="#4b5563")
        tk.Frame(card_costo, bg="#f3f4f6", height=1).pack(fill="x", padx=14, pady=4)
        self.lbl_costo_total_upc = fila_card(card_costo, "TOTAL COSTO UPC", f"$ {costo_upc:,.0f} COP", bold=True, color="#1d4ed8")
        tk.Frame(card_costo, bg="white", height=4).pack()

        # 4. INFORMACIÓN SALARIAL DOCENTE (DECRETO 1279 / ACUERDO 027)
        reg_title = "INFORMACIÓN SALARIAL DOCENTE (DECRETO 1279)" if profesor.tipo_vinculacion == "Planta" else f"INFORMACIÓN SALARIAL ({regimen_nomina(profesor).upper()})"
        card_info, _ = crear_tarjeta(reg_title, "", color_titulo="#2563eb")
        if profesor.tipo_vinculacion == "Planta":
            fila_card(card_info, "Categoría Docente:", (profesor.categoria_escalafon or "—").upper(), bold=True)
            self.lbl_info_pts = fila_card(card_info, "Total Puntos Salariales:", f"{total_puntos(profesor)} pts", bold=True)
            fila_card(card_info, "Valor Punto Salarial:", f"$ {VALOR_PUNTO:,.0f} COP", bold=True)
            self.lbl_calc_asig = fila_card(card_info, "Cálculo Asignación Básica:", f"{total_puntos(profesor)} pts × ${VALOR_PUNTO:,.0f} COP", bold=True)
            self.lbl_ibc_info = fila_card(card_info, "IBC Seguridad Social:", f"$ {bruto:,.0f} COP", bold=True)
        elif profesor.tipo_vinculacion == "Ocasional":
            fila_card(card_info, "Categoría Docente:", (profesor.categoria_escalafon or "—").upper(), bold=True)
            fila_card(card_info, "Dedicación:", profesor.dedicacion, bold=True)
            if getattr(profesor, "posgrado", ""):
                fila_card(card_info, "Cualificación Posgrado:", profesor.posgrado, bold=True)
            fact = factor_ocasional(profesor) or 0.0
            fila_card(card_info, "Factor Acuerdo UPC 027:", f"{fact:.3f} SMMLV", bold=True)
            fila_card(card_info, "SMMLV 2026 Vigente:", f"$ {SMMLV:,.0f} COP", bold=True)
            self.lbl_ibc_info = fila_card(card_info, "IBC Seguridad Social:", f"$ {bruto:,.0f} COP", bold=True)
        else:
            fila_card(card_info, "Horas Cátedra Semanales:", str(profesor.horas_catedra_semanales), bold=True)
            self.lbl_ibc_info = fila_card(card_info, "IBC Seguridad Social:", f"$ {bruto:,.0f} COP", bold=True)
        tk.Frame(card_info, bg="white", height=4).pack()

        # 5. PROVISIONES PRESTACIONALES CONTABLES (ACUMULADO AUDITABLE)
        card_ps, self.lbl_sub_ps = crear_tarjeta("PROVISIÓN PRESTACIONES SOCIALES (LEY 52 / DTO 1279)", f"$ {calcular_total_prestaciones(bruto):,.0f} COP", color_titulo="#059669")
        prima_s  = calcular_prima_servicios(bruto)
        ces      = calcular_cesantias(bruto)
        int_ces  = calcular_intereses_cesantias(bruto)
        p_nav    = calcular_prima_navidad(bruto)
        vac      = calcular_vacaciones(bruto)
        p_vac    = calcular_prima_vacaciones(bruto)
        bonif    = calcular_bonificacion_servicios(bruto)
        self.lbl_ps_prima_s = fila_card(card_ps, "Prima de Servicios (Art. 44 Dto. 1279)", f"$ {prima_s:,.0f} COP")
        self.lbl_ps_ces     = fila_card(card_ps, "Cesantías (Art. 45 Dto. 1279)", f"$ {ces:,.0f} COP")
        self.lbl_ps_int_ces = fila_card(card_ps, "Intereses a Cesantías (Ley 52/1975 1%/mes)", f"$ {int_ces:,.0f} COP")
        self.lbl_ps_p_nav   = fila_card(card_ps, "Prima de Navidad (Dto. 1042/1978 Art. 33)", f"$ {p_nav:,.0f} COP")
        self.lbl_ps_vac     = fila_card(card_ps, "Vacaciones (15 días hábiles/año)", f"$ {vac:,.0f} COP")
        self.lbl_ps_p_vac   = fila_card(card_ps, "Prima de Vacaciones (Dto. 1279 Art. 33)", f"$ {p_vac:,.0f} COP")
        self.lbl_ps_bonif   = fila_card(card_ps, "Bonificación por Servicios (Dto. 1279 Art. 39)", f"$ {bonif:,.0f} COP")
        tk.Frame(card_ps, bg="white", height=4).pack()

        # 6. BANNER NETO A PAGAR
        neto_box = tk.Frame(inner, bg="white", highlightbackground="#10b981", highlightthickness=2)
        neto_box.pack(fill="x", padx=16, pady=(4, 14))

        neto_top = tk.Frame(neto_box, bg="white")
        neto_top.pack(fill="x", padx=14, pady=(10, 3))
        tk.Label(neto_top, text="NETO A PAGAR:", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#111827").pack(side="left")
        self.lbl_neto_val = tk.Label(neto_top, text=f"$ {neto:,.0f} COP",
                                     font=("Segoe UI", 13, "bold"), bg="white", fg="#059669")
        self.lbl_neto_val.pack(side="right")

        self.lbl_neto_resumen = tk.Label(
            neto_box,
            text=f"Total Devengado: $ {devengado:,.0f} COP  ·  Total Deducciones: -$ {total_ded:,.0f} COP",
            font=("Segoe UI", 8), bg="white", fg="#6b7280"
        )
        self.lbl_neto_resumen.pack(anchor="w", padx=14, pady=(0, 10))

        self._val = {
            "bruto": bruto, "bonif_posg": bonif_posg, "devengado": devengado,
            "total_ded": total_ded, "estampilla": estampilla, "retencion": retencion,
            "salud_e": salud_e, "pension_e": pension_e, "fsp_e": fsp_e,
            "costo_upc": costo_upc, "ap_salud": ap["salud"], "ap_pension": ap["pension"],
            "ap_arl": ap["arl"], "ap_caja": ap["caja"], "neto": neto,
            "total_ps": calcular_total_prestaciones(bruto),
            "prima_s": prima_s, "ces": ces, "int_ces": int_ces, "p_nav": p_nav,
            "vac": vac, "p_vac": p_vac, "bonif": bonif,
        }

        ttk.Button(inner, text="Cerrar", command=self.destroy).pack(pady=(0, 16))
        self.transient(parent)
        self.grab_set()

    def _alternar_periodo(self):
        """Alterna entre vista mensual y anual."""
        if not hasattr(self, "_val"):
            return
        v = self._val
        if self.periodo == "mensual":
            self.periodo = "anual"
            f = 12
            self.btn_periodo.configure(text="Ver mensual")
            self.lbl_periodo_fechas.configure(text="Período Liquidado: Año Vigente 2026 (Consolidado 12 Meses)")
        else:
            self.periodo = "mensual"
            f = 1
            self.btn_periodo.configure(text="Ver anual")
            self.lbl_periodo_fechas.configure(text="Período Liquidado: Marzo 2026 · 01/03/2026 - 31/03/2026")

        self.lbl_sub_dev.configure(text=f"$ {v['devengado']*f:,.0f} COP")
        self.lbl_asig_val.configure(text=f"+ $ {v['bruto']*f:,.0f} COP")
        if self.lbl_bonif_posg and v["bonif_posg"] > 0:
            self.lbl_bonif_posg.configure(text=f"+ $ {v['bonif_posg']*f:,.0f} COP")

        self.lbl_sub_ded.configure(text=f"$ {v['total_ded']*f:,.0f} COP")
        self.lbl_ibc_ded.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_estampilla_val.configure(text=f"- $ {v['estampilla']*f:,} COP")
        self.lbl_retencion_val.configure(text=f"- $ {v['retencion']*f:,} COP" if v['retencion'] > 0 else "$ 0 COP")
        self.lbl_pension_val.configure(text=f"- $ {v['pension_e']*f:,} COP")
        self.lbl_salud_val.configure(text=f"- $ {v['salud_e']*f:,} COP")
        self.lbl_fsp_val.configure(text=f"- $ {v['fsp_e']*f:,} COP" if v['fsp_e'] > 0 else "$ 0 COP")

        self.lbl_sub_costo.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")
        self.lbl_costo_asig.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_ap_salud.configure(text=f"$ {v['ap_salud']*f:,} COP")
        self.lbl_ap_pension.configure(text=f"$ {v['ap_pension']*f:,} COP")
        self.lbl_ap_arl.configure(text=f"$ {v['ap_arl']*f:,} COP")
        self.lbl_ap_caja.configure(text=f"$ {v['ap_caja']*f:,} COP")
        self.lbl_costo_total_upc.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")

        if hasattr(self, "lbl_ibc_info"):
            self.lbl_ibc_info.configure(text=f"$ {v['bruto']*f:,.0f} COP")

        self.lbl_sub_ps.configure(text=f"$ {v['total_ps']*f:,.0f} COP")
        self.lbl_ps_prima_s.configure(text=f"$ {v['prima_s']*f:,.0f} COP")
        self.lbl_ps_ces.configure(text=f"$ {v['ces']*f:,.0f} COP")
        self.lbl_ps_int_ces.configure(text=f"$ {v['int_ces']*f:,.0f} COP")
        self.lbl_ps_p_nav.configure(text=f"$ {v['p_nav']*f:,.0f} COP")
        self.lbl_ps_vac.configure(text=f"$ {v['vac']*f:,.0f} COP")
        self.lbl_ps_p_vac.configure(text=f"$ {v['p_vac']*f:,.0f} COP")
        self.lbl_ps_bonif.configure(text=f"$ {v['bonif']*f:,.0f} COP")

        self.lbl_neto_val.configure(text=f"$ {v['neto']*f:,.0f} COP")
        self.lbl_neto_resumen.configure(text=f"Total Devengado: $ {v['devengado']*f:,.0f} COP  ·  Total Deducciones: -$ {v['total_ded']*f:,.0f} COP")


class VentanaSalarioAdmin(tk.Toplevel):
    """Desprendible Oficial de Pago de Nómina Administrativa (UPC)."""
    def __init__(self, parent, admin):
        super().__init__(parent)
        self.title(f"Desprendible Administrativo - {admin.nombre_completo}")
        self.configure(bg="#eef2f6")
        self.resizable(True, True)
        self.geometry("620x740")
        self.minsize(560, 600)
        self.periodo = "mensual"

        canvas = tk.Canvas(self, bg="#eef2f6", highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#eef2f6")
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        card_header = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_header.pack(fill="x", padx=16, pady=(14, 10))

        top_h = tk.Frame(card_header, bg="white")
        top_h.pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(top_h, text="Desprendible Oficial de Pago - Personal Administrativo",
                 font=("Segoe UI", 11, "bold"), bg="white", fg="#111827").pack(side="left")
        self.btn_periodo = ttk.Button(top_h, text="Ver anual", command=self._alternar_periodo)
        self.btn_periodo.pack(side="right")

        facultad = admin.codigo_facultad if admin.codigo_facultad else "Nivel Central"
        liq_num = abs(hash(admin.identificacion)) % 900 + 100
        sub_info = f"Funcionario: {admin.nombre_completo}  |  Cargo: {admin.cargo} ({admin.categoria})  |  Liquidación N° {liq_num}"
        tk.Label(card_header, text=sub_info, font=("Segoe UI", 8), bg="white", fg="#6b7280").pack(anchor="w", padx=14, pady=(0, 4))
        tk.Label(card_header, text=f"Contratación: {admin.tipo_contratacion}  |  Adscrito a: {facultad}",
                 font=("Segoe UI", 8, "italic"), bg="white", fg="#4b5563").pack(anchor="w", padx=14, pady=(0, 4))

        self.lbl_periodo_fechas = tk.Label(card_header, text="Período Liquidado: Marzo 2026 · 01/03/2026 - 31/03/2026",
                                            font=("Segoe UI", 8, "bold"), bg="white", fg="#1d4ed8")
        self.lbl_periodo_fechas.pack(anchor="w", padx=14, pady=(0, 12))

        bruto     = calcular_salario_bruto_admin(admin)
        salud_e   = calcular_descuento_salud_admin(bruto)
        pension_e = calcular_descuento_pension_admin(bruto)
        fsp_e     = calcular_descuento_fsp_admin(bruto)
        total_ded = salud_e + pension_e + fsp_e
        neto      = bruto - total_ded

        ap = calcular_aportes_patronales_admin(bruto)
        costo_upc = bruto + ap["total"]

        def crear_tarjeta(titulo, subtotal_txt="", color_titulo="#1f4e79"):
            card = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
            card.pack(fill="x", padx=16, pady=(0, 10))

            header_t = tk.Frame(card, bg="white")
            header_t.pack(fill="x", padx=14, pady=(10, 6))
            tk.Label(header_t, text=titulo, font=("Segoe UI", 9, "bold"),
                     bg="white", fg=color_titulo).pack(side="left")
            lbl_sub = None
            if subtotal_txt:
                lbl_sub = tk.Label(header_t, text=subtotal_txt, font=("Segoe UI", 9, "bold"),
                                   bg="white", fg=color_titulo)
                lbl_sub.pack(side="right")
            return card, lbl_sub

        def fila_card(parent, label, valor, bold=False, color="#111827"):
            f = tk.Frame(parent, bg="white")
            f.pack(fill="x", padx=14, pady=2)
            tk.Label(f, text=label, font=FONT_BOLD if bold else FONT,
                     bg="white", fg="#374151" if not bold else "#111827").pack(side="left")
            lbl = tk.Label(f, text=valor, font=FONT_BOLD if bold else FONT,
                           bg="white", fg=color)
            lbl.pack(side="right")
            return lbl

        # 1. DEVENGADOS Y ASIGNACIONES (+)
        card_dev, self.lbl_sub_dev = crear_tarjeta(
            "DEVENGADOS Y ASIGNACIONES (+)", f"$ {bruto:,.0f} COP", color_titulo="#1d4ed8")
        desc_asig = f"Asignación Salarial Base ({admin.categoria} - Decretos Salariales 2026)"
        self.lbl_asig_val = fila_card(card_dev, desc_asig, f"+ $ {bruto:,.0f} COP", bold=True, color="#1d4ed8")
        tk.Frame(card_dev, bg="white", height=4).pack()

        # 2. DEDUCCIONES OBLIGATORIAS DE LEY (-)
        card_ded, self.lbl_sub_ded = crear_tarjeta(
            "DEDUCCIONES OBLIGATORIAS DE LEY (-)", f"$ {total_ded:,.0f} COP", color_titulo="#dc2626")
        self.lbl_ibc_ded = fila_card(card_ded, "IBC Seguridad Social (Base Cotización):", f"$ {bruto:,.0f} COP", bold=True)
        tk.Frame(card_ded, bg="white", height=3).pack()
        self.lbl_salud_val = fila_card(card_ded, "Aporte Salud Trabajador (4%)", f"- $ {salud_e:,} COP", color="#dc2626")
        self.lbl_pension_val = fila_card(card_ded, "Aporte Pensión Trabajador (4%)", f"- $ {pension_e:,} COP", color="#dc2626")
        self.lbl_fsp_val = fila_card(card_ded, "Fondo de Solidaridad Pensional (1%)", f"- $ {fsp_e:,} COP" if fsp_e > 0 else "$ 0 COP", color="#dc2626" if fsp_e > 0 else "#6b7280")
        tk.Frame(card_ded, bg="white", height=4).pack()

        # 3. COSTO TOTAL EMPLEADOR (UPC)
        card_costo, self.lbl_sub_costo = crear_tarjeta(
            "COSTO TOTAL EMPLEADOR (UPC)", f"$ {costo_upc:,.0f} COP", color_titulo="#d97706")
        self.lbl_costo_asig = fila_card(card_costo, "Asignación Básica", f"$ {bruto:,.0f} COP", bold=True, color="#1d4ed8")
        self.lbl_ap_salud = fila_card(card_costo, "Salud Patronal (8.5%)", f"$ {ap['salud']:,} COP", color="#4b5563")
        self.lbl_ap_pension = fila_card(card_costo, "Pensión Patronal (12%)", f"$ {ap['pension']:,} COP", color="#4b5563")
        self.lbl_ap_arl = fila_card(card_costo, "Aporte Riesgos Laborales (ARL)", f"$ {ap['arl']:,} COP", color="#4b5563")
        self.lbl_ap_caja = fila_card(card_costo, "Caja de Compensación Familiar (4%)", f"$ {ap['caja']:,} COP", color="#4b5563")
        tk.Frame(card_costo, bg="#f3f4f6", height=1).pack(fill="x", padx=14, pady=4)
        self.lbl_costo_total_upc = fila_card(card_costo, "TOTAL COSTO UPC", f"$ {costo_upc:,.0f} COP", bold=True, color="#1d4ed8")
        tk.Frame(card_costo, bg="white", height=4).pack()

        # 4. BANNER NETO A PAGAR
        neto_box = tk.Frame(inner, bg="white", highlightbackground="#10b981", highlightthickness=2)
        neto_box.pack(fill="x", padx=16, pady=(4, 14))

        neto_top = tk.Frame(neto_box, bg="white")
        neto_top.pack(fill="x", padx=14, pady=(10, 3))
        tk.Label(neto_top, text="NETO A PAGAR:", font=("Segoe UI", 11, "bold"),
                 bg="white", fg="#111827").pack(side="left")
        self.lbl_neto_val = tk.Label(neto_top, text=f"$ {neto:,.0f} COP",
                                     font=("Segoe UI", 13, "bold"), bg="white", fg="#059669")
        self.lbl_neto_val.pack(side="right")

        self.lbl_neto_resumen = tk.Label(
            neto_box,
            text=f"Total Devengado: $ {bruto:,.0f} COP  ·  Total Deducciones: -$ {total_ded:,.0f} COP",
            font=("Segoe UI", 8), bg="white", fg="#6b7280"
        )
        self.lbl_neto_resumen.pack(anchor="w", padx=14, pady=(0, 10))

        self._val = {
            "bruto": bruto, "total_ded": total_ded, "salud_e": salud_e, "pension_e": pension_e, "fsp_e": fsp_e,
            "costo_upc": costo_upc, "ap_salud": ap["salud"], "ap_pension": ap["pension"],
            "ap_arl": ap["arl"], "ap_caja": ap["caja"], "neto": neto,
        }

        ttk.Button(inner, text="Cerrar", command=self.destroy).pack(pady=(0, 16))
        self.transient(parent)
        self.grab_set()

    def _alternar_periodo(self):
        """Alterna entre vista mensual y anual."""
        if not hasattr(self, "_val"):
            return
        v = self._val
        if self.periodo == "mensual":
            self.periodo = "anual"
            f = 12
            self.btn_periodo.configure(text="Ver mensual")
            self.lbl_periodo_fechas.configure(text="Período Liquidado: Año Vigente 2026 (Consolidado 12 Meses)")
        else:
            self.periodo = "mensual"
            f = 1
            self.btn_periodo.configure(text="Ver anual")
            self.lbl_periodo_fechas.configure(text="Período Liquidado: Marzo 2026 · 01/03/2026 - 31/03/2026")

        self.lbl_sub_dev.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_asig_val.configure(text=f"+ $ {v['bruto']*f:,.0f} COP")
        self.lbl_sub_ded.configure(text=f"$ {v['total_ded']*f:,.0f} COP")
        self.lbl_ibc_ded.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_salud_val.configure(text=f"- $ {v['salud_e']*f:,} COP")
        self.lbl_pension_val.configure(text=f"- $ {v['pension_e']*f:,} COP")
        self.lbl_fsp_val.configure(text=f"- $ {v['fsp_e']*f:,} COP" if v['fsp_e'] > 0 else "$ 0 COP")
        self.lbl_sub_costo.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")
        self.lbl_costo_asig.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_ap_salud.configure(text=f"$ {v['ap_salud']*f:,} COP")
        self.lbl_ap_pension.configure(text=f"$ {v['ap_pension']*f:,} COP")
        self.lbl_ap_arl.configure(text=f"$ {v['ap_arl']*f:,} COP")
        self.lbl_ap_caja.configure(text=f"$ {v['ap_caja']*f:,} COP")
        self.lbl_costo_total_upc.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")
        self.lbl_neto_val.configure(text=f"$ {v['neto']*f:,.0f} COP")
        self.lbl_neto_resumen.configure(text=f"Total Devengado: $ {v['bruto']*f:,.0f} COP  ·  Total Deducciones: -$ {v['total_ded']*f:,.0f} COP")


if __name__ == "__main__":
    app = PitaApp()
    app.mainloop()
