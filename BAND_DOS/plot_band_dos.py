import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from matplotlib.gridspec import GridSpec

# ================================================================
# USER SETTINGS - Publication Quality
# ================================================================
PLOT_DPI = 600                  # DPI for PNG preview (high resolution)
SAVE_PDF = True                 # Set to True to save vector PDF files
ENERGY_MIN = -8.0               # Y-axis minimum (eV)
ENERGY_MAX = 8.0                # Y-axis maximum (eV)
DOT_SIZE_SCALE = 20             # Scale factor for projected band dot sizes
BAND_DIR = '../BAND'            # Relative path to BAND folder
DOS_DIR = '../DOS'              # Relative path to DOS folder
# ================================================================

# ----------------------------------------------------------------
# 1. PROFESSIONAL PUBLICATION STYLING
# ----------------------------------------------------------------
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Computer Modern']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = PLOT_DPI
# ----------------------------------------------------------------

# Helper function to save figures in both PNG and PDF
def save_figure(fig, basename):
    fig.savefig(f'{basename}.png', dpi=PLOT_DPI, bbox_inches='tight')
    if SAVE_PDF:
        fig.savefig(f'{basename}.pdf', bbox_inches='tight')
    plt.close(fig)
    print(f" Created: {basename}.png & .pdf" if SAVE_PDF else f" Created: {basename}.png")

def format_ax(ax, title, ylabel=True, xlabel=True, is_band=True):
    """Apply publication-grade formatting to axes."""
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8, label=r'$E_F$')
    ax.set_ylim(ENERGY_MIN, ENERGY_MAX)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    if ylabel:
        ax.set_ylabel(r'$E - E_F$ (eV)', fontsize=14)
    if xlabel:
        if is_band:
            ax.set_xlabel(r'$k$-path', fontsize=14)
        else:
            ax.set_xlabel('DOS (states/eV)', fontsize=14)
    ax.grid(True, linestyle=':', alpha=0.4, linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax

# ----------------------------------------------------------------
# 2. READ HIGH-SYMMETRY POINTS
# ----------------------------------------------------------------
klabels_path = os.path.join(BAND_DIR, 'KLABELS')
k_labels, k_coords = [], []
if os.path.exists(klabels_path):
    with open(klabels_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                coord = float(parts[1])
                label = parts[0]
                if label.upper() in ['G', 'GAMMA']:
                    label = r'$\Gamma$'
                k_labels.append(label)
                k_coords.append(coord)
            except ValueError:
                continue
else:
    print("Warning: KLABELS not found. Using default path.")
    k_labels = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
    k_coords = [0.0, 0.5, 0.8, 1.0]

# ----------------------------------------------------------------
# 3. LOAD BAND DATA
# ----------------------------------------------------------------
band_file = os.path.join(BAND_DIR, 'REFORMATTED_BAND.dat')
if not os.path.exists(band_file):
    band_file = os.path.join(BAND_DIR, 'BAND.dat')
plain_band = np.loadtxt(band_file) if os.path.exists(band_file) else None

pband_files = sorted(glob.glob(os.path.join(BAND_DIR, 'PBAND_*.dat')))
pband_data = {}
for pf in pband_files:
    elem = os.path.basename(pf).replace('PBAND_', '').replace('.dat', '')
    pband_data[elem] = np.loadtxt(pf)

# ----------------------------------------------------------------
# 4. LOAD DOS DATA (with correct PDOS parsing - LAST column)
# ----------------------------------------------------------------
tdos_file = os.path.join(DOS_DIR, 'TDOS.dat')
tdos_data = np.loadtxt(tdos_file) if os.path.exists(tdos_file) else None

pdos_files = sorted(glob.glob(os.path.join(DOS_DIR, 'PDOS_*.dat')))
pdos_data = {}
for pf in pdos_files:
    elem = os.path.basename(pf).replace('PDOS_', '').replace('.dat', '')
    data = np.loadtxt(pf)
    total_pdos = data[:, -1]  # CORRECT: Use the 'tot' column
    pdos_data[elem] = {'energy': data[:, 0], 'total': total_pdos}

# ----------------------------------------------------------------
# 5. SETUP PLOT LAYOUT
# ----------------------------------------------------------------
fig = plt.figure(figsize=(12, 6))
gs = GridSpec(1, 2, width_ratios=[2.2, 1], wspace=0.08)

ax_band = fig.add_subplot(gs[0])
ax_dos = fig.add_subplot(gs[1], sharey=ax_band)

colors = plt.cm.Set1.colors

# ----------------------------------------------------------------
# 6. PLOT BAND STRUCTURE (left panel)
# ----------------------------------------------------------------
if plain_band is not None:
    for i in range(1, plain_band.shape[1]):
        ax_band.plot(plain_band[:, 0], plain_band[:, i],
                     color='lightgray' if pband_data else '#1f77b4',
                     linewidth=0.6 if pband_data else 1.2,
                     zorder=1, alpha=0.7)

if pband_data:
    for idx, (elem, data) in enumerate(pband_data.items()):
        color = colors[idx % len(colors)]
        sizes = np.maximum(data[:, 2] * DOT_SIZE_SCALE, 0.5)
        ax_band.scatter(data[:, 0], data[:, 1], s=sizes,
                        color=color, alpha=0.7, label=elem,
                        zorder=2, edgecolors='none')

for x in k_coords:
    ax_band.axvline(x, color='dimgray', linestyle='--', linewidth=0.6, alpha=0.7)

if k_coords:
    ax_band.set_xticks(k_coords)
    ax_band.set_xticklabels(k_labels, fontsize=12)
    ax_band.set_xlim(k_coords[0], k_coords[-1])

format_ax(ax_band, '(a) Band Structure', ylabel=True, xlabel=True, is_band=True)

if pband_data:
    ax_band.legend(loc='upper right', frameon=True, framealpha=0.9,
                   edgecolor='black', fontsize=10)

# ----------------------------------------------------------------
# 7. PLOT DOS (right panel)
# ----------------------------------------------------------------
max_dos_visible = 0.0

if tdos_data is not None:
    energy_tdos = tdos_data[:, 0]
    tdos_val = tdos_data[:, 1]
    mask = (energy_tdos >= ENERGY_MIN) & (energy_tdos <= ENERGY_MAX)
    if np.any(mask):
        max_dos_visible = max(max_dos_visible, np.max(tdos_val[mask]))
    ax_dos.plot(tdos_val[mask], energy_tdos[mask],
                color='black', label='TDOS', linewidth=1.8, zorder=3)
    ax_dos.fill_betweenx(energy_tdos[mask], 0, tdos_val[mask],
                         color='gray', alpha=0.15)

for idx, (elem, data) in enumerate(pdos_data.items()):
    color = colors[idx % len(colors)]
    energy_pdos = data['energy']
    total_pdos = data['total']
    mask = (energy_pdos >= ENERGY_MIN) & (energy_pdos <= ENERGY_MAX)
    if np.any(mask):
        max_dos_visible = max(max_dos_visible, np.max(total_pdos[mask]))
    ax_dos.plot(total_pdos[mask], energy_pdos[mask],
                color=color, label=elem, linewidth=1.4, zorder=2)

if max_dos_visible > 0:
    ax_dos.set_xlim(0, max_dos_visible * 1.15)
else:
    ax_dos.set_xlim(0, 1.0)

format_ax(ax_dos, '(b) Density of States', ylabel=False, xlabel=True, is_band=False)

# --- FIX 1: Use tick_params instead of set_xticklabels to avoid FixedFormatter warning ---
ax_dos.tick_params(axis='x', labelsize=11)

# Hide y-axis ticks on DOS panel (since it shares y-axis with band panel)
plt.setp(ax_dos.get_yticklabels(), visible=False)

ax_dos.legend(loc='upper right', frameon=True, framealpha=0.9,
              edgecolor='black', fontsize=10)

# ----------------------------------------------------------------
# 8. SAVE FIGURE
# ----------------------------------------------------------------
# --- FIX 2: Use subplots_adjust instead of tight_layout to avoid warning ---
fig.subplots_adjust(left=0.07, right=0.95, top=0.93, bottom=0.12, wspace=0.08)

save_figure(fig, 'Band_DOS_Combined')
print("\n All tasks completed successfully!")
