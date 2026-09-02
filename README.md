# PITA — Integrated Program for Academic Transactions
Universidad Popular del Cesar · Data Structures · Workshop 1

Group: [Kovyn Mena]

## Project Structure
```text
PITA/
├── cpp/            C++ Version
│   ├── include/     Headers (.h): entities, management, payroll, persistence
│   ├── src/         Implementation (.cpp) and main.cpp
│   ├── data/        Data files (plain text)
│   └── Makefile
├── python/         Python Version (same logic and data format)
│   ├── src/         entidades.py, gestion.py, nomina.py, persistencia.py, main.py
│   └── data/        Data files (plain text)
└── docs/           Design diagrams and persistence format specification

```

## How to Run — C++ Version

Requirements: `g++` with C++17 support (any standard Linux/Mac/WSL installation will work).

```bash
cd cpp
make run

```

This compiles (`make`) and executes (`./pita`) in a single step. If you only want to compile the project first:

```bash
make
./pita

```

To clean the compiled binaries:

```bash
make clean

```

## How to Run — Python Version

Requirements: Python 3.8 or higher. No external dependencies required (uses standard library only).

```bash
cd python/src
python3 main.py

```

## Program Usage

1. Upon startup, the program will ask if you want to **load existing data** from the `data/` directory or **start without data**. You can answer `s` (yes) or `n` (no).
2. The main menu allows you to navigate through the management modules for each entity (Faculties, Programs, Courses, Students, Professors, Administrative Staff) and simulate payroll calculations.
3. Each entity's submenu provides standard CRUD operations: Create, List, Update, Deactivate, and Delete.
4. Upon exiting the program (option `0` in the main menu), all data is automatically saved to the `data/` directory.

## Test Data

The project is delivered with preloaded data inside the `data/` folders for both versions. This allows the professor to test the system immediately without needing to manually input mock information.

## Design Documentation

Please refer to `docs/formato_persistencia.md` for a detailed breakdown of the data file formats. The comprehensive conceptual design, the applied institutional regulations (Decree 1279 of 2002 and Agreement 027 of 2024), and the reasoning behind our data structure decisions are detailed in the Word document submitted alongside this repository.
