# VASP-Electronic-Structure-Tools
Automated post-processing and visualization tools for VASP electronic structure calculations, generating customizable, publication-ready DOS and Band Structure figures from VASPkit outputs in high-resolution PNG and vector PDF formats.

## 📁 Guides
- [DOS Guide](DOS/README.md)
- [Band Structure Guide](BAND/README.md)

## 🖥️ Requirements
- Python 3.8+ with `numpy` and `matplotlib`
- VASPkit (version 1.3.5 or 1.5.1)

## 🚀 Quick Start
1. Run VASPkit to generate the required `.dat` files (see each guide).
2. Place the corresponding Python script in the same folder.
3. Execute `python3 plot_all_dos.py` or `python3 plot_all_bands.py`.

---

**Tested on TiB₂**  
Distributed under the MIT License.
