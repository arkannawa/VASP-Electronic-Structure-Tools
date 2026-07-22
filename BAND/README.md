# Band Structure Plotting Guide

This guide explains how to extract and plot electronic Band Structure and Projected Band Structure (PBAND) from VASP output using VASPkit, and generate publication-quality figures using `plot_all_bands.py`.

---

## 📁 Folder Structure

```text
Project/
└── BAND/
    ├── INCAR
    ├── POSCAR
    ├── KPOINTS
    ├── PRIMCELL.vasp
    ├── BAND.dat
    ├── BAND_GAP
    ├── KLABELS
    ├── KLINES.dat
    ├── PBAND_Ti.dat
    ├── PBAND_B.dat
    ├── REFORMATTED_BAND.dat
    ├── HIGH_SYMMETRY_POINTS
    ├── plot_all_bands.py
    ├── README.md
    └── plots/
        ├── 1_Plain_Band_Structure.png / .pdf
        ├── 2_Projected_Band_Structure.png / .pdf
        └── 3_Bands_Comparison.png / .pdf
```

---

## 🛠️ Prerequisites

* Python 3.8+ with `numpy` and `matplotlib`
* VASPkit installed
* VASP calculation completed with `ICHARG = 11` (Non-self-consistent calculation)

> **Note on POTCAR**: Generate the combined `POTCAR` from your local pseudopotential library using:
> ```bash
> cat path/to/Ti-sv/POTCAR path/to/B/POTCAR > POTCAR
> ```

---

## 📝 Step-by-Step Extraction with VASPkit

1. **Generate High-Symmetry K-Path**:
   * Launch `vaspkit`, select option `3` (K-Path Generation) -> `302` or `303` to generate `KPATH.in` and `HIGH_SYMMETRY_POINTS`.

2. **Run VASP Calculation**:
   * Perform the band structure calculation using the generated `KPOINTS` file.

3. **Extract Band Data**:
   * Launch `vaspkit` in the working directory.
   * Select menu `21` (Band-Structure Analysis).
   * Select `211` to extract total band structure (`BAND.dat`, `BAND_GAP`, `KLABELS`, `KLINES.dat`).
   * Select `213` (or element-projected option) to generate elemental `PBAND_Ti.dat`, `PBAND_B.dat`, etc.

---

## 🖥️ Plotting with `plot_all_bands.py`

1. Run the Python plotting script:
   ```bash
   python3 plot_all_bands.py
   ```

2. All generated figures are automatically organized inside the `plots/` directory.

**Output Figures:**
* `1_Plain_Band_Structure.png` / `.pdf`: Standard electronic band structure.
* `2_Projected_Band_Structure.png` / `.pdf`: Element-projected (fat-band) structure.
* `3_Bands_Comparison.png` / `.pdf`: Comparative multi-panel summary figure.

---

## 📚 References
* [VASPkit Documentation](https://vaspkit.com)
* [VASP Manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual)
