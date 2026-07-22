import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# ================================================================
# USER SETTINGS - Customize for highest quality
# ================================================================
ENERGY_MIN = -10          # Y-axis minimum (eV)
ENERGY_MAX = 10           # Y-axis maximum (eV)
DOT_SIZE_SCALE = 30        # Size of projected dots
PLOT_DPI = 1000             # DPI for PNG preview
SAVE_PDF = True            # Set to True to save vector PDF files
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
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.fontsize'] = 11
# ----------------------------------------------------------------

# 2. Read High-Symmetry Points
k_labels, k_coords = [], []
if os.path.exists('KLABELS'):
    with open('KLABELS', 'r') as f:
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
    k_labels = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
    k_coords = [0.0, 0.5, 0.8, 1.0]

# 3. Find Band Data Files
band_file = None
if os.path.exists('REFORMATTED_BAND.dat'):
    band_file = 'REFORMATTED_BAND.dat'
elif os.path.exists('BAND.dat'):
    band_file = 'BAND.dat'

plain_data = np.loadtxt(band_file) if band_file else None

# 4. Find Projected Band Files
pband_files = sorted(glob.glob('PBAND_*.dat'))
elements_data = {}
for pfile in pband_files:
    elem = pfile.replace('PBAND_', '').replace('.dat', '')
    elements_data[elem] = np.loadtxt(pfile)

# 5. Color Palette
colors = plt.cm.Set1.colors
if len(colors) < len(elements_data):
    colors = plt.cm.tab10.colors

# Helper Function
def format_ax(ax, title, ylabel=True, show_legend=False):
    ax.axhline(0, color='black', linestyle='-', linewidth=0.8, label=r'$E_F$' if show_legend else "")
    for x in k_coords:
        ax.axvline(x, color='dimgray', linestyle='--', linewidth=0.6, alpha=0.7)
    if k_coords:
        ax.set_xticks(k_coords)
        ax.set_xticklabels(k_labels, fontsize=12)
        ax.set_xlim(k_coords[0], k_coords[-1])
    ax.set_ylim(ENERGY_MIN, ENERGY_MAX)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    if ylabel:
        ax.set_ylabel(r'$E - E_F$ (eV)', fontsize=14)
    ax.grid(True, linestyle=':', alpha=0.4, linewidth=0.5)
    return ax

def save_figure(fig, basename):
    fig.savefig(f'{basename}.png', dpi=PLOT_DPI, bbox_inches='tight')
    if SAVE_PDF:
        fig.savefig(f'{basename}.pdf', bbox_inches='tight')
    plt.close(fig)

# ================================================================
# IMAGE 1: Plain Band Structure
# ================================================================
if plain_data is not None:
    fig, ax = plt.subplots(figsize=(6, 6), dpi=PLOT_DPI)
    for i in range(1, plain_data.shape[1]):
        ax.plot(plain_data[:, 0], plain_data[:, i], color='#1f77b4', linewidth=1.0, alpha=0.8)
    format_ax(ax, 'Plain Band Structure', ylabel=True, show_legend=False)
    save_figure(fig, '1_Plain_Band_Structure')
    print(" Created: 1_Plain_Band_Structure.png & .pdf")

# ================================================================
# IMAGE 2: Projected Band Structure
# ================================================================
if elements_data:
    fig, ax = plt.subplots(figsize=(6, 6), dpi=PLOT_DPI)
    if plain_data is not None:
        for i in range(1, plain_data.shape[1]):
            ax.plot(plain_data[:, 0], plain_data[:, i], color='lightgray', linewidth=0.5, zorder=1, alpha=0.6)
    for idx, (elem, data) in enumerate(elements_data.items()):
        color = colors[idx % len(colors)]
        sizes = np.maximum(data[:, 2] * DOT_SIZE_SCALE, 0.5)
        ax.scatter(data[:, 0], data[:, 1], s=sizes, color=color, alpha=0.7, label=elem, zorder=2, edgecolors='none')
    format_ax(ax, 'Projected Band Structure', ylabel=True, show_legend=True)
    ax.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black', fontsize=11)  # <--- FIXED: removed linewidth
    save_figure(fig, '2_Projected_Band_Structure')
    print(" Created: 2_Projected_Band_Structure.png & .pdf")

# ================================================================
# IMAGE 3: Combined Side-by-Side
# ================================================================
if plain_data is not None and elements_data:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True, dpi=PLOT_DPI)
    for i in range(1, plain_data.shape[1]):
        ax1.plot(plain_data[:, 0], plain_data[:, i], color='#1f77b4', linewidth=1.0, alpha=0.8)
    format_ax(ax1, '(a) Plain', ylabel=True, show_legend=False)
    for i in range(1, plain_data.shape[1]):
        ax2.plot(plain_data[:, 0], plain_data[:, i], color='lightgray', linewidth=0.5, zorder=1, alpha=0.6)
    for idx, (elem, data) in enumerate(elements_data.items()):
        color = colors[idx % len(colors)]
        sizes = np.maximum(data[:, 2] * DOT_SIZE_SCALE, 0.5)
        ax2.scatter(data[:, 0], data[:, 1], s=sizes, color=color, alpha=0.7, label=elem, zorder=2, edgecolors='none')
    format_ax(ax2, '(b) Projected', ylabel=False, show_legend=True)
    ax2.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black', fontsize=11)  # <--- FIXED: removed linewidth
    plt.tight_layout()
    save_figure(fig, '3_Bands_Comparison')
    print(" Created: 3_Bands_Comparison.png & .pdf")

print("\n All high-quality band structure plots generated successfully!")
print(" PDF files are vector graphics, perfect for publication!")
