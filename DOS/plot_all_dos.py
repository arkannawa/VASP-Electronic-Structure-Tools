import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# ================================================================
# USER SETTINGS - Publication Quality 
# ================================================================
PLOT_DPI = 600                  # DPI for PNG preview (high resolution)
SAVE_PDF = True                 # Set to True to save vector PDF files
ENERGY_RANGE = [-10.0, 10.0]    # Energy range for x-axis (eV)
APPLY_ATOMIC_SCALING = False    # Keep False for VASPKIT 113 output set true if ypur PDOS is per atom
# ================================================================

# ----------------------------------------------------------------
# 1. PROFESSIONAL PUBLICATION STYLING (copied from Band code)
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
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.dpi'] = PLOT_DPI
# ----------------------------------------------------------------

# Helper function to save figures in both PNG and PDF
def save_figure(fig, basename):
    """Save figure as high-res PNG and optionally as vector PDF."""
    fig.savefig(f'{basename}.png', dpi=PLOT_DPI, bbox_inches='tight')
    if SAVE_PDF:
        fig.savefig(f'{basename}.pdf', bbox_inches='tight')
    plt.close(fig)
    print(f" Created: {basename}.png & .pdf" if SAVE_PDF else f" Created: {basename}.png")

# Helper function for plot formatting (publication style)
def format_ax(ax, title, ylabel=True):
    """Apply publication-grade formatting to DOS axes."""
    # Fermi level line (dashed, thin)
    ax.axvline(x=0, color='red', linestyle='--', linewidth=0.8, label=r'$E_F$', zorder=4)
    
    # Set x-axis limits
    ax.set_xlim(ENERGY_RANGE[0], ENERGY_RANGE[1])
    
    # Labels
    ax.set_xlabel(r'$E - E_F$ (eV)', fontsize=14)
    if ylabel:
        ax.set_ylabel('Density of States (states/eV)', fontsize=14)
    
    # Title
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    # Subtle grid
    ax.grid(True, linestyle=':', alpha=0.4, linewidth=0.5)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    return ax


def get_atomic_counts(poscar_path="POSCAR"):
    """
    Automatically reads the POSCAR file to extract element names and their counts.
    Returns a dictionary: {'Element': number_of_atoms}
    """
    counts = {}
    try:
        with open(poscar_path, 'r') as f:
            lines = f.readlines()
        if len(lines) < 6:
            return counts
        
        elements_line = lines[5].strip().split()
        atoms_line = lines[6].strip().split()
        
        if all(not val.replace('.', '').isdigit() for val in elements_line) and len(elements_line) > 0:
            if len(elements_line) == len(atoms_line):
                for i, elem in enumerate(elements_line):
                    counts[elem] = int(atoms_line[i])
            else:
                if len(atoms_line) >= len(elements_line):
                    for i, elem in enumerate(elements_line):
                        counts[elem] = int(atoms_line[i])
                else:
                    for elem in elements_line:
                        counts[elem] = 1
        else:
            if len(lines) > 6:
                test_line = lines[6].strip().split()
                if all(not val.replace('.', '').isdigit() for val in test_line) and len(test_line) > 0:
                    elements_line = test_line
                    atoms_line = lines[7].strip().split()
                    for i, elem in enumerate(elements_line):
                        if i < len(atoms_line):
                            counts[elem] = int(atoms_line[i])
    except Exception as e:
        print(f"Warning: Could not read {poscar_path}. Error: {e}")
    
    return counts


def parse_pdos_data(data):
    """
    Correctly parses VASPKIT PDOS data.
    Uses the LAST column ('tot') directly.
    """
    num_cols = data.shape[1]
    
    # Read the LAST column as the total PDOS (tot)
    total_pdos = data[:, -1]  
    
    dict_orbitals = {}
    
    if num_cols == 4:  # Energy, s, p, d (Already aggregated)
        dict_orbitals['s'] = data[:, 1]
        dict_orbitals['p'] = data[:, 2]
        dict_orbitals['d'] = data[:, 3]
    elif num_cols >= 10:  # LORBIT=11 detailed orbitals (s, py, pz, px, d1..d5)
        dict_orbitals['s'] = data[:, 1]
        dict_orbitals['p'] = np.sum(data[:, 2:5], axis=1)
        dict_orbitals['d'] = np.sum(data[:, 5:10], axis=1)
        if num_cols >= 17:
            dict_orbitals['f'] = np.sum(data[:, 10:17], axis=1)
    else:  # General fallback
        for i in range(1, num_cols):
            dict_orbitals[f'orb_{i}'] = data[:, i]
            
    return total_pdos, dict_orbitals


def plot_file(filepath, atom_counts=None):
    filename = os.path.basename(filepath)
    basename = os.path.splitext(filename)[0]
    
    try:
        data = np.loadtxt(filepath)
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return

    if data.ndim < 2 or data.shape[1] < 2:
        return

    energy = data[:, 0]

    mask = (energy >= ENERGY_RANGE[0]) & (energy <= ENERGY_RANGE[1])
    if not np.any(mask):
        mask = np.ones(len(energy), dtype=bool)

    fig, ax = plt.subplots(figsize=(7, 5))
    ymax = 0.0

    # Case 1: Total DOS or Integrated Total DOS
    if basename in ['TDOS', 'ITDOS']:
        y_val = data[:, 1]
        ax.plot(energy, y_val, label=basename, color='black', linewidth=1.5, zorder=3)
        ax.fill_between(energy, 0, y_val, color='black', alpha=0.1)
        ymax = np.max(y_val[mask])
        format_ax(ax, basename, ylabel=True)

    # Case 2: Partial DOS or Integrated Partial DOS
    else:
        elem_name = basename.replace('PDOS_', '').replace('IPDOS_', '')
        total_per_atom, dict_orbitals = parse_pdos_data(data)
        
        if APPLY_ATOMIC_SCALING and atom_counts:
            scale_factor = atom_counts.get(elem_name, 1.0)
        else:
            scale_factor = 1.0
            
        total_scaled = total_per_atom * scale_factor
        ymax = np.max(total_scaled[mask])

        # Plot orbital breakdown (s, p, d, f) - Clean labels without (scaled)
        colors_orb = {'s': 'crimson', 'p': 'dodgerblue', 'd': 'forestgreen', 'f': 'darkorange'}
        for orb_name, orb_val in dict_orbitals.items():
            color = colors_orb.get(orb_name, 'purple')
            orb_scaled = orb_val * scale_factor
            ax.plot(energy, orb_scaled, label=f'{orb_name}',
                     color=color, linestyle='--', linewidth=1.2, zorder=2)

        # Plot total contribution - Clean label without (cell)
        ax.plot(energy, total_scaled, label=f'Total {elem_name}',
                 color='navy', linewidth=1.8, zorder=3)
        
        format_ax(ax, f'{elem_name} PDOS', ylabel=True)

    ax.set_ylim(0, ymax * 1.15 if ymax > 0 else 1.0)
    ax.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black', fontsize=11)
    plt.tight_layout()
    save_figure(fig, basename)


def create_master_summary(atom_counts=None):
    """Generates a combined master plot with TDOS and all PDOS elements."""
    if not os.path.exists('TDOS.dat'):
        print("TDOS.dat not found. Skipping master summary.")
        return

    tdos_data = np.loadtxt('TDOS.dat')
    energy = tdos_data[:, 0]
    tdos_val = tdos_data[:, 1]
    
    mask = (energy >= ENERGY_RANGE[0]) & (energy <= ENERGY_RANGE[1])
    if not np.any(mask):
        mask = np.ones(len(energy), dtype=bool)

    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Clean label for Total DOS
    ax.plot(energy, tdos_val, label='Total DOS', color='black', linewidth=1.8, zorder=3)
    ax.fill_between(energy, 0, tdos_val, color='gray', alpha=0.15)

    ymax = np.max(tdos_val[mask])

    pdos_files = sorted([f for f in glob.glob('PDOS_*.dat') if not f.startswith('IPDOS')])
    colors = ['crimson', 'dodgerblue', 'forestgreen', 'darkorange', 'purple', 'brown', 'pink']

    for idx, pdos_file in enumerate(pdos_files):
        elem_name = os.path.splitext(pdos_file)[0].replace('PDOS_', '')
        data = np.loadtxt(pdos_file)
        
        elem_per_atom, _ = parse_pdos_data(data)
        
        if APPLY_ATOMIC_SCALING and atom_counts:
            scale_factor = atom_counts.get(elem_name, 1.0)
        else:
            scale_factor = 1.0
            
        elem_scaled = elem_per_atom * scale_factor
        color = colors[idx % len(colors)]
        
        # Clean label for PDOS elements
        ax.plot(energy, elem_scaled, label=f'{elem_name}', color=color, linewidth=1.4, zorder=2)
        ymax = max(ymax, np.max(elem_scaled[mask]))

    format_ax(ax, 'Complete Density of States (DOS) Spectrum', ylabel=True)
    ax.set_ylim(0, ymax * 1.15 if ymax > 0 else 1.0)
    ax.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black', fontsize=11)
    plt.tight_layout()
    save_figure(fig, 'DOS_Master_Summary')


if __name__ == "__main__":
    print("Attempting to read POSCAR for reference...")
    atom_counts = get_atomic_counts("POSCAR")
    if atom_counts:
        print(" Detected atomic counts per unit cell:", atom_counts)
    else:
        print(" POSCAR not found or could not be parsed.")
    
    if APPLY_ATOMIC_SCALING:
        print(" NOTE: Atomic scaling is ENABLED.")
    else:
        print(" NOTE: Atomic scaling is DISABLED.")

    dat_files = glob.glob("*.dat")
    if not dat_files:
        print("No .dat files found in the current directory.")
    else:
        print("\n--- Processing individual files ---")
        for f in dat_files:
            plot_file(f, atom_counts)
        
        print("\n--- Generating Master Summary Plot ---")
        create_master_summary(atom_counts)
        print("\nAll tasks completed successfully!")
