# VASP-Electronic-Structure-Tools

Automated post-processing and visualization tools for VASP electronic structure calculations, generating customizable, publication-ready DOS and Band Structure figures from VASPkit outputs in high-resolution PNG and vector PDF formats.

---

## 📁 Guides & Modules

* 📊 **[DOS Guide](./DOS/README.md)** – Total and Partial Density of States extraction & plotting.
* 📈 **[Band Structure Guide](./BAND/README.md)** – Electronic band structure & element-projected bands.
* 🔄 **[Combined BAND + DOS](./BAND_DOS)** – Side-by-side publication-ready combined plot script.

---

## 🖥️ Requirements

* Python 3.8+ with `numpy` and `matplotlib`
* VASPkit (version 1.3.5 or 1.5.1)

---

## 🚀 Quick Start

1. Run VASPkit to generate the required `.dat` files (see each guide).
2. Execute the corresponding script inside its folder:
   ```bash
   python3 DOS/plot_all_dos.py
   python3 BAND/plot_all_bands.py
   python3 BAND_DOS/plot_band_dos.py
   ```

---

*Tested on $\text{TiB}_2$*  
*Distributed under the MIT License.*
