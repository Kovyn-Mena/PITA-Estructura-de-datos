# Revisión normativa de nómina PITA — 2026

Esta documentación consolida la implementación técnica, fórmulas legales y arquitectura de nómina implementada en **PITA** tanto para **Python** (GUI con Tkinter y lógica) como para **C++** (consola modular).

---

## 1. Docentes de Planta (Decreto 1279 de 2002)

Aplica a empleados públicos docentes de carrera.
- **Fórmula de asignación básica:**
  $$\text{Salario Bruto} = (\text{Total Puntos}) \times \text{Valor Punto 2026} \times \text{Factor Dedicación}$$
- **Valor del punto 2026:** **$23.924 COP** (*Decreto 318 de 2026, art. 2*).
- **Puntos base pregrado:** 178 puntos (*Decreto 1279 de 2002, art. 7*).
- **Puntos escalafón:** Auxiliar (37 pts), Asistente (58 pts), Asociado (74 pts), Titular (96 pts).
- **Factor dedicación:** Tiempo Completo ($1.0$), Medio Tiempo ($0.5$).
- **Experiencia y productividad:** Se computan los puntos ya reconocidos en el registro. No se convierten automáticamente años de experiencia sin acto administrativo.

---

## 2. Docentes Ocasionales (Acuerdo UPC 027 de 2024, Art. 24)

No se rigen por el Decreto 1279. Su asignación básica y bonificaciones se calculan en SMMLV:
- **SMMLV Vigente 2026:** **$1.750.905 COP** (*Decreto 159 de 2026*).
- **Factores de asignación básica (Sueldo):**
  - Auxiliar TC: $2.645$ SMMLV | MT: $1.509$ SMMLV
  - Asistente TC: $3.125$ SMMLV | MT: $1.749$ SMMLV
  - Asociado TC: $3.606$ SMMLV | MT: $1.990$ SMMLV
  - Titular TC: $3.918$ SMMLV | MT: $2.146$ SMMLV
- **Bonificación mensual por cualificación en postgrado (Acuerdo UPC 027/2024):**
  - Especialización: $0.10$ SMMLV ($175.091 COP)
  - Maestría: $0.45$ SMMLV ($787.907 COP)
  - Doctorado: $0.90$ SMMLV ($1.575.815 COP)
  - *Nota legal:* Esta bonificación es un reconocimiento económico adicional y no constituye factor salarial para liquidación de prestaciones ni aportes a seguridad social.
- **Total Devengados:** $\text{Sueldo Básico} + \text{Bonificación Postgrado}$.

---

## 3. Docentes Catedráticos (Acuerdo UPC 027 de 2024, Art. 23)

- La liquidación depende de las horas mensuales asignadas y el valor hora fijado por resolución rectoral.
- Si no está configurada la resolución vigente, el sistema indica explícitamente **"Liquidación no disponible / pendiente de resolución rectoral"** sin inventar valores ficticios.
- Soporta modalidad **Ad-honorem** (sin remuneración).
- La bonificación por postgrado se reconoce de forma proporcional a las horas cátedra.

---

## 4. Deducciones Obligatorias del Trabajador

Conforme al **Decreto 1990 de 2016** (plataforma PILA) y la normativa tributaria:
1. **Salud empleado (4%):** Se calcula sobre el salario básico (IBC) y se aproxima al **múltiplo de 100 más cercano** según regla PILA.
2. **Pensión empleado (4%):** Se calcula sobre el salario básico (IBC) y se aproxima al **múltiplo de 100 más cercano**.
3. **Fondo de Solidaridad Pensional - FSP (1%):** Aplica si el salario básico $\ge 4\text{ SMMLV}$ ($7.003.620 COP).
4. **Descuento Estampilla Pro-UPC (0.2%):** Gravamen territorial del $0.2\%$ sobre el sueldo básico contractual.
5. **Retención en la fuente por salarios (Art. 383 Estatuto Tributario):** Se aplica la tarifa del $19\%$ sobre la base gravable depurada (restando salud y pensión obligatoria y el $25\%$ de renta exenta laboral) que exceda el umbral de 95 UVT, redondeado a miles (norma DIAN).
- **Neto a Pagar:** $\text{Total Devengados} - \text{Total Deducciones}$.
  *(Ejemplo real docente Adith Pérez: Devengado \$7.889.578 - Deducciones \$624.828 = **\$7.264.750 COP**)*.

---

## 5. Costo Total Empleador UPC (Aportes Patronales)

Aportes institucionales que asume la Universidad Popular del Cesar:
- **Pensión Patronal (12%):** $\text{round}(\text{Bruto} \times 0.12)$ (*Ley 100 de 1993, art. 20*).
- **Salud Patronal (8.5%):** $\text{round}(\text{Bruto} \times 0.085)$ (*Ley 1122 de 2007, art. 10*).
- **ARL Clase I (0.522%):** $\text{round}(\text{Bruto} \times 0.00522)$ (*Decreto 1295 de 1994*).
- **Caja de Compensación Familiar (4%):** $\text{round}(\text{Bruto} \times 0.04)$ (*Ley 21 de 1982*).
- **TOTAL COSTO UPC (Auditable institucional):**
  $$\text{Costo UPC} = \text{Asignación Básica} + \text{Salud Patronal} + \text{Pensión Patronal} + \text{ARL} + \text{Caja Compensación}$$

---

## 6. Prestaciones Sociales (Provisión Mensual Legal)

Provisiones contables obligatorias para servidores públicos docentes y administrativos:
1. **Prima de Servicios (Decreto 1279/2002 art. 44):** 30 días de salario por año $\rightarrow \text{Bruto} / 12$.
2. **Cesantías (Decreto 1279/2002 art. 45 / Ley 50 de 1990):** 1 mes de salario por año $\rightarrow \text{Bruto} / 12$.
3. **Intereses a las Cesantías (Ley 52 de 1975):** 12% anual (1% mensual sobre cesantías) $\rightarrow \text{Bruto} / 1200$.
4. **Prima de Navidad (Decreto 1042 de 1978 art. 33):** 1 mes de salario por año $\rightarrow \text{Bruto} / 12$.
5. **Vacaciones Remuneradas:** 15 días hábiles al año $\rightarrow \text{Bruto} / 24$.
6. **Prima de Vacaciones (Decreto 1279/2002 art. 33):** 15 días adicionales $\rightarrow \text{Bruto} / 24$.
7. **Bonificación por Servicios Prestados (Decreto 1279/2002 art. 39):** Equivalente a 2 meses por año $\rightarrow \text{Bruto} \times 2 / 12$.

---

## 7. Personal Administrativo (Escala Salarial y Liquidación)

Para evitar salarios inventados, se articuló la escala salarial por niveles del sector público:
- **Nivel 1 (Asistencial / Auxiliar / Biblioteca):** $\$1.950.000\text{ COP}$
- **Nivel 2 (Técnico / Secretario Académico):** $\$2.800.000\text{ COP}$
- **Nivel 3 (Profesional Universitario / Coordinador):** $\$3.750.000\text{ COP}$
- **Nivel 4 (Directivo / Asesor / Jefe de Oficina):** $\$5.050.000\text{ COP}$
- Si en la creación/edición se ingresa 0, el sistema asigna automáticamente el valor de la escala legal.
- Aplican las mismas deducciones legales (Salud 4%, Pensión 4%, FSP 1% si $\ge 4$ SMMLV) y Aportes Patronales UPC.

---

## 8. Sincronización entre Python y C++

Ambos proyectos comparten exactamente las mismas reglas, constantes y cálculos:
- **Python:**
  - `python/src/nomina.py`: Módulo con toda la lógica pura de nómina y escala administrativa.
  - `python/src/gui.py`: Clases `VentanaNomina` y `VentanaSalarioAdmin` con diseño oficial de desprendible por tarjetas, switch dinámico anual/mensual y banner verde de Neto a Pagar.
- **C++:**
  - `cpp/include/nomina.h` y `cpp/src/nomina.cpp`: Declaración e implementación de toda la matemática prestacional y aportes patronales.
  - `cpp/src/main.cpp`: Menú Profesores (opción 6) y Menú Administrativos (opción 6) para imprimir desprendibles oficiales formateados en consola.
  - `cpp/src/gestion.cpp`: Formulario de creación/modificación de administrativos asistido por escala legal de niveles.
