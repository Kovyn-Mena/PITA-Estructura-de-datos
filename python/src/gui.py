"""PITA - Interfaz grafica (bono)
Universidad Popular del Cesar

Reutiliza integramente la logica ya probada en entidades.py, persistencia.py,
gestion.py (funciones de busqueda) y nomina.py. Esta capa SOLO agrega la
presentacion visual; ninguna regla de negocio se reescribe aqui.

Ejecutar con: python3 gui.py (desde python/src)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os

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
    calcular_salario_bruto, calcular_descuento_salud, calcular_descuento_pension,
    calcular_salario_neto, calcular_prima_servicios, calcular_cesantias,
    total_puntos, puntos_por_categoria, factor_proporcionalidad, VALOR_PUNTO,
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
    "danger": "#c0392b",
    "danger_dark": "#922b21",
    "card": "#ffffff",
    "muted": "#6b7280",
    "warn_bg": "#fdecea",
    "warn_fg": "#922b21",
    "ok_bg": "#e8f5e9",
    "ok_fg": "#256029",
}
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUB = ("Segoe UI", 10)


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
        self.title("PITA — Universidad Popular del Cesar")
        self.geometry("1150x700")
        self.minsize(950, 600)
        self.configure(bg=C["bg"])

        self.facultades = []
        self.programas = []
        self.cursos = []
        self.estudiantes = []
        self.profesores = []
        self.administrativos = []
        self.notebook = None
        self.pantalla_inicio = None

        self._configurar_estilo()
        self._construir_header()
        # Los datos se cargan antes de mostrar el menú para que la pantalla
        # de entrada pueda presentar un resumen real del sistema.
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
        style.configure("TNotebook.Tab", padding=(18, 10), font=FONT_BOLD, background="#dbe4ee")
        style.map("TNotebook.Tab",
                  background=[("selected", C["primary"])],
                  foreground=[("selected", "white")])

        style.configure("Treeview", rowheight=27, font=FONT, background="white",
                        fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=FONT_BOLD, background=C["primary"],
                        foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[("active", C["primary_dark"])])
        style.map("Treeview", background=[("selected", "#cfe0f0")], foreground=[("selected", "black")])

        style.configure("TButton", padding=7, font=FONT)
        style.configure("Accent.TButton", background=C["primary"], foreground="white", font=FONT_BOLD, padding=8)
        style.map("Accent.TButton", background=[("active", C["primary_dark"])])
        style.configure("Danger.TButton", background=C["danger"], foreground="white", font=FONT_BOLD, padding=8)
        style.map("Danger.TButton", background=[("active", C["danger_dark"])])

    def _construir_header(self):
        # Un poco más de altura evita que los botones superiores queden
        # recortados en Windows y deja respirar mejor al encabezado.
        header = tk.Frame(self, bg=C["primary"], height=82)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=C["primary"])
        left.pack(side="left", padx=20, pady=10)
        tk.Label(left, text="PITA", font=FONT_TITLE, bg=C["primary"], fg="white").pack(anchor="w")
        tk.Label(left, text="Programa Integrado de Transacciones Académicas — UPC",
                 font=FONT_SUB, bg=C["primary"], fg="#c9d9e8").pack(anchor="w")

        self.header_actions = tk.Frame(header, bg=C["primary"])
        # Estos botones solo aparecen al entrar al sistema; así la portada
        # queda limpia y el menú no aparece de golpe al iniciar.
        ttk.Button(self.header_actions, text="Recargar datos", width=15,
                   command=self._recargar_datos).pack(side="left", padx=4, pady=18)
        ttk.Button(self.header_actions, text="Guardar datos", width=15,
                   style="Accent.TButton", command=self._guardar_datos).pack(side="left", padx=4, pady=18)

        self.status_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.status_var, font=("Segoe UI", 9, "italic"),
                 bg=C["bg"], fg=C["muted"], anchor="w").pack(fill="x", padx=16, pady=(6, 0))

    def _construir_pantalla_inicio(self):
        """Pantalla de bienvenida que aparece antes de las pestañas de gestión."""
        self.pantalla_inicio = tk.Frame(self, bg=C["bg"])
        self.pantalla_inicio.pack(fill="both", expand=True, padx=18, pady=18)

        card = tk.Frame(self.pantalla_inicio, bg=C["card"],
                        highlightbackground="#d8dde3", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78, relheight=0.78)

        tk.Label(card, text="Bienvenido a PITA", font=("Segoe UI", 24, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(pady=(28, 5))
        tk.Label(card, text="Programa Integrado de Transacciones Académicas",
                 font=("Segoe UI", 12), bg=C["card"], fg=C["muted"]).pack()
        tk.Label(card, text="Universidad Popular del Cesar", font=("Segoe UI", 11, "bold"),
                 bg=C["card"], fg="#374151").pack(pady=(3, 18))

        # Tarjetas en 2 filas de 3: se leen mejor y no se comprimen cuando
        # la ventana se ejecuta en resoluciones pequeñas de Windows.
        stats = tk.Frame(card, bg="#f4f7fa", highlightbackground="#e1e6eb", highlightthickness=1)
        stats.pack(fill="x", padx=42, pady=(0, 20))
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
            celda.grid(row=fila, column=columna, padx=10, pady=8, sticky="nsew")
            tk.Label(celda, text=str(cantidad), font=("Segoe UI", 17, "bold"),
                     bg="#f4f7fa", fg=C["primary"]).pack()
            tk.Label(celda, text=nombre, font=("Segoe UI", 9),
                     bg="#f4f7fa", fg=C["muted"]).pack()
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)

        tk.Label(card, text="Selecciona una opción para continuar.",
                 font=FONT, bg=C["card"], fg="#4b5563").pack(pady=(0, 12))

        # Se usan botones tk.Button con dimensiones explícitas para evitar el
        # problema de ttk en algunas configuraciones de Windows donde "Salir"
        # terminaba renderizándose como puntos o quedaba comprimido.
        acciones = tk.Frame(card, bg=C["card"])
        acciones.pack(pady=(0, 4))

        tk.Button(acciones, text="Entrar al sistema", command=self._entrar_sistema,
                  font=("Segoe UI", 10, "bold"), width=24, height=1,
                  bg=C["primary"], fg="white", activebackground=C["primary_dark"],
                  activeforeground="white", relief="flat", cursor="hand2",
                  padx=8, pady=7).pack(pady=(0, 8))

        tk.Button(acciones, text="Salir", command=self._salir,
                  font=("Segoe UI", 10, "bold"), width=24, height=1,
                  bg="#e5e7eb", fg="#374151", activebackground="#d1d5db",
                  activeforeground="#111827", relief="flat", cursor="hand2",
                  padx=8, pady=7).pack()

        self._set_status(
            f"Datos cargados: {len(self.facultades)} facultades, {len(self.programas)} programas, "
            f"{len(self.cursos)} cursos, {len(self.estudiantes)} estudiantes, "
            f"{len(self.profesores)} profesores, {len(self.administrativos)} administrativos."
        )

    def _entrar_sistema(self):
        """Oculta la bienvenida y muestra el menú completo de gestión."""
        if self.pantalla_inicio is not None:
            self.pantalla_inicio.destroy()
            self.pantalla_inicio = None
        self.header_actions.pack(side="right", padx=16)
        self._construir_notebook()
        self._set_status(
            f"Sistema listo: {len(self.facultades)} facultades, {len(self.programas)} programas, "
            f"{len(self.cursos)} cursos, {len(self.estudiantes)} estudiantes, "
            f"{len(self.profesores)} profesores, {len(self.administrativos)} administrativos."
        )

    def _set_status(self, texto):
        self.status_var.set(texto)

    # ---------------- Notebook (pestañas) ----------------

    def _construir_notebook(self):
        if self.notebook is not None:
            return
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=12)

        self._tab_facultades()
        self._tab_programas()
        self._tab_cursos()
        self._tab_estudiantes()
        self._tab_profesores()
        self._tab_administrativos()

    def _crear_shell_tab(self, nombre_pestaña, columnas):
        """Crea el esqueleto comun de una pestaña: card + treeview + scrollbar."""
        outer = tk.Frame(self.notebook, bg=C["bg"])
        self.notebook.add(outer, text=nombre_pestaña)

        card = tk.Frame(outer, bg=C["card"], highlightbackground="#d8dde3", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        tree_frame = tk.Frame(card, bg=C["card"])
        tree_frame.pack(fill="both", expand=True, padx=12, pady=(12, 6))

        tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="w")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = tk.Frame(card, bg=C["card"])
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))

        return outer, tree, btn_frame

    def _fila_activo(self, activo):
        return "Activo" if activo else "Inactivo"

    # ---------------- FACULTADES ----------------

    def _tab_facultades(self):
        _, self.tree_facultades, btns = self._crear_shell_tab(
            "Facultades", ["Código", "Nombre", "Decano", "Estado"])

        ttk.Button(btns, text="Nueva", style="Accent.TButton",
                   command=self._facultad_nueva).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._facultad_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._facultad_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._facultad_eliminar).pack(side="left", padx=4)

        self._refrescar_facultades()

    def _refrescar_facultades(self):
        self.tree_facultades.delete(*self.tree_facultades.get_children())
        for f in self.facultades:
            self.tree_facultades.insert("", "end", iid=f.codigo,
                values=(f.codigo, f.nombre, f.decano, self._fila_activo(f.activo)))

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
        _, self.tree_programas, btns = self._crear_shell_tab(
            "Programas", ["Código", "Nombre", "Nivel", "Facultad", "Estado"])

        ttk.Button(btns, text="Nuevo", style="Accent.TButton",
                   command=self._programa_nuevo).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._programa_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._programa_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._programa_eliminar).pack(side="left", padx=4)

        self._refrescar_programas()

    def _refrescar_programas(self):
        self.tree_programas.delete(*self.tree_programas.get_children())
        for p in self.programas:
            self.tree_programas.insert("", "end", iid=p.codigo,
                values=(p.codigo, p.nombre, p.nivel, p.codigo_facultad, self._fila_activo(p.activo)))

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
        _, self.tree_cursos, btns = self._crear_shell_tab(
            "Cursos", ["Código", "Nombre", "Créditos", "Programa", "Profesor", "Estado"])

        ttk.Button(btns, text="Nuevo", style="Accent.TButton",
                   command=self._curso_nuevo).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._curso_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._curso_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._curso_eliminar).pack(side="left", padx=4)

        self._refrescar_cursos()

    def _refrescar_cursos(self):
        self.tree_cursos.delete(*self.tree_cursos.get_children())
        for c in self.cursos:
            prof = c.codigo_profesor if c.codigo_profesor else "(sin asignar)"
            self.tree_cursos.insert("", "end", iid=c.codigo,
                values=(c.codigo, c.nombre, c.creditos, c.codigo_programa, prof, self._fila_activo(c.activo)))

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

    # ---------------- ESTUDIANTES ----------------

    def _tab_estudiantes(self):
        _, self.tree_estudiantes, btns = self._crear_shell_tab(
            "Estudiantes", ["ID", "Nombre", "Programa", "Estado", "Promedio", "EBRA"])

        ttk.Button(btns, text="Nuevo", style="Accent.TButton",
                   command=self._estudiante_nuevo).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._estudiante_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Matricular curso", command=self._estudiante_matricular).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancelar curso", command=self._estudiante_cancelar_curso).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._estudiante_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._estudiante_eliminar).pack(side="left", padx=4)

        self._refrescar_estudiantes()

    def _refrescar_estudiantes(self):
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        for e in self.estudiantes:
            promedio = e.calcular_promedio()
            ebra = "⚠ EN RIESGO" if e.esta_en_riesgo_ebra() else "—"
            self.tree_estudiantes.insert("", "end", iid=e.identificacion,
                values=(e.identificacion, e.nombre_completo, e.codigo_programa, e.estado,
                        f"{promedio:.2f}", ebra))
        # Colorear filas en riesgo EBRA
        for e in self.estudiantes:
            if e.esta_en_riesgo_ebra():
                self.tree_estudiantes.tag_configure("riesgo", foreground=C["danger"])
                self.tree_estudiantes.item(e.identificacion, tags=("riesgo",))

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
        if not self.cursos:
            messagebox.showwarning("Sin cursos", "No hay cursos registrados.")
            return
        opciones_curso = [c.codigo for c in self.cursos if c.activo]
        if not opciones_curso:
            messagebox.showwarning("Sin cursos activos", "No hay cursos activos disponibles.")
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

    # ---------------- PROFESORES ----------------

    def _tab_profesores(self):
        _, self.tree_profesores, btns = self._crear_shell_tab(
            "Profesores", ["ID", "Nombre", "Vinculación", "Dedicación", "Categoría", "Programa", "Estado"])

        ttk.Button(btns, text="Nuevo", style="Accent.TButton",
                   command=self._profesor_nuevo).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._profesor_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Ver nómina", command=self._profesor_ver_nomina).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._profesor_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._profesor_eliminar).pack(side="left", padx=4)

        self._refrescar_profesores()

    def _refrescar_profesores(self):
        self.tree_profesores.delete(*self.tree_profesores.get_children())
        for p in self.profesores:
            self.tree_profesores.insert("", "end", iid=p.identificacion,
                values=(p.identificacion, p.nombre_completo, p.tipo_vinculacion, p.dedicacion,
                        p.categoria_escalafon, p.codigo_programa, self._fila_activo(p.activo)))

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
            {"label": "Años de experiencia", "key": "anios_experiencia", "tipo": "entry",
             "valor": str(p.anios_experiencia)},
            {"label": "Puntos por títulos", "key": "puntos_titulos", "tipo": "entry",
             "valor": str(p.puntos_titulos)},
            {"label": "Puntos por productividad", "key": "puntos_productividad", "tipo": "entry",
             "valor": str(p.puntos_productividad)},
        ]
        def guardar(v):
            p.nombre_completo = v["nombre"].strip() or p.nombre_completo
            try:
                p.anios_experiencia = int(v["anios_experiencia"])
                p.puntos_titulos = int(v["puntos_titulos"])
                p.puntos_productividad = int(v["puntos_productividad"])
            except ValueError:
                return "Los campos numéricos deben ser números enteros."
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
        _, self.tree_admins, btns = self._crear_shell_tab(
            "Administrativos", ["ID", "Nombre", "Cargo", "Contratación", "Facultad", "Salario", "Estado"])

        ttk.Button(btns, text="Nuevo", style="Accent.TButton",
                   command=self._admin_nuevo).pack(side="left", padx=4)
        ttk.Button(btns, text="Editar", command=self._admin_editar).pack(side="left", padx=4)
        ttk.Button(btns, text="Activar/Desactivar", command=self._admin_toggle).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton",
                   command=self._admin_eliminar).pack(side="left", padx=4)

        self._refrescar_administrativos()

    def _refrescar_administrativos(self):
        self.tree_admins.delete(*self.tree_admins.get_children())
        for a in self.administrativos:
            facultad = a.codigo_facultad if a.codigo_facultad else "(nivel central)"
            self.tree_admins.insert("", "end", iid=a.identificacion,
                values=(a.identificacion, a.nombre_completo, a.cargo, a.tipo_contratacion,
                        facultad, f"${a.salario_base:,.0f}", self._fila_activo(a.activo)))

    def _admin_seleccionado(self):
        sel = self.tree_admins.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un administrativo de la lista.")
            return None
        return buscar_administrativo(self.administrativos, sel[0])

    def _admin_nuevo(self):
        opciones_facultad = [""] + [f.codigo for f in self.facultades]
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry"},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry"},
            {"label": "Cargo", "key": "cargo", "tipo": "entry"},
            {"label": "Categoría", "key": "categoria", "tipo": "entry", "valor": "Nivel 1"},
            {"label": "Tipo de contratación", "key": "tipo_contratacion", "tipo": "combo",
             "opciones": ["Planta", "Provisional", "Contrato"]},
            {"label": "Salario base", "key": "salario_base", "tipo": "entry", "valor": "0"},
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
        campos = [
            {"label": "Identificación", "key": "identificacion", "tipo": "entry",
             "valor": a.identificacion, "readonly": True},
            {"label": "Nombre completo", "key": "nombre", "tipo": "entry", "valor": a.nombre_completo},
            {"label": "Cargo", "key": "cargo", "tipo": "entry", "valor": a.cargo},
            {"label": "Salario base", "key": "salario_base", "tipo": "entry", "valor": str(a.salario_base)},
        ]
        def guardar(v):
            a.nombre_completo = v["nombre"].strip() or a.nombre_completo
            a.cargo = v["cargo"].strip() or a.cargo
            try:
                a.salario_base = float(v["salario_base"])
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

    # ---------------- Persistencia (cargar / guardar / recargar) ----------------

    def _cargar_datos(self, silencioso=False):
        self.facultades = cargar_facultades(RUTA_FACULTADES)
        self.programas = cargar_programas(RUTA_PROGRAMAS)
        self.cursos = cargar_cursos(RUTA_CURSOS)
        self.estudiantes = cargar_estudiantes(RUTA_ESTUDIANTES, RUTA_MATRICULAS)
        self.profesores = cargar_profesores(RUTA_PROFESORES)
        self.administrativos = cargar_administrativos(RUTA_ADMINISTRATIVOS)
        for refrescar in (self._refrescar_facultades, self._refrescar_programas, self._refrescar_cursos,
                          self._refrescar_estudiantes, self._refrescar_profesores, self._refrescar_administrativos):
            try:
                refrescar()
            except AttributeError:
                pass  # pestaña aun no construida en la carga inicial
        msg = (f"Datos cargados: {len(self.facultades)} facultades, {len(self.programas)} programas, "
               f"{len(self.cursos)} cursos, {len(self.estudiantes)} estudiantes, "
               f"{len(self.profesores)} profesores, {len(self.administrativos)} administrativos.")
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
        self._set_status("Datos guardados correctamente.")

    def _salir(self):
        if messagebox.askyesno("Guardar antes de salir", "¿Deseas guardar los datos antes de salir?"):
            self._guardar_datos()
        self.destroy()


class VentanaNomina(tk.Toplevel):
    """Muestra el desglose de nomina de un profesor, reutilizando nomina.py."""
    def __init__(self, parent, profesor):
        super().__init__(parent)
        self.title(f"Nómina — {profesor.nombre_completo}")
        self.configure(bg=C["card"])
        self.resizable(False, False)
        self.geometry("420x480")

        tk.Label(self, text=profesor.nombre_completo, font=("Segoe UI", 14, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=18, pady=(16, 2))
        tk.Label(self, text=f"{profesor.tipo_vinculacion} · {profesor.dedicacion}",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=18, pady=(0, 12))

        filas = tk.Frame(self, bg=C["card"])
        filas.pack(fill="x", padx=18)

        def fila(label, valor, bold=False, color=None):
            f = tk.Frame(filas, bg=C["card"])
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label, font=FONT_BOLD if bold else FONT, bg=C["card"],
                     fg=color or "#1a1a1a").pack(side="left")
            tk.Label(f, text=valor, font=FONT_BOLD if bold else FONT, bg=C["card"],
                     fg=color or "#1a1a1a").pack(side="right")

        puntos_cat = puntos_por_categoria(profesor.categoria_escalafon)
        puntos_total = total_puntos(profesor)
        factor = factor_proporcionalidad(profesor)
        bruto = calcular_salario_bruto(profesor)
        salud = calcular_descuento_salud(bruto)
        pension = calcular_descuento_pension(bruto)
        neto = calcular_salario_neto(profesor)
        prima = calcular_prima_servicios(bruto)
        cesantias = calcular_cesantias(bruto)

        fila("Categoría escalafón:", f"{profesor.categoria_escalafon or '—'} ({puntos_cat} pts)")
        fila("Puntos por títulos:", str(profesor.puntos_titulos))
        fila("Puntos por productividad:", str(profesor.puntos_productividad))
        fila("Total de puntos:", str(puntos_total), bold=True)
        fila("Valor del punto:", f"${VALOR_PUNTO:,.2f}")
        fila("Factor proporcional:", f"{factor:.2f}")

        tk.Frame(self, bg="#d8dde3", height=1).pack(fill="x", padx=18, pady=10)

        filas2 = tk.Frame(self, bg=C["card"])
        filas2.pack(fill="x", padx=18)

        def fila2(label, valor, bold=False, color=None):
            f = tk.Frame(filas2, bg=C["card"])
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label, font=FONT_BOLD if bold else FONT, bg=C["card"],
                     fg=color or "#1a1a1a").pack(side="left")
            tk.Label(f, text=valor, font=FONT_BOLD if bold else FONT, bg=C["card"],
                     fg=color or "#1a1a1a").pack(side="right")

        fila2("Salario bruto:", f"${bruto:,.2f}", bold=True)
        fila2("(-) Salud (4%):", f"${salud:,.2f}")
        fila2("(-) Pensión (4%):", f"${pension:,.2f}")

        neto_frame = tk.Frame(self, bg=C["ok_bg"] if neto > 0 else C["warn_bg"])
        neto_frame.pack(fill="x", padx=18, pady=12)
        tk.Label(neto_frame, text="SALARIO NETO", font=FONT_BOLD, bg=neto_frame["bg"],
                 fg=C["ok_fg"] if neto > 0 else C["warn_fg"]).pack(side="left", padx=10, pady=8)
        tk.Label(neto_frame, text=f"${neto:,.2f}", font=("Segoe UI", 13, "bold"), bg=neto_frame["bg"],
                 fg=C["ok_fg"] if neto > 0 else C["warn_fg"]).pack(side="right", padx=10, pady=8)

        if profesor.ad_honorem:
            tk.Label(self, text="Vinculación ad-honorem: sin remuneración por normativa.",
                     font=("Segoe UI", 9, "italic"), bg=C["card"], fg=C["muted"]).pack(padx=18)

        filas3 = tk.Frame(self, bg=C["card"])
        filas3.pack(fill="x", padx=18, pady=(6, 16))
        tk.Label(filas3, text=f"Prima (informativo): ${prima:,.2f}", font=("Segoe UI", 9),
                 bg=C["card"], fg=C["muted"]).pack(anchor="w")
        tk.Label(filas3, text=f"Cesantías (informativo): ${cesantias:,.2f}", font=("Segoe UI", 9),
                 bg=C["card"], fg=C["muted"]).pack(anchor="w")

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 14))
        self.transient(parent)
        self.grab_set()


if __name__ == "__main__":
    app = PitaApp()
    app.mainloop()
