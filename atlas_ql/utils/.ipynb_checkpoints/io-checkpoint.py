def read_lightcurve(source_id):
    from .paths import lc_path
    from .timeseries import bjd_convert
    import pandas as pd 
    import os

    cols = {
        'mjd': 0, # start of exposure (all exposures are 30s)
        'm': 1, 'dm': 2,
        'ujy': 3, 'dujy': 4,
        'filter': 5,
        'err': 6, # tphot error flag
        'chi_n': 7, # reduced chi^2 of PSF fit
        'ra': 8, 'dec': 9, # RA and DEC at which the PSF is forced
        'x': 10, 'y': 11, # x- and y-pixel value at which the PSF is forced
        'maj': 12, 'min': 13, 'phi': 14,
        'apfit': 15, # aperture correction (in mags) required by tphot
        'mag5sig': 16, # five-sigma limit magnitude
        'pa_deg': 17, # fitted position angle between North and detector Y-axis
        'sky': 18, # sky mag in 1 sq arcsec
        'obs': 19 # the ATLAS data file on which the measurements were made
    }

    path = lc_path(source_id)
    try:
        df = pd.read_csv(path, sep='\s+', header=None, comment='#')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return None
    
    # Get coordinates
    ra = float(df.iloc[0, cols['ra']])
    dec = float(df.iloc[0, cols['dec']])
    
    # Convert to mid-exposure time (MJD is start of 30s exposure, add 15s)
    t_mjd = df.iloc[:, cols['mjd']].to_numpy(float)
    t_mid_mjd = t_mjd + 15.0 / 86400.0  # Add 15 seconds in days
    
    # Convert to barycentric Julian date
    t_bjd = bjd_convert(t_mid_mjd, ra, dec, date_format='mjd')
    
    flux = df.iloc[:, cols['ujy']].to_numpy(float)
    flux_err = df.iloc[:, cols['dujy']].to_numpy(float)
    filter_col = df.iloc[:, cols['filter']].to_numpy(str)

    return {"time": t_bjd, "flux": flux, "flux_err": flux_err,
            "filter": filter_col, "ra": ra, "dec": dec}

def read_bin_lightcurve(source_id, num_bins=500, num_cycles=3, normalization=False,
                       period=None, reference_epoch=None):
    from .timeseries import bin_phase_folded_data
    from .bls import get_bls_stats

    lc_data = read_lightcurve(source_id)
    if lc_data is None:
        return None
    
    bls_data = get_bls_stats(source_id)
    if bls_data is None and period is None:
        return None
    if bls_data is not None:
        print(f'Period: {bls_data["per_min"]} min')
        period=bls_data['per_day']
        reference_epoch=bls_data['epo']
    
    c_mask = lc_data['filter'] == 'c'
    o_mask = lc_data['filter'] == 'o'
    
    binned_c = bin_phase_folded_data(
        time=lc_data['time'][c_mask],
        flux=lc_data['flux'][c_mask],
        flux_err=lc_data['flux_err'][c_mask],
        period=period,
        reference_epoch=reference_epoch,
        num_bins=num_bins,
        num_cycles=num_cycles,
        normalization=normalization
    )
    
    binned_o = bin_phase_folded_data(
        time=lc_data['time'][o_mask],
        flux=lc_data['flux'][o_mask],
        flux_err=lc_data['flux_err'][o_mask],
        period=period,
        reference_epoch=reference_epoch,
        num_bins=num_bins,
        num_cycles=num_cycles,
        normalization=normalization
    )
    
    return {"c": binned_c, "o": binned_o}