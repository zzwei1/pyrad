"""
======================================================
Dataset and products processing (:mod:`pyrad.proc`)
======================================================

.. currentmodule:: pyrad.proc

Initiate the dataset and products processing.

Dataset processing
==================

.. autosummary::
    :toctree: generated/

    process_raw
    process_echo_id
    process_snr
    process_signal_power
    process_l
    process_cdr
    process_correct_noise_rhohv
    process_correct_bias
    process_echo_filter
    process_filter_snr
    process_estimate_phidp0
    process_correct_phidp0
    process_smooth_phidp_single_window
    process_smooth_phidp_double_window
    process_kdp_leastsquare_single_window
    process_kdp_leastsquare_double_window
    process_phidp_kdp_Maesaka
    process_phidp_kdp_lp
    process_attenuation
    process_rainrate
    process_hydroclass
    process_point_measurement
    process_save_radar
    process_selfconsistency_kdp_phidp
    process_selfconsistency_bias
    process_rhohv_rain
    process_sun_hits

Product processing
==================

.. autosummary::
    :toctree: generated/

    generate_vol_products
    generate_timeseries_products
    generate_sun_hits_products

"""

from .process_dataset import get_process_type, process_raw, process_echo_id
from .process_dataset import process_snr, process_l, process_cdr
from .process_dataset import process_correct_noise_rhohv, process_correct_bias
from .process_dataset import process_echo_filter, process_filter_snr
from .process_dataset import process_attenuation, process_signal_power
from .process_dataset import process_phidp_kdp_lp, process_phidp_kdp_Maesaka
from .process_dataset import process_estimate_phidp0, process_correct_phidp0
from .process_dataset import process_smooth_phidp_single_window
from .process_dataset import process_smooth_phidp_double_window
from .process_dataset import process_kdp_leastsquare_single_window
from .process_dataset import process_kdp_leastsquare_double_window

from .process_dataset import process_rainrate, process_hydroclass
from .process_dataset import process_point_measurement, process_save_radar
from .process_dataset import process_selfconsistency_kdp_phidp
from .process_dataset import process_selfconsistency_bias, process_rhohv_rain
from .process_dataset import process_sun_hits

from .process_product import get_product_type, generate_vol_products
from .process_product import generate_timeseries_products
from .process_product import generate_sun_hits_products

__all__ = [s for s in dir() if not s.startswith('_')]
