# DOS Plotting Guide

This guide explains how to extract and plot Density of States (DOS) from VASP output using VASPkit, and generate high-quality figures suitable for publication.

---

## 📁 Folder Structure

```text
Project/
└── DOS/
    ├── DOSCAR
    ├── POSCAR
    ├── INCAR (must contain LORBIT)
    └── (after VASPkit runs)
        ├── TDOS.dat
        ├── PDOS_Ti.dat
        ├── PDOS_B.dat
        └── ...

---

## 🛠️ Prerequisites

* Python 3.8+ with numpy and matplotlib
* VASPkit installed
* VASP calculation with LORBIT = 11 or 12 in INCAR

---

## 📝 Step-by-Step Extraction with VASPkit

1. Navigate to your DOS folder:
   cd DOS

2. Launch VASPkit:
   vaspkit

3. Select the DOS menu: type 11 and press Enter.

4. Extract total DOS: type 111 – this creates TDOS.dat.

5. Extract element-resolved PDOS: type 113 – then enter the element indices.

---

## 🖥️ Plotting with the Python Script

1. Copy the script plot_all_dos.py into the DOS folder.
2. Run the script:
   python3 plot_all_dos.py

Output files:
* TDOS.png / .pdf
* PDOS_*.png / .pdf (one per element)
* DOS_Master_Summary.png / .pdf – combined plot with all curves.

---

## ⚙️ Script Settings

* PLOT_DPI = 600 (PNG resolution)
* SAVE_PDF = True (save vector PDFs)
* ENERGY_RANGE = [-10.0, 10.0] (x-axis range in eV)
* APPLY_ATOMIC_SCALING = False (keep False for VASPkit 113 output)

---

## 📚 References
* [VASPkit Documentation](https://vaspkit.com)
* [VASP Manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual)
