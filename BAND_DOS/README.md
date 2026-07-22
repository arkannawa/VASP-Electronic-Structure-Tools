# Combined Band Structure & DOS Plotter

This directory contains a script to generate a publication-quality side-by-side plot combining both the Electronic Band Structure and the Total/Partial Density of States (DOS).

---

## 📁 Folder Structure

```text
BAND_DOS/
├── plot_band_dos.py
├── README.md
├── Band_DOS_Combined.png
└── Band_DOS_Combined.pdf
```

---

## ⚙️ How It Works

The script `plot_band_dos.py` automatically fetches extracted data files from adjacent directories:
* **Band Data**: Read from `../BAND/` (`BAND.dat`, `PBAND_*.dat`, `KLABELS`).
* **DOS Data**: Read from `../DOS/` (`TDOS.dat`, `PDOS_*.dat`).

> **Note**: Make sure you have already generated the extracted `.dat` files in both `../BAND` and `../DOS` directories before running this script.

---

## 🖥️ Usage

1. Navigate to the `BAND_DOS` directory:
   ```bash
   cd BAND_DOS
   ```

2. Run the script:
   ```bash
   python3 plot_band_dos.py
   ```

3. High-resolution figures (`.png` and vector `.pdf`) will be automatically saved in the `plots/` directory.

---

## 🎨 Features & Publication Settings
* Shared Y-axis energy alignment ($E - E_F$).
* Automatic extraction of Fermi energy and High-Symmetry K-path lines.
* Matplotlib configuration tuned for academic publications ($600\text{ DPI}$, Times New Roman typography, vector PDF output).
