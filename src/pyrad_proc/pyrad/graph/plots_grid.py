"""
pyrad.graph.plots_grid
======================

Functions to plot data in a Cartesian grid format

.. autosummary::
    :toctree: generated/

    plot_surface
    plot_surface_contour
    plot_latitude_slice
    plot_longitude_slice
    plot_latlon_slice

"""

from warnings import warn
import numpy as np

import matplotlib as mpl
mpl.use('Agg')

# Increase a bit font size
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family':  "sans-serif"})

import matplotlib.pyplot as plt

import pyart

from .plots_aux import get_norm


def plot_surface(grid, field_name, level, prdcfg, fname_list, titl=None,
                 save_fig=True, use_basemap=True):
    """
    plots a surface from gridded data

    Parameters
    ----------
    grid : Grid object
        object containing the gridded data to plot
    field_name : str
        name of the radar field to plot
    level : int
        level index
    prdcfg : dict
        dictionary containing the product configuration
    fname_list : list of str
        list of names of the files where to store the plot
    titl : str
        Plot title
    save_fig : bool
        if true save the figure. If false it does not close the plot and
        returns the handle to the figure

    Returns
    -------
    fname_list : list of str or
    fig, ax : tupple
        list of names of the saved plots or handle of the figure an axes

    """
    dpi = prdcfg['gridMapImageConfig'].get('dpi', 72)

    norm, ticks, ticklabs = get_norm(field_name)

    xsize = prdcfg['gridMapImageConfig']['xsize']
    ysize = prdcfg['gridMapImageConfig']['ysize']
    lonstep = prdcfg['gridMapImageConfig'].get('lonstep', 0.5)
    latstep = prdcfg['gridMapImageConfig'].get('latstep', 0.5)
    min_lon = prdcfg['gridMapImageConfig'].get('lonmin', 2.5)
    max_lon = prdcfg['gridMapImageConfig'].get('lonmax', 12.5)
    min_lat = prdcfg['gridMapImageConfig'].get('latmin', 43.5)
    max_lat = prdcfg['gridMapImageConfig'].get('latmax', 49.5)

    lon_lines = np.arange(np.floor(min_lon), np.ceil(max_lon)+1, lonstep)
    lat_lines = np.arange(np.floor(min_lat), np.ceil(max_lat)+1, latstep)

    fig = plt.figure(figsize=[xsize, ysize], dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')

    if use_basemap:
        resolution = prdcfg['gridMapImageConfig'].get('mapres', 'l')
        if resolution not in ('c', 'l', 'i', 'h', 'f'):
            warn('Unknown map resolution: '+resolution)
            resolution = 'l'

        if resolution == 'c':
            area_thresh = 10000
        elif resolution == 'l':
            area_thresh = 1000
        elif resolution == 'i':
            area_thresh = 100
        elif resolution == 'h':
            area_thresh = 10
        elif resolution == 'f':
            area_thresh = 1

        display = pyart.graph.GridMapDisplayBasemap(grid)
        display.plot_basemap(
            lat_lines=lat_lines, lon_lines=lon_lines, resolution=resolution,
            area_thresh=area_thresh, auto_range=False, min_lon=min_lon,
            max_lon=max_lon, min_lat=min_lat, max_lat=max_lat, ax=ax)
        display.plot_grid(
            field_name, level=level, norm=norm, ticks=ticks, title=titl,
            ticklabs=ticklabs, ax=ax, fig=fig)
    else:
        resolution = prdcfg['gridMapImageConfig'].get('mapres', '110m')
        if resolution not in ('110m', '50m', '10m'):
            warn('Unknown map resolution: '+resolution)
            resolution = '110m'

        display = pyart.graph.GridMapDisplay(grid)
        ax, fig = display.plot_grid(
            field_name, level=level, norm=norm, ticks=ticks, ticklabs=ticklabs,
            resolution=resolution, lat_lines=lat_lines, lon_lines=lon_lines,
            maps_list=prdcfg['gridMapImageConfig']['maps'],
            title=titl, ax=ax, fig=fig)
        # display.plot_crosshairs(lon=lon, lat=lat)

    if save_fig:
        for fname in fname_list:
            fig.savefig(fname, dpi=dpi)
        plt.close(fig)

        return fname_list

    return (fig, ax, display)


def plot_surface_contour(grid, field_name, level, prdcfg, fname_list,
                         contour_values=None, linewidths=1.5, ax=None,
                         fig=None, display=None, save_fig=True,
                         use_basemap=True):
    """
    plots a surface from gridded data

    Parameters
    ----------
    grid : Grid object
        object containing the gridded data to plot
    field_name : str
        name of the radar field to plot
    level : int
        level index
    prdcfg : dict
        dictionary containing the product configuration
    fname_list : list of str
        list of names of the files where to store the plot
    contour_values : float array
        list of contours to plot
    linewidths : float
        width of the contour lines
    fig : Figure
        Figure to add the colorbar to. If none a new figure will be created
    ax : Axis
        Axis to plot on. if fig is None a new axis will be created
    save_fig : bool
        if true save the figure if false it does not close the plot and
        returns the handle to the figure

    Returns
    -------
    fname_list : list of str or
    fig, ax : tupple
        list of names of the saved plots or handle of the figure an axes

    """
    # get contour intervals
    if contour_values is None:
        field_dict = pyart.config.get_metadata(field_name)
        if 'boundaries' in field_dict:
            vmin = field_dict['boundaries'][0]
            vmax = field_dict['boundaries'][-1]
            num = len(field_dict['boundaries'])
        else:
            vmin, vmax = pyart.config.get_field_limits(field_name)
            num = 10

        contour_values = np.linspace(vmin, vmax, num=num)

    dpi = prdcfg['gridMapImageConfig'].get('dpi', 72)

    if fig is None:
        xsize = prdcfg['gridMapImageConfig']['xsize']
        ysize = prdcfg['gridMapImageConfig']['ysize']
        lonstep = prdcfg['gridMapImageConfig'].get('lonstep', 0.5)
        latstep = prdcfg['gridMapImageConfig'].get('latstep', 0.5)
        min_lon = prdcfg['gridMapImageConfig'].get('lonmin', 2.5)
        max_lon = prdcfg['gridMapImageConfig'].get('lonmax', 12.5)
        min_lat = prdcfg['gridMapImageConfig'].get('latmin', 43.5)
        max_lat = prdcfg['gridMapImageConfig'].get('latmax', 49.5)

        lon_lines = np.arange(np.floor(min_lon), np.ceil(max_lon)+1, lonstep)
        lat_lines = np.arange(np.floor(min_lat), np.ceil(max_lat)+1, latstep)

        fig = plt.figure(figsize=[xsize, ysize], dpi=dpi)
        ax = fig.add_subplot(111, aspect='equal')

        if use_basemap:
            resolution = prdcfg['gridMapImageConfig'].get('mapres', 'l')
            if resolution not in ('c', 'l', 'i', 'h', 'f'):
                warn('Unknown map resolution: '+resolution)
                resolution = 'l'

            if resolution == 'c':
                area_thresh = 10000
            elif resolution == 'l':
                area_thresh = 1000
            elif resolution == 'i':
                area_thresh = 100
            elif resolution == 'h':
                area_thresh = 10
            elif resolution == 'f':
                area_thresh = 1

            display = pyart.graph.GridMapDisplayBasemap(grid)
            display.plot_basemap(
                lat_lines=lat_lines, lon_lines=lon_lines,
                resolution=resolution, auto_range=False,
                area_thresh=area_thresh, min_lon=min_lon, max_lon=max_lon,
                min_lat=min_lat, max_lat=max_lat, ax=ax)

            lons, lats = grid.get_point_longitude_latitude(edges=False)
            data = grid.fields[field_name]['data'][level, :, :]

            basemap = display.get_basemap()
            basemap.contour(
                lons, lats, data, contour_values, colors='k',
                linewidths=linewidths, latlon=True)
            ax.set_title(display.generate_grid_title(field_name, level))
        else:
            resolution = prdcfg['gridMapImageConfig'].get('mapres', '110m')
            if resolution not in ('110m', '50m', '10m'):
                warn('Unknown map resolution: '+resolution)
                resolution = '110m'

            display = pyart.graph.GridMapDisplay(grid)
            ax, fig = display.plot_grid_contour(
                field_name, level=level, ax=ax, fig=fig, lat_lines=lat_lines,
                lon_lines=lon_lines, contour_values=contour_values,
                linewidths=linewidths, resolution=resolution,
                map_list=prdcfg['gridMapImageConfig']['maps'])
    else:
        if use_basemap:
            lons, lats = grid.get_point_longitude_latitude(edges=False)
            data = grid.fields[field_name]['data'][level, :, :]

            basemap = display.get_basemap()
            basemap.contour(
                lons, lats, data, contour_values, colors='k',
                linewidths=linewidths, latlon=True)
        else:
            lons, lats = grid.get_point_longitude_latitude(edges=False)
            data = grid.fields[field_name]['data'][level, :, :]

            ax.contour(
                lons, lats, data, contour_values, colors='k',
                linewidths=linewidths)

    if save_fig:
        for fname in fname_list:
            fig.savefig(fname, dpi=dpi)
        plt.close(fig)

        return fname_list

    return (fig, ax)


def plot_latitude_slice(grid, field_name, lon, lat, prdcfg, fname_list):
    """
    plots a latitude slice from gridded data

    Parameters
    ----------
    grid : Grid object
        object containing the gridded data to plot
    field_name : str
        name of the radar field to plot
    lon, lat : float
        coordinates of the slice to plot
    prdcfg : dict
        dictionary containing the product configuration
    fname_list : list of str
        list of names of the files where to store the plot

    Returns
    -------
    fname_list : list of str
        list of names of the created plots

    """
    dpi = 72
    if 'dpi' in prdcfg['rhiImageConfig']:
        dpi = prdcfg['rhiImageConfig']['dpi']

    norm, ticks, ticklabs = get_norm(field_name)

    xsize = prdcfg['rhiImageConfig'].get('xsize', 10.)
    ysize = prdcfg['rhiImageConfig'].get('ysize', 5.)
    xmin = prdcfg['rhiImageConfig'].get('xmin', None)
    xmax = prdcfg['rhiImageConfig'].get('xmax', None)
    ymin = prdcfg['rhiImageConfig'].get('ymin', None)
    ymax = prdcfg['rhiImageConfig'].get('ymax', None)

    fig = plt.figure(figsize=[xsize, ysize], dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    display = pyart.graph.GridMapDisplay(grid)
    display.plot_latitude_slice(
        field_name, lon=lon, lat=lat, norm=norm, colorbar_orient='horizontal',
        ticks=ticks, ticklabs=ticklabs, ax=ax, fig=fig)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    for fname in fname_list:
        fig.savefig(fname, dpi=dpi)
    plt.close(fig)


def plot_longitude_slice(grid, field_name, lon, lat, prdcfg, fname_list):
    """
    plots a longitude slice from gridded data

    Parameters
    ----------
    grid : Grid object
        object containing the gridded data to plot
    field_name : str
        name of the radar field to plot
    lon, lat : float
        coordinates of the slice to plot
    prdcfg : dict
        dictionary containing the product configuration
    fname_list : list of str
        list of names of the files where to store the plot

    Returns
    -------
    fname_list : list of str
        list of names of the created plots

    """
    dpi = 72
    if 'dpi' in prdcfg['rhiImageConfig']:
        dpi = prdcfg['rhiImageConfig']['dpi']

    norm, ticks, ticklabs = get_norm(field_name)

    xsize = prdcfg['rhiImageConfig'].get('xsize', 10.)
    ysize = prdcfg['rhiImageConfig'].get('ysize', 5.)
    xmin = prdcfg['rhiImageConfig'].get('xmin', None)
    xmax = prdcfg['rhiImageConfig'].get('xmax', None)
    ymin = prdcfg['rhiImageConfig'].get('ymin', None)
    ymax = prdcfg['rhiImageConfig'].get('ymax', None)

    fig = plt.figure(figsize=[xsize, ysize], dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    display = pyart.graph.GridMapDisplay(grid)
    display.plot_longitude_slice(
        field_name, lon=lon, lat=lat, norm=norm, colorbar_orient='horizontal',
        ticks=ticks, ticklabs=ticklabs, ax=ax, fig=fig)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    for fname in fname_list:
        fig.savefig(fname, dpi=dpi)
    plt.close(fig)


def plot_latlon_slice(grid, field_name, coord1, coord2, prdcfg, fname_list):
    """
    plots a croos section crossing two points in the grid

    Parameters
    ----------
    grid : Grid object
        object containing the gridded data to plot
    field_name : str
        name of the radar field to plot
    coord1 : tupple of floats
        lat, lon of the first point
    coord2 : tupple of floats
        lat, lon of the second point
    fname_list : list of str
        list of names of the files where to store the plot

    Returns
    -------
    fname_list : list of str
        list of names of the created plots

    """
    dpi = 72
    if 'dpi' in prdcfg['rhiImageConfig']:
        dpi = prdcfg['rhiImageConfig']['dpi']

    norm, ticks, ticklabs = get_norm(field_name)

    xsize = prdcfg['rhiImageConfig'].get('xsize', 10.)
    ysize = prdcfg['rhiImageConfig'].get('ysize', 5.)
    # xmin = prdcfg['rhiImageConfig'].get('xmin', None)
    # xmax = prdcfg['rhiImageConfig'].get('xmax', None)
    # ymin = prdcfg['rhiImageConfig'].get('ymin', None)
    # ymax = prdcfg['rhiImageConfig'].get('ymax', None)

    fig = plt.figure(figsize=[xsize, ysize], dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    display = pyart.graph.GridMapDisplay(grid)
    display.plot_latlon_slice(
        field_name, coord1=coord1, coord2=coord2, norm=norm,
        colorbar_orient='vertical', ticks=ticks, ticklabs=ticklabs, fig=fig,
        ax=ax)
    # ax.set_ylim(
    #    [prdcfg['rhiImageConfig']['ymin'], prdcfg['rhiImageConfig']['ymax']])

    for fname in fname_list:
        fig.savefig(fname, dpi=dpi)
    plt.close(fig)
