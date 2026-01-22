"""
Plotting utilities for ATLAS light curve visualization.

TODO:
- Use Gaia magnitude to correct over sky subtraction
"""

import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

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
                             dpi=120, alpha=0.7, marker_size=3):
    if not binned_lc:
        return None
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    phases_c = binned_lc['c']['phase']
    flux_c = binned_lc['c']['flux']
    flux_err_c = binned_lc['c']['flux_err']

    ax.errorbar(phases_c, flux_c, flux_err_c, fmt='.', ms=marker_size, 
               alpha=alpha, capsize=3, color='cyan', label='c-band')

    phases_o = binned_lc['o']['phase']
    flux_o = binned_lc['o']['flux']
    flux_err_o = binned_lc['o']['flux_err']

    ax.errorbar(phases_o, flux_o, flux_err_o, fmt='.', ms=marker_size, 
               alpha=alpha, capsize=3, color='orange', label='o-band')
    
    ax.set_xlabel('Phase')
    ax.set_ylabel('Flux (µJy)')
    ax.set_xlim(-1, 2)
    ax.legend(loc='best')
    
    if source_id:
        ax.set_title(f'Gaia DR3 ID: {source_id}')
    
    fig.tight_layout()
    
    return fig

def plot_phase_folded(lc_data, period, reference_epoch=None, period_derivative=0,
                      source_id=None, figsize=(10, 4), dpi=120, 
                      alpha=0.5, marker_size=1.5, num_cycles=3):
    from .timeseries import phase_fold
    import numpy as np
    
    # Extract data
    times = lc_data['time']
    flux = lc_data['flux']
    flux_err = lc_data['flux_err']
    filters = lc_data['filter']
    
    # Phase fold the data
    phases = phase_fold(times, period, period_derivative, reference_epoch)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    colors = {'c': 'cyan', 'o': 'orange'}
    
    # Plot each filter
    for filt in sorted(set(filters)):
        mask = filters == filt
        phase_filt = phases[mask]
        flux_filt = flux[mask]
        flux_err_filt = flux_err[mask]
        
        # Replicate for multiple cycles
        if num_cycles == 1:
            phase_plot = phase_filt
            flux_plot = flux_filt
            flux_err_plot = flux_err_filt
        elif num_cycles == 2:
            phase_plot = np.concatenate([phase_filt - 1, phase_filt])
            flux_plot = np.concatenate([flux_filt, flux_filt])
            flux_err_plot = np.concatenate([flux_err_filt, flux_err_filt])
        elif num_cycles == 3:
            phase_plot = np.concatenate([phase_filt - 1, phase_filt, phase_filt + 1])
            flux_plot = np.concatenate([flux_filt, flux_filt, flux_filt])
            flux_err_plot = np.concatenate([flux_err_filt, flux_err_filt, flux_err_filt])
        else:
            raise ValueError(f"num_cycles must be 1, 2, or 3, got {num_cycles}")
        
        ax.errorbar(phase_plot, flux_plot, flux_err_plot,
                   fmt='.', ms=marker_size, alpha=alpha, capsize=0,
                   color=colors.get(filt, 'gray'), label=f'{filt}-band')
    
    ax.set_xlabel('Phase', fontsize=12)
    ax.set_ylabel('Flux (µJy)', fontsize=12)
    ax.set_xlim(-1 if num_cycles >= 2 else 0, 2 if num_cycles == 3 else 1)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    if source_id:
        ax.set_title(f'Gaia DR3 ID: {source_id}', fontsize=14)
    
    fig.tight_layout()
    
    return fig

def plot_scatter(catalog, x_col, y_col, color_col=None, 
                 figsize=(12, 6), dpi=120,
                 xscale='log', yscale='log',
                 reference_x=None, reference_y=None,
                 xlim=None, ylim=None,
                 xlabel=None, ylabel=None, colorbar_label=None,
                 title=None, **scatter_kwargs):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Default scatter parameters
    scatter_defaults = {'s': 20, 'alpha': 0.6}
    if color_col is not None:
        scatter_defaults.update({'cmap': 'viridis'})
    else:
        scatter_defaults.update({'color': 'steelblue'})
    scatter_defaults.update(scatter_kwargs)
    
    # Create scatter plot
    if color_col is not None:
        scatter = ax.scatter(catalog[x_col], catalog[y_col], 
                            c=catalog[color_col], **scatter_defaults)
        # Add colorbar
        cbar_label = colorbar_label if colorbar_label is not None else color_col
        plt.colorbar(scatter, ax=ax, label=cbar_label)
    else:
        ax.scatter(catalog[x_col], catalog[y_col], **scatter_defaults)
    
    # Add reference lines
    if reference_x is not None:
        if not isinstance(reference_x, (list, tuple)):
            reference_x = [reference_x]
        for x_val in reference_x:
            ax.axvline(x_val, color='red', linestyle='--', alpha=0.5)
    
    if reference_y is not None:
        if not isinstance(reference_y, (list, tuple)):
            reference_y = [reference_y]
        for y_val in reference_y:
            ax.axhline(y_val, color='gray', linestyle=':', alpha=0.5)
    
    # Set scales
    if xscale:
        ax.set_xscale(xscale)
    if yscale:
        ax.set_yscale(yscale)
    
    # Set limits
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    
    # Labels
    ax.set_xlabel(xlabel if xlabel is not None else x_col, fontsize=12)
    ax.set_ylabel(ylabel if ylabel is not None else y_col, fontsize=12)
    
    if title:
        ax.set_title(title, fontsize=14)
    
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    
    return fig

def plot_multi_lightcurves(catalog, gid_col='gid', n_per_row=3,
                           num_bins=200, markersize=2):
    from .io import read_bin_lightcurve 
    
    # Get GIDs
    if catalog.index.name == gid_col:
        gids = catalog.index
        rows = catalog
    else:
        gids = catalog[gid_col].values
        rows = catalog.set_index(gid_col)
        
    n_candidates = len(gids)
    n_rows = (n_candidates + n_per_row - 1) // n_per_row
    n_rows = min(n_rows, 4)
    figsize=(15,n_rows*2)
    
    fig, axes = plt.subplots(n_rows, n_per_row, 
                            figsize=(figsize[0], figsize[1] * n_rows),
                            dpi=100)
    
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    axes_flat = axes.flatten()
    
    for idx, gid in enumerate(gids):
        if idx >= len(axes_flat):
            break
            
        ax = axes_flat[idx]
        row = rows.loc[gid]
        
        binned_lc = read_bin_lightcurve(gid, num_bins=num_bins)
        

        ax.errorbar(binned_lc['c']['phase'], 
                   binned_lc['c']['flux'],
                   binned_lc['c']['flux_err'], 
                   fmt='.', ms=marker_size,
                   alpha=0.5, color='cyan', label='c')
            
        ax.errorbar(binned_lc['o']['phase'], 
                   binned_lc['o']['flux'],
                   binned_lc['o']['flux_err'], 
                   fmt='.', ms=marker_size,
                   alpha=0.5, color='orange', label='o')
        
        ax.set_xlim(-1, 2)
        
        # Title with key parameters
        period_str = f"{row['per_min']:.1f}m" if 'per_min' in row else f"{row.get('per_day', 0):.4f}d"
        ax.set_title(f"P={period_str}, SNR={row['snr']:.1f}", fontsize=9)
        ax.set_xlabel('Phase', fontsize=8)
        ax.set_ylabel('Flux (µJy)', fontsize=8)
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=6, loc='best')
    
    # Hide unused axes
    for idx in range(n_candidates, len(axes_flat)):
        axes_flat[idx].axis('off')
    
    plt.tight_layout()
    return fig