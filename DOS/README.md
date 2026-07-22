# DOS Plotting Guide

This guide explains how to extract and plot Density of States (DOS) from VASP output using VASPkit, and generate high-quality figures suitable for publication.

---

## 📁 Folder Structure

```text
Project/
└── DOS/
    ├── INCAR
    ├── POSCAR
    ├── KPOINTS
    ├── TDOS.dat
    ├── PDOS_Ti.dat
    ├── PDOS_B.dat
    ├── ITDOS.dat
    ├── IPDOS_Ti.dat
    ├── IPDOS_B.dat
    ├── plot_all_dos.py
    ├── README.md
    └── plots/
        ├── TDOS.png / .pdf
        ├── PDOS_Ti.png / .pdf
        ├── PDOS_B.png / .pdf
        ├── IPDOS_Ti.png / .pdf
        ├── IPDOS_B.png / .pdf
        ├── ITDOS.png / .pdf
        └── DOS_Master_Summary.png / .pdf
```

---

## 🛠️ Prerequisites

* Python 3.8+ with `numpy` and `matplotlib`
* VASPkit installed
* VASP calculation with `LORBIT = 11` or `12` in `INCAR`

> **Note on POTCAR**: Generate the combined `POTCAR` from your local pseudopotential library using:
> ```bash
> cat path/to/Ti-sv/POTCAR path/to/B/POTCAR > POTCAR
> ```

---

## 📝 Step-by-Step Extraction with VASPkit

1. **Navigate to your DOS folder**:
   ```bash
   cd DOS
   ```

2. **Launch VASPkit**:
   ```bash
   vaspkit
   ```

3. **Select DOS Menu**: Type `11` and press Enter.

4. **Extract Total DOS**: Type `111` – generates `TDOS.dat`.

5. **Extract Partial DOS (PDOS)**: Type `113` – enter atom indices (e.g., `1-2` for Ti and B) to generate `PDOS_Ti.dat`, `PDOS_B.dat`, etc.

---

## 🖥️ Plotting with the Python Script

1. Run the script:
   ```bash
   python3 plot_all_dos.py
   ```

2. All generated plots and vector PDFs will be organized inside the `plots/` directory.

**Outputs Summary:**
* `TDOS.png` / `.pdf`: Total Density of States.
* `PDOS_*.png` / `.pdf`: Partial Density of States for each element.
* `DOS_Master_Summary.png` / `.pdf`: Combined Master plot featuring all orbital/element contributions.

---

## ⚙️ Script Settings (adjustable at top of plot_all_dos.py)

```python
PLOT_DPI = 600                  # PNG resolution
SAVE_PDF = True                 # save vector PDFs
ENERGY_RANGE = [-10.0, 10.0]    # x-axis energy range (eV)
APPLY_ATOMIC_SCALING = False    # keep False for VASPkit 113 output
```

---

## 📚 References
* [VASPkit Documentation](https://vaspkit.com)
* [VASP Manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual)
