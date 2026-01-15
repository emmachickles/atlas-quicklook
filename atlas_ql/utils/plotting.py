"""
Plotting utilities for ATLAS light curve visualization.

TODO:
- Use Gaia magnitude to correct over sky subtraction
"""

import io
import matplotlib.pyplot as plt


def plot_lightcurve(lc_data, source_id=None, figsize=(10, 4), dpi=120, 
                    alpha=0.7, marker_size=2.5):

    # Extract data from lightcurve dict
    times = lc_data['time']
    flux = lc_data['flux']
    flux_err = lc_data['flux_err']
    filters = lc_data['filter']
    
    # Plot by filter
    fig, ax = plt.subplots(figsize=figsize)
    colors = {'o': 'orange', 'c': 'cyan'}
    
    for filt in sorted(set(filters)):
        mask = filters == filt
        ax.errorbar(times[mask], flux[mask], flux_err[mask], 
                   fmt='.', ms=marker_size, alpha=alpha, capsize=3,
                   label=f"Filter {filt}", color=colors.get(filt, 'gray'))
    
    ax.set_xlabel('Time (MJD)')
    ax.set_ylabel('Flux (µJy)')
    
    if source_id:
        ax.set_title(f'Gaia DR3 ID: {source_id}')
    
    ax.legend(loc='best', fontsize=8)
    fig.tight_layout()
    
    return fig


def plot_binned_phase_folded(binned_lc, source_id=None, figsize=(10, 4), 
                             dpi=120, alpha=0.7, marker_size=3, color='steelblue'):
    phases = binned_lc[:, 0]
    flux = binned_lc[:, 1]
    flux_err = binned_lc[:, 2]
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    ax.errorbar(phases, flux, flux_err, fmt='.', ms=marker_size, alpha=alpha,
               capsize=3, color=color)
    
    ax.set_xlabel('Phase')
    ax.set_ylabel('Flux (µJy)')
    ax.set_xlim(-1, 2)
    
    if source_id:
        ax.set_title(f'Gaia DR3 ID: {source_id}')
    
    fig.tight_layout()
    
    return fig
