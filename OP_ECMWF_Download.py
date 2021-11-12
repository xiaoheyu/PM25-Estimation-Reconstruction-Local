import cdsapi
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import time
import os

from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import numpy as np

###############################################################################################################################




def download_ECMWF(UTC_input):
    UTC_format = '%Y-%m-%dT%H:%M'
    dt_object = datetime.strptime(UTC_input,UTC_format)
    year = datetime.strftime(dt_object, "%Y")
    month = datetime.strftime(dt_object, "%m")
    day = datetime.strftime(dt_object, "%d")
    hour = datetime.strftime(dt_object, "%H:00")
    
    if not os.path.exists("ECMWF"):
        os.makedirs("ECMWF")

    out_fn = os.path.join("ECMWF",'era5_US_Land_' + UTC_input+'.grib')
    
    c = cdsapi.Client()

    data = c.retrieve(
        'reanalysis-era5-land',
        {
            'product_type': 'reanalysis',
        'variable': [
             '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
            '2m_temperature', 'leaf_area_index_high_vegetation','leaf_area_index_low_vegetation',
             'surface_pressure', 'surface_runoff', 'total_precipitation',
        ],

            'year': year,
            'month': [month],
            'day': [
             day,
        ],
            'time': [

            hour,

        ],
            'format': 'grib',                 # Supported format: grib and netcdf. Default: grib
#             'area'          : [36.9, -106.8, 25.74, -92.91,], # North, West, South, East.          Default: global
            'area'          : [50, -125, 25, -65,], #US
#            'area'          : [38, -107, 25, -91,], ## TX
#             'area'          : [43, -125, 32, -113,], ## CA
            'grid'          : [0.1, 0.1],       # Latitude/longitude grid.           Default: 0.25 x 0.25
        },
        os.path.join("ECMWF",'era5_US_Land_' + UTC_input+'.grib'))# Output file. Adapt as you wish.

    return out_fn
#########################################################################################################################
if __name__ == "__main__":
    download_ECMWF()