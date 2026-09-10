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
        self.icons = {}          # referencias a PhotoImage (evita que Tkinter las borre)
        self.secciones = {}      # id_seccion -> Frame de contenido
        self.dock_botones = {}   # id_seccion -> widget boton (para resaltar el activo)
        self.seccion_actual = None
        self.titulo_vars = {}    # id_seccion -> StringVar (titulo dinamico con filtros)
        self.refrescos_seccion = {}  # id_seccion -> funcion a llamar al entrar a esa seccion

        # Navegación jerárquica Facultad → Programa → Curso.
        # None significa que se muestran todos los registros.
        self.filtro_facultad_programas = None
        self.filtro_programa_cursos = None
        self.filtro_programa_estudiantes = None
        self.filtro_curso_estudiantes = None

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

        # Solo se fija el ANCHO (relwidth); el ALTO se deja que lo determine
        # el propio contenido empacado adentro (comportamiento por defecto
        # de un Frame). Antes se fijaba tambien relheight=0.78, y en
        # ventanas mas bajas (por ejemplo el tamano minimo de la ventana)
        # el contenido no alcanzaba a caber en esa altura fija: el boton
        # "Entrar al sistema" quedaba aplastado contra el borde inferior de
        # la tarjeta y el boton "Salir" quedaba completamente recortado
        # fuera de ella, aunque la ventana en si tuviera espacio de sobra.
        card = tk.Frame(self.pantalla_inicio, bg=C["card"],
                        highlightbackground="#d8dde3", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78)

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
        self._construir_dock()
        self._set_status(
            f"Sistema listo: {len(self.facultades)} facultades, {len(self.programas)} programas, "
            f"{len(self.cursos)} cursos, {len(self.estudiantes)} estudiantes, "
            f"{len(self.profesores)} profesores, {len(self.administrativos)} administrativos."
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
        self.icons[nombre_archivo] = img  # evita que el recolector de basura la borre
        return img

    def _construir_dock(self):
        if self.secciones:
            return  # ya construido (por si _entrar_sistema se llama dos veces)

        # El dock se empaqueta PRIMERO en "bottom" para reservar su espacio;
        # el area de contenido se empaqueta despues y ocupa el resto.
        # OJO: antes se forzaba una altura fija de 84px (con
        # pack_propagate(False)), pero un icono de 64px mas su etiqueta de
        # texto abajo mas el relleno (pady) necesitan mas que eso: el
        # texto de cada boton quedaba cortado a la mitad. Se deja que el
        # propio contenido (iconos + etiquetas) determine la altura del
        # dock, que es el comportamiento por defecto de un Frame.
        dock = tk.Frame(self, bg="#1b2a3a")
        dock.pack(side="bottom", fill="x")

        izquierda = tk.Frame(dock, bg="#1b2a3a")
        izquierda.pack(side="left", fill="y", padx=(10, 0))

        for sid, etiqueta, archivo in self.SECCIONES:
            icono = self._cargar_icono(archivo)
            btn = tk.Button(
                izquierda, image=icono, text=etiqueta, compound="top",
                font=("Segoe UI", 8, "bold"), fg="#c9d9e8", bg="#1b2a3a",
                activebackground="#28405c", activeforeground="white",
                relief="flat", bd=0, cursor="hand2", padx=10, pady=6,
                command=lambda s=sid: self._mostrar_seccion(s),
            )
            btn.pack(side="left", padx=3, pady=6)
            self.dock_botones[sid] = btn

        # Salir separado a la derecha, con su propio color de acento rojo,
        # visible SIEMPRE sin importar en que seccion este el usuario.
        icono_salir = self._cargar_icono("salir.png")
        btn_salir = tk.Button(
            dock, image=icono_salir, text="Salir", compound="top",
            font=("Segoe UI", 8, "bold"), fg="#f5b7b1", bg="#1b2a3a",
            activebackground="#922b21", activeforeground="white",
            relief="flat", bd=0, cursor="hand2", padx=14, pady=6,
            command=self._salir,
        )
        btn_salir.pack(side="right", padx=16, pady=6)

        # Area de contenido: ocupa todo el espacio restante arriba del dock.
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
        self.secciones[sid].pack(fill="both", expand=True, padx=16, pady=14)
        self.dock_botones[sid].configure(bg="#28405c", fg="white")
        self.seccion_actual = sid
        if sid in self.refrescos_seccion:
            self.refrescos_seccion[sid]()

    def _construir_seccion_panel(self, frame):
        """Panel de inicio: resumen general del sistema (tipo dashboard)."""
        tk.Label(frame, text="Panel de control", font=("Segoe UI", 16, "bold"),
                 bg=C["bg"], fg=C["primary"]).pack(anchor="w", pady=(0, 12))

        tarjetas = tk.Frame(frame, bg=C["bg"])
        tarjetas.pack(fill="x")
        datos = [
            ("Facultades", len(self.facultades)), ("Programas", len(self.programas)),
            ("Cursos", len(self.cursos)), ("Estudiantes", len(self.estudiantes)),
            ("Profesores", len(self.profesores)), ("Administrativos", len(self.administrativos)),
        ]
        for i, (etiqueta, valor) in enumerate(datos):
            card = tk.Frame(tarjetas, bg=C["card"], highlightbackground="#d8dde3", highlightthickness=1)
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="ew")
            tarjetas.grid_columnconfigure(i % 3, weight=1)
            tk.Label(card, text=str(valor), font=("Segoe UI", 22, "bold"),
                     bg=C["card"], fg=C["primary"]).pack(pady=(14, 0))
            tk.Label(card, text=etiqueta, font=FONT, bg=C["card"], fg=C["muted"]).pack(pady=(0, 14))

        tk.Label(frame, text="Usa el menú de abajo para navegar entre secciones.",
                 font=("Segoe UI", 9, "italic"), bg=C["bg"], fg=C["muted"]).pack(anchor="w", pady=(16, 0))

    def _construir_placeholder(self, frame, sid):
        """Marcador temporal; se reemplaza por el contenido real en el
        siguiente bloque de trabajo (migracion de cada seccion al dock)."""
        tk.Label(frame, text="Sección en construcción",
                 font=("Segoe UI", 14, "bold"), bg=C["bg"], fg=C["muted"]).pack(pady=(60, 4))
        tk.Label(frame, text=f"(\"{sid}\" se conecta en el siguiente bloque)",
                 font=FONT, bg=C["bg"], fg=C["muted"]).pack()

    # ---------------- Contenido de cada sección (dentro del dock) ----------------

    def _crear_shell_tab(self, sid, nombre_seccion, columnas):
        """Crea el contenido comun de una seccion (titulo + card + treeview
        + scrollbar) DENTRO del frame que el dock ya creo para esa seccion."""
        outer = self.secciones[sid]

        titulo_var = tk.StringVar(value=nombre_seccion)
        self.titulo_vars[sid] = titulo_var
        tk.Label(outer, textvariable=titulo_var, font=("Segoe UI", 15, "bold"),
                 bg=C["bg"], fg=C["primary"]).pack(anchor="w", pady=(0, 8))

        card = tk.Frame(outer, bg=C["card"], highlightbackground="#d8dde3", highlightthickness=1)
        card.pack(fill="both", expand=True)

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
        btn_frame.pack(fill="x", padx=12, pady=(4, 12))

        return tree, btn_frame

    def _fila_activo(self, activo):
        return "Activo" if activo else "Inactivo"

    # Helper: crea un tk.Button bien estilizado (sin los problemas de recorte
    # que tiene ttk.Button en Windows al redimensionar la ventana).
    # estilo: "normal" | "accent" | "danger" | "nav" (para botones ← Volver)
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
            padx=10, pady=5,
        )
        b.pack(side=lado, padx=4, pady=2)
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

        self.tree_facultades.bind("<Double-1>", self._doble_click_facultad)
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
        self.tree_programas, btns = self._crear_shell_tab(
            "programas", "Programas", ["Código", "Nombre", "Nivel", "Facultad", "Estado"])

        self._btn(btns, "Nuevo",              self._programa_nuevo,              estilo="accent")
        self._btn(btns, "Editar",             self._programa_editar)
        self._btn(btns, "Activar/Desactivar", self._programa_toggle)
        self._btn(btns, "Eliminar",           self._programa_eliminar,           estilo="danger")
        self._btn(btns, "Ver cursos",         self._ir_a_cursos_filtrados)
        self._btn(btns, "Ver estudiantes",    self._ir_a_estudiantes_programa)
        self._btn(btns, "Mostrar todos",      self._mostrar_todos_programas)
        self._btn(btns, "← Facultades",      self._volver_a_facultades,         estilo="nav", lado="right")

        self.tree_programas.bind("<Double-1>", self._doble_click_programa)
        self._refrescar_programas()

    def _refrescar_programas(self):
        self.tree_programas.delete(*self.tree_programas.get_children())
        for p in self.programas:
            if self.filtro_facultad_programas and p.codigo_facultad != self.filtro_facultad_programas:
                continue
            self.tree_programas.insert("", "end", iid=p.codigo,
                values=(p.codigo, p.nombre, p.nivel, p.codigo_facultad, self._fila_activo(p.activo)))
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
            "cursos", "Cursos", ["Código", "Nombre", "Créditos", "Programa", "Profesor", "Estado"])

        self._btn(btns, "Nuevo",              self._curso_nuevo,              estilo="accent")
        self._btn(btns, "Editar",             self._curso_editar)
        self._btn(btns, "Activar/Desactivar", self._curso_toggle)
        self._btn(btns, "Eliminar",           self._curso_eliminar,           estilo="danger")
        self._btn(btns, "Ver detalle",        self._curso_ver_detalle)
        self._btn(btns, "Ver profesor",       self._curso_ver_profesor)
        self._btn(btns, "Ver estudiantes",    self._ir_a_estudiantes_curso)
        self._btn(btns, "Mostrar todos",      self._mostrar_todos_cursos)
        self._btn(btns, "← Programas",       self._volver_a_programas,       estilo="nav", lado="right")

        self.tree_cursos.bind("<Double-1>", self._doble_click_curso)
        self._refrescar_cursos()

    def _refrescar_cursos(self):
        self.tree_cursos.delete(*self.tree_cursos.get_children())
        for c in self.cursos:
            if self.filtro_programa_cursos and c.codigo_programa != self.filtro_programa_cursos:
                continue
            prof = c.codigo_profesor if c.codigo_profesor else "(sin asignar)"
            self.tree_cursos.insert("", "end", iid=c.codigo,
                values=(c.codigo, c.nombre, c.creditos, c.codigo_programa, prof, self._fila_activo(c.activo)))
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
            "estudiantes", "Estudiantes", ["ID", "Nombre", "Programa", "Estado", "Promedio", "EBRA"])

        self._btn(btns, "Nuevo",              self._estudiante_nuevo,           estilo="accent")
        self._btn(btns, "Editar",             self._estudiante_editar)
        self._btn(btns, "Matricular curso",   self._estudiante_matricular)
        self._btn(btns, "Cancelar curso",     self._estudiante_cancelar_curso)
        self._btn(btns, "Ver ficha",          self._estudiante_ver_ficha)
        self._btn(btns, "Mostrar todos",      self._mostrar_todos_estudiantes)
        self._btn(btns, "Activar/Desactivar", self._estudiante_toggle)
        self._btn(btns, "Eliminar",           self._estudiante_eliminar,        estilo="danger")

        self.tree_estudiantes.bind("<Double-1>", self._doble_click_estudiante)
        self._refrescar_estudiantes()

    def _refrescar_estudiantes(self):
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        visibles = []
        for e in self.estudiantes:
            if self.filtro_programa_estudiantes and e.codigo_programa != self.filtro_programa_estudiantes:
                continue
            if self.filtro_curso_estudiantes and not any(
                    m["codigo_curso"] == self.filtro_curso_estudiantes for m in e.matriculas):
                continue
            visibles.append(e)
            promedio = e.calcular_promedio()
            ebra = "⚠ EN RIESGO" if e.esta_en_riesgo_ebra() else "—"
            self.tree_estudiantes.insert("", "end", iid=e.identificacion,
                values=(e.identificacion, e.nombre_completo, e.codigo_programa, e.estado,
                        f"{promedio:.2f}", ebra))
        self.tree_estudiantes.tag_configure("riesgo", foreground=C["danger"])
        for e in visibles:
            if e.esta_en_riesgo_ebra():
                self.tree_estudiantes.item(e.identificacion, tags=("riesgo",))
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
        # Filtro basico: solo cursos ACTIVOS del MISMO PROGRAMA del estudiante,
        # y que aun no tenga matriculados.
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
        self._btn(btns, "Activar/Desactivar", self._profesor_toggle)
        self._btn(btns, "Eliminar",           self._profesor_eliminar, estilo="danger")

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

        self._refrescar_administrativos()

    def _admin_ver_salario(self):
        a = self._admin_seleccionado()
        if not a:
            return
        VentanaSalarioAdmin(self, a)

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

    # ---------------- NÓMINA DOCENTE (solo consulta, sin CRUD) ----------------
    # Separada de "Profesores" a proposito: aqui NO se crea/edita/elimina
    # nada, solo se consulta el desglose de salario ya calculado.

    def _tab_nomina(self):
        self.tree_nomina, btns = self._crear_shell_tab(
            "nomina", "Nómina Docente", ["ID", "Nombre", "Vinculación", "Dedicación", "Programa"])

        self._btn(btns, "Ver nómina", self._nomina_ver_seleccionado, estilo="accent")
        tk.Label(btns, text="Solo consulta — para editar datos del profesor, usa la sección Profesores.",
                 font=("Segoe UI", 9, "italic"), bg=C["card"], fg=C["muted"]).pack(side="left", padx=12)

        self.tree_nomina.bind("<Double-1>", lambda e: self._nomina_ver_seleccionado())
        self.refrescos_seccion["nomina"] = self._refrescar_nomina
        self._refrescar_nomina()

    def _refrescar_nomina(self):
        self.tree_nomina.delete(*self.tree_nomina.get_children())
        for p in self.profesores:
            self.tree_nomina.insert("", "end", iid=p.identificacion,
                values=(p.identificacion, p.nombre_completo, p.tipo_vinculacion,
                        p.dedicacion, p.codigo_programa))

    def _nomina_ver_seleccionado(self):
        sel = self.tree_nomina.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un profesor de la lista.")
            return
        p = buscar_profesor(self.profesores, sel[0])
        if p:
            VentanaNomina(self, p)


class VentanaEstudiante(tk.Toplevel):
    """Ficha académica compacta, similar a la ventana de nómina."""
    def __init__(self, parent, estudiante):
        super().__init__(parent)
        self.title(f"Ficha estudiante — {estudiante.nombre_completo}")
        self.configure(bg=C["card"])
        self.geometry("600x500")
        self.minsize(540, 440)

        programa = buscar_programa(parent.programas, estudiante.codigo_programa)
        tk.Label(self, text=estudiante.nombre_completo, font=("Segoe UI", 14, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=18, pady=(16, 2))
        tk.Label(self, text=f"ID {estudiante.identificacion} · Programa: "
                            f"{programa.nombre if programa else estudiante.codigo_programa}",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=18, pady=(0, 10))

        promedio = estudiante.calcular_promedio()
        riesgo = estudiante.esta_en_riesgo_ebra()
        resumen = tk.Frame(self, bg=C["warn_bg"] if riesgo else C["ok_bg"])
        resumen.pack(fill="x", padx=18, pady=(0, 12))
        tk.Label(resumen, text=f"Estado: {estudiante.estado}", font=FONT_BOLD,
                 bg=resumen["bg"], fg=C["warn_fg"] if riesgo else C["ok_fg"]).pack(side="left", padx=10, pady=8)
        tk.Label(resumen, text=f"Promedio: {promedio:.2f}  ·  EBRA: {'EN RIESGO' if riesgo else 'Sin alerta'}",
                 font=FONT_BOLD, bg=resumen["bg"],
                 fg=C["warn_fg"] if riesgo else C["ok_fg"]).pack(side="right", padx=10, pady=8)

        tk.Label(self, text="Cursos matriculados", font=FONT_BOLD,
                 bg=C["card"], fg="#1a1a1a").pack(anchor="w", padx=18, pady=(2, 6))
        frame = tk.Frame(self, bg=C["card"])
        frame.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        tree = ttk.Treeview(frame, columns=("Código", "Curso", "Nota", "Profesor"), show="headings")
        for col, width in (("Código", 90), ("Curso", 220), ("Nota", 70), ("Profesor", 130)):
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
            tree.insert("", "end", values=(m["codigo_curso"], nombre, f"{m['nota']:.2f}", profesor))

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 14))
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
        tk.Label(self, text=profesor.nombre_completo, font=("Segoe UI", 14, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=18, pady=(16, 3))
        if curso:
            tk.Label(self, text=f"Asignado a: {curso.nombre} ({curso.codigo})", font=FONT,
                     bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=18, pady=(0, 10))

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
        cuerpo.pack(fill="x", padx=18, pady=4)
        for etiqueta, valor in datos:
            f = tk.Frame(cuerpo, bg=C["card"])
            f.pack(fill="x", pady=3)
            tk.Label(f, text=f"{etiqueta}:", font=FONT_BOLD, bg=C["card"]).pack(side="left")
            tk.Label(f, text=str(valor), font=FONT, bg=C["card"]).pack(side="right")

        acciones = tk.Frame(self, bg=C["card"])
        acciones.pack(pady=14)
        ttk.Button(acciones, text="Ver nómina", command=lambda: VentanaNomina(parent, profesor)).pack(side="left", padx=5)
        ttk.Button(acciones, text="Cerrar", command=self.destroy).pack(side="left", padx=5)
        self.transient(parent)
        self.grab_set()


class VentanaCursoDetalle(tk.Toplevel):
    def __init__(self, parent, curso):
        super().__init__(parent)
        self.title(f"Curso — {curso.nombre}")
        self.configure(bg=C["card"])
        self.geometry("650x470")
        self.minsize(580, 420)

        programa = buscar_programa(parent.programas, curso.codigo_programa)
        profesor = buscar_profesor(parent.profesores, curso.codigo_profesor) if curso.codigo_profesor else None
        matriculados = [e for e in parent.estudiantes
                        if any(m["codigo_curso"] == curso.codigo for m in e.matriculas)]

        tk.Label(self, text=curso.nombre, font=("Segoe UI", 14, "bold"),
                 bg=C["card"], fg=C["primary"]).pack(anchor="w", padx=18, pady=(16, 2))
        tk.Label(self, text=f"{curso.codigo} · {curso.creditos} créditos · "
                            f"{programa.nombre if programa else curso.codigo_programa}",
                 font=FONT, bg=C["card"], fg=C["muted"]).pack(anchor="w", padx=18, pady=(0, 10))

        profbox = tk.Frame(self, bg="#f4f7fa", highlightbackground="#d8dde3", highlightthickness=1)
        profbox.pack(fill="x", padx=18, pady=(0, 12))
        tk.Label(profbox, text="Profesor asignado", font=FONT_BOLD,
                 bg="#f4f7fa", fg=C["primary"]).pack(anchor="w", padx=10, pady=(8, 2))
        texto_prof = profesor.nombre_completo if profesor else "Sin profesor asignado"
        tk.Label(profbox, text=texto_prof, font=FONT, bg="#f4f7fa", fg="#1a1a1a").pack(anchor="w", padx=10)
        if profesor:
            ttk.Button(profbox, text="Ver profesor", command=lambda: VentanaProfesorResumen(parent, profesor, curso)).pack(anchor="e", padx=10, pady=(4, 8))
        else:
            tk.Frame(profbox, bg="#f4f7fa", height=8).pack()

        tk.Label(self, text=f"Estudiantes matriculados ({len(matriculados)})", font=FONT_BOLD,
                 bg=C["card"], fg="#1a1a1a").pack(anchor="w", padx=18, pady=(2, 6))
        frame = tk.Frame(self, bg=C["card"])
        frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Programa", "Nota"), show="headings")
        for col, width in (("ID", 110), ("Nombre", 260), ("Programa", 90), ("Nota", 70)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="w")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        for e in matriculados:
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

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=(0, 14))
        self.transient(parent)
        self.grab_set()


class VentanaNomina(tk.Toplevel):
    """Desprendible Oficial de Pago de Nómina (formato institucional auditable UPC)."""
    def __init__(self, parent, profesor):
        super().__init__(parent)
        self.title(f"Desprendible de Liquidación - {profesor.nombre_completo}")
        self.configure(bg="#eef2f6")
        self.resizable(True, True)
        self.geometry("640x860")
        self.minsize(580, 720)
        self.periodo = "mensual"

        # ── Scrollable content ─────────────────────────────────────────────
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

        # ── Encabezado Oficial ─────────────────────────────────────────────
        card_header = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_header.pack(fill="x", padx=20, pady=(16, 12))

        top_h = tk.Frame(card_header, bg="white")
        top_h.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(top_h, text="🗎  Desprendible Oficial de Pago de Nómina",
                 font=("Segoe UI", 13, "bold"), bg="white", fg="#111827").pack(side="left")
        self.btn_periodo = ttk.Button(top_h, text="Ver anual", command=self._alternar_periodo)
        self.btn_periodo.pack(side="right")

        # Modalidad / Nro Liquidación
        liq_num = abs(hash(profesor.identificacion)) % 900 + 100
        sub_info = f"Docente: {profesor.nombre_completo}  |  Modalidad: {profesor.tipo_vinculacion.upper()}  |  Liquidación N° {liq_num}"
        tk.Label(card_header, text=sub_info, font=("Segoe UI", 9), bg="white", fg="#6b7280").pack(anchor="w", padx=16, pady=(0, 4))

        self.lbl_periodo_fechas = tk.Label(card_header, text="🗓 Período Liquidado: Marzo 2026  ·  01/03/2026 - 31/03/2026",
                                           font=("Segoe UI", 9, "bold"), bg="white", fg="#1d4ed8")
        self.lbl_periodo_fechas.pack(anchor="w", padx=16, pady=(0, 14))

        bruto = calcular_salario_bruto(profesor)
        disponible = liquidacion_disponible(profesor)

        if not disponible:
            self.btn_periodo.pack_forget()
            aviso = tk.Frame(inner, bg=C["warn_bg"], highlightbackground="#fca5a5", highlightthickness=1)
            aviso.pack(fill="x", padx=20, pady=8)
            tk.Label(aviso, text="NO SE LIQUIDA UN SALARIO INVENTADO",
                     font=FONT_BOLD, bg=C["warn_bg"], fg=C["warn_fg"]).pack(padx=14, pady=(10, 2))
            tk.Label(aviso, text="Falta el valor de hora cátedra fijado por resolución rectoral vigente.",
                     font=("Segoe UI", 9), bg=C["warn_bg"], fg=C["warn_fg"], wraplength=480).pack(padx=14, pady=(0, 10))
            return

        # ── Cálculos ───────────────────────────────────────────────────────
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

        # Helper para crear tarjetas
        def crear_tarjeta(titulo, subtotal_txt="", color_titulo="#1f4e79"):
            card = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
            card.pack(fill="x", padx=20, pady=(0, 12))

            header_t = tk.Frame(card, bg="white")
            header_t.pack(fill="x", padx=16, pady=(12, 8))
            tk.Label(header_t, text=titulo, font=("Segoe UI", 10, "bold"),
                     bg="white", fg=color_titulo).pack(side="left")
            lbl_sub = None
            if subtotal_txt:
                lbl_sub = tk.Label(header_t, text=subtotal_txt, font=("Segoe UI", 10, "bold"),
                                   bg="white", fg=color_titulo)
                lbl_sub.pack(side="right")
            return card, lbl_sub

        def fila_card(parent, label, valor, bold=False, color="#111827"):
            f = tk.Frame(parent, bg="white")
            f.pack(fill="x", padx=16, pady=3)
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
        tk.Frame(card_dev, bg="white", height=6).pack()

        # 2. DEDUCCIONES OBLIGATORIAS DE LEY (-)
        card_ded, self.lbl_sub_ded = crear_tarjeta(
            "DEDUCCIONES OBLIGATORIAS DE LEY (-)", f"$ {total_ded:,.0f} COP", color_titulo="#dc2626")
        self.lbl_ibc_ded = fila_card(card_ded, "IBC Seguridad Social (Base Cotización):", f"$ {bruto:,.0f} COP", bold=True)
        tk.Frame(card_ded, bg="white", height=4).pack()
        self.lbl_estampilla_val = fila_card(card_ded, "Descuento Estampilla Pro-UPC (0.2%)", f"- $ {estampilla:,} COP", color="#dc2626")
        self.lbl_retencion_val = fila_card(card_ded, "Retención en la Fuente por Salario (Art. 383 E.T.)",
                                          f"- $ {retencion:,} COP" if retencion > 0 else "$ 0 COP",
                                          color="#dc2626" if retencion > 0 else "#6b7280")
        self.lbl_pension_val = fila_card(card_ded, "Aporte Pensión Empleado (4% PILA)", f"- $ {pension_e:,} COP", color="#dc2626")
        self.lbl_salud_val = fila_card(card_ded, "Aporte Salud Empleado (4% PILA)", f"- $ {salud_e:,} COP", color="#dc2626")
        self.lbl_fsp_val = fila_card(card_ded, "Fondo de Solidaridad Pensional (1%)", f"- $ {fsp_e:,} COP" if fsp_e > 0 else "$ 0 COP", color="#dc2626" if fsp_e > 0 else "#6b7280")
        tk.Frame(card_ded, bg="white", height=6).pack()

        # 3. COSTO TOTAL EMPLEADOR (UPC)
        card_costo, self.lbl_sub_costo = crear_tarjeta(
            "COSTO TOTAL EMPLEADOR (UPC)", f"$ {costo_upc:,.0f} COP", color_titulo="#d97706")
        self.lbl_costo_asig = fila_card(card_costo, "Asignación Básica", f"$ {bruto:,.0f} COP", bold=True, color="#1d4ed8")
        self.lbl_ap_salud = fila_card(card_costo, "Salud Patronal (8.5%)", f"$ {ap['salud']:,} COP", color="#4b5563")
        self.lbl_ap_pension = fila_card(card_costo, "Pensión Patronal (12%)", f"$ {ap['pension']:,} COP", color="#4b5563")
        self.lbl_ap_arl = fila_card(card_costo, "Aporte Riesgos Laborales (ARL)", f"$ {ap['arl']:,} COP", color="#4b5563")
        self.lbl_ap_caja = fila_card(card_costo, "Caja de Compensación Familiar (4%)", f"$ {ap['caja']:,} COP", color="#4b5563")
        tk.Frame(card_costo, bg="#f3f4f6", height=1).pack(fill="x", padx=16, pady=6)
        self.lbl_costo_total_upc = fila_card(card_costo, "TOTAL COSTO UPC", f"$ {costo_upc:,.0f} COP", bold=True, color="#1d4ed8")
        tk.Frame(card_costo, bg="white", height=6).pack()

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
        tk.Frame(card_info, bg="white", height=6).pack()

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
        tk.Frame(card_ps, bg="white", height=6).pack()

        # 6. BANNER NETO A PAGAR (VERDE)
        neto_box = tk.Frame(inner, bg="white", highlightbackground="#10b981", highlightthickness=2)
        neto_box.pack(fill="x", padx=20, pady=(4, 16))

        neto_top = tk.Frame(neto_box, bg="white")
        neto_top.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(neto_top, text="NETO A PAGAR:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#111827").pack(side="left")
        self.lbl_neto_val = tk.Label(neto_top, text=f"$ {neto:,.0f} COP",
                                     font=("Segoe UI", 14, "bold"), bg="white", fg="#059669")
        self.lbl_neto_val.pack(side="right")

        self.lbl_neto_resumen = tk.Label(
            neto_box,
            text=f"Total Devengado: $ {devengado:,.0f} COP  ·  Total Deducciones: -$ {total_ded:,.0f} COP",
            font=("Segoe UI", 9), bg="white", fg="#6b7280"
        )
        self.lbl_neto_resumen.pack(anchor="w", padx=16, pady=(0, 12))

        # Guardar valores para switch Anual / Mensual
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

        # Botón cerrar
        ttk.Button(inner, text="Cerrar", command=self.destroy).pack(pady=(0, 20))
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
            self.lbl_periodo_fechas.configure(text="🗓 Período Liquidado: Año Vigente 2026 (Consolidado 12 Meses)")
        else:
            self.periodo = "mensual"
            f = 1
            self.btn_periodo.configure(text="Ver anual")
            self.lbl_periodo_fechas.configure(text="🗓 Período Liquidado: Agosto 2026  ·  01/08/2026 - 31/08/2026")

        # Devengados
        self.lbl_sub_dev.configure(text=f"$ {v['devengado']*f:,.0f} COP")
        self.lbl_asig_val.configure(text=f"+ $ {v['bruto']*f:,.0f} COP")
        if self.lbl_bonif_posg and v["bonif_posg"] > 0:
            self.lbl_bonif_posg.configure(text=f"+ $ {v['bonif_posg']*f:,.0f} COP")

        # Deducciones
        self.lbl_sub_ded.configure(text=f"$ {v['total_ded']*f:,.0f} COP")
        self.lbl_ibc_ded.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_estampilla_val.configure(text=f"- $ {v['estampilla']*f:,} COP")
        self.lbl_retencion_val.configure(text=f"- $ {v['retencion']*f:,} COP" if v['retencion'] > 0 else "$ 0 COP")
        self.lbl_pension_val.configure(text=f"- $ {v['pension_e']*f:,} COP")
        self.lbl_salud_val.configure(text=f"- $ {v['salud_e']*f:,} COP")
        self.lbl_fsp_val.configure(text=f"- $ {v['fsp_e']*f:,} COP" if v['fsp_e'] > 0 else "$ 0 COP")

        # Costo Empleador
        self.lbl_sub_costo.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")
        self.lbl_costo_asig.configure(text=f"$ {v['bruto']*f:,.0f} COP")
        self.lbl_ap_salud.configure(text=f"$ {v['ap_salud']*f:,} COP")
        self.lbl_ap_pension.configure(text=f"$ {v['ap_pension']*f:,} COP")
        self.lbl_ap_arl.configure(text=f"$ {v['ap_arl']*f:,} COP")
        self.lbl_ap_caja.configure(text=f"$ {v['ap_caja']*f:,} COP")
        self.lbl_costo_total_upc.configure(text=f"$ {v['costo_upc']*f:,.0f} COP")

        # Info Salarial
        if hasattr(self, "lbl_ibc_info"):
            self.lbl_ibc_info.configure(text=f"$ {v['bruto']*f:,.0f} COP")

        # Prestaciones
        self.lbl_sub_ps.configure(text=f"$ {v['total_ps']*f:,.0f} COP")
        self.lbl_ps_prima_s.configure(text=f"$ {v['prima_s']*f:,.0f} COP")
        self.lbl_ps_ces.configure(text=f"$ {v['ces']*f:,.0f} COP")
        self.lbl_ps_int_ces.configure(text=f"$ {v['int_ces']*f:,.0f} COP")
        self.lbl_ps_p_nav.configure(text=f"$ {v['p_nav']*f:,.0f} COP")
        self.lbl_ps_vac.configure(text=f"$ {v['vac']*f:,.0f} COP")
        self.lbl_ps_p_vac.configure(text=f"$ {v['p_vac']*f:,.0f} COP")
        self.lbl_ps_bonif.configure(text=f"$ {v['bonif']*f:,.0f} COP")

        # Neto
        self.lbl_neto_val.configure(text=f"$ {v['neto']*f:,.0f} COP")
        self.lbl_neto_resumen.configure(text=f"Total Devengado: $ {v['devengado']*f:,.0f} COP  ·  Total Deducciones: -$ {v['total_ded']*f:,.0f} COP")


class VentanaSalarioAdmin(tk.Toplevel):
    """Desprendible Oficial de Pago de Nómina Administrativa (UPC)."""
    def __init__(self, parent, admin):
        super().__init__(parent)
        self.title(f"Desprendible Administrativo - {admin.nombre_completo}")
        self.configure(bg="#eef2f6")
        self.resizable(True, True)
        self.geometry("640x780")
        self.minsize(580, 640)
        self.periodo = "mensual"

        # ── Scrollable content ─────────────────────────────────────────────
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

        # ── Encabezado Oficial ─────────────────────────────────────────────
        card_header = tk.Frame(inner, bg="white", highlightbackground="#dce2ea", highlightthickness=1)
        card_header.pack(fill="x", padx=20, pady=(16, 12))

        top_h = tk.Frame(card_header, bg="white")
        top_h.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(top_h, text="🗎  Desprendible Oficial de Pago - Personal Administrativo",
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#111827").pack(side="left")
        self.btn_periodo = ttk.Button(top_h, text="Ver anual", command=self._alternar_periodo)
        self.btn_periodo.pack(side="right")

        facultad = admin.codigo_facultad if admin.codigo_facultad else "Nivel Central"
        liq_num = abs(hash(admin.identificacion)) % 900 + 100
        sub_info = f"Funcionario: {admin.nombre_completo}  |  Cargo: {admin.cargo} ({admin.categoria})  |  Liquidación N° {liq_num}"
        tk.Label(card_header, text=sub_info, font=("Segoe UI", 9), bg="white", fg="#6b7280").pack(anchor="w", padx=16, pady=(0, 4))
        tk.Label(card_header, text=f"Contratación: {admin.tipo_contratacion}  |  Adscrito a: {facultad}",
                 font=("Segoe UI", 9, "italic"), bg="white", fg="#4b5563").pack(anchor="w", padx=16, pady=(0, 4))

        self.lbl_periodo_fechas = tk.Label(card_header, text="🗓 Período Liquidado: Marzo 2026  ·  01/03/2026 - 31/03/2026",
                                           font=("Segoe UI", 9, "bold"), bg="white", fg="#1d4ed8")
        self.lbl_periodo_fechas.pack(anchor="w", padx=16, pady=(0, 14))

        # ── Cálculos ───────────────────────────────────────────────────────
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
            card.pack(fill="x", padx=20, pady=(0, 12))

            header_t = tk.Frame(card, bg="white")
            header_t.pack(fill="x", padx=16, pady=(12, 8))
            tk.Label(header_t, text=titulo, font=("Segoe UI", 10, "bold"),
                     bg="white", fg=color_titulo).pack(side="left")
            lbl_sub = None
            if subtotal_txt:
                lbl_sub = tk.Label(header_t, text=subtotal_txt, font=("Segoe UI", 10, "bold"),
                                   bg="white", fg=color_titulo)
                lbl_sub.pack(side="right")
            return card, lbl_sub

        def fila_card(parent, label, valor, bold=False, color="#111827"):
            f = tk.Frame(parent, bg="white")
            f.pack(fill="x", padx=16, pady=3)
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
        tk.Frame(card_dev, bg="white", height=6).pack()

        # 2. DEDUCCIONES OBLIGATORIAS DE LEY (-)
        card_ded, self.lbl_sub_ded = crear_tarjeta(
            "DEDUCCIONES OBLIGATORIAS DE LEY (-)", f"$ {total_ded:,.0f} COP", color_titulo="#dc2626")
        self.lbl_ibc_ded = fila_card(card_ded, "IBC Seguridad Social (Base Cotización):", f"$ {bruto:,.0f} COP", bold=True)
        tk.Frame(card_ded, bg="white", height=4).pack()
        self.lbl_salud_val = fila_card(card_ded, "Aporte Salud Trabajador (4%)", f"- $ {salud_e:,} COP", color="#dc2626")
        self.lbl_pension_val = fila_card(card_ded, "Aporte Pensión Trabajador (4%)", f"- $ {pension_e:,} COP", color="#dc2626")
        self.lbl_fsp_val = fila_card(card_ded, "Fondo de Solidaridad Pensional (1%)", f"- $ {fsp_e:,} COP" if fsp_e > 0 else "$ 0 COP", color="#dc2626" if fsp_e > 0 else "#6b7280")
        tk.Frame(card_ded, bg="white", height=6).pack()

        # 3. COSTO TOTAL EMPLEADOR (UPC)
        card_costo, self.lbl_sub_costo = crear_tarjeta(
            "COSTO TOTAL EMPLEADOR (UPC)", f"$ {costo_upc:,.0f} COP", color_titulo="#d97706")
        self.lbl_costo_asig = fila_card(card_costo, "Asignación Básica", f"$ {bruto:,.0f} COP", bold=True, color="#1d4ed8")
        self.lbl_ap_salud = fila_card(card_costo, "Salud Patronal (8.5%)", f"$ {ap['salud']:,} COP", color="#4b5563")
        self.lbl_ap_pension = fila_card(card_costo, "Pensión Patronal (12%)", f"$ {ap['pension']:,} COP", color="#4b5563")
        self.lbl_ap_arl = fila_card(card_costo, "Aporte Riesgos Laborales (ARL)", f"$ {ap['arl']:,} COP", color="#4b5563")
        self.lbl_ap_caja = fila_card(card_costo, "Caja de Compensación Familiar (4%)", f"$ {ap['caja']:,} COP", color="#4b5563")
        tk.Frame(card_costo, bg="#f3f4f6", height=1).pack(fill="x", padx=16, pady=6)
        self.lbl_costo_total_upc = fila_card(card_costo, "TOTAL COSTO UPC", f"$ {costo_upc:,.0f} COP", bold=True, color="#1d4ed8")
        tk.Frame(card_costo, bg="white", height=6).pack()

        # 4. BANNER NETO A PAGAR (VERDE)
        neto_box = tk.Frame(inner, bg="white", highlightbackground="#10b981", highlightthickness=2)
        neto_box.pack(fill="x", padx=20, pady=(4, 16))

        neto_top = tk.Frame(neto_box, bg="white")
        neto_top.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(neto_top, text="NETO A PAGAR:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#111827").pack(side="left")
        self.lbl_neto_val = tk.Label(neto_top, text=f"$ {neto:,.0f} COP",
                                     font=("Segoe UI", 14, "bold"), bg="white", fg="#059669")
        self.lbl_neto_val.pack(side="right")

        self.lbl_neto_resumen = tk.Label(
            neto_box,
            text=f"Total Devengado: $ {bruto:,.0f} COP  ·  Total Deducciones: -$ {total_ded:,.0f} COP",
            font=("Segoe UI", 9), bg="white", fg="#6b7280"
        )
        self.lbl_neto_resumen.pack(anchor="w", padx=16, pady=(0, 12))

        # Guardar valores para switch Anual / Mensual
        self._val = {
            "bruto": bruto, "total_ded": total_ded, "salud_e": salud_e, "pension_e": pension_e, "fsp_e": fsp_e,
            "costo_upc": costo_upc, "ap_salud": ap["salud"], "ap_pension": ap["pension"],
            "ap_arl": ap["arl"], "ap_caja": ap["caja"], "neto": neto,
        }

        ttk.Button(inner, text="Cerrar", command=self.destroy).pack(pady=(0, 20))
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
            self.lbl_periodo_fechas.configure(text="🗓 Período Liquidado: Año Vigente 2026 (Consolidado 12 Meses)")
        else:
            self.periodo = "mensual"
            f = 1
            self.btn_periodo.configure(text="Ver anual")
            self.lbl_periodo_fechas.configure(text="🗓 Período Liquidado: Marzo 2026  ·  01/03/2026 - 31/03/2026")

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
