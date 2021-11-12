from datetime import datetime
import os
import glob
import xarray as xr
from pyproj import Proj
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from scipy.interpolate import griddata

## Starting from the AOD, use AOD as the base resolution. 

def opaod_base(time_input,ds_GOES,plotvar="yes",shape_feature=""):

## convert GOES projection to gcs
    sat_sweep =  ds_GOES.variables['goes_imager_projection'].attrs["sweep_angle_axis"]
    sat_h = ds_GOES.variables['goes_imager_projection'].attrs["perspective_point_height"]
    ds_GOES.variables['goes_imager_projection'].attrs["longitude_of_projection_origin"]
    pro = Proj("+proj=geos +lon_0=-75 +h=35786023 + x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs=True") 
    # proj=Proj(proj='geos', h=35786023, lon_0=-75,sweep=sat_sweep)
#     z = ds_GOES.AOD.data
    # z_flag = np.where((ds_GOES.variables['DQF'].data == 2.0), np.nan, ds_GOES.variables['AOD'].data) # flag filter

    xx_goes, yy_goes = np.meshgrid(ds_GOES.x.data*sat_h, ds_GOES.y.data*sat_h)
    lons, lats = pro(xx_goes, yy_goes, inverse=True)

## trim to US extent to  
    x_flat = lons.flatten()
    y_flat = lats.flatten()
    x_flat[x_flat<-125] = None
    x_flat[x_flat>-65] = None
    y_flat[y_flat>50] = None
    y_flat[y_flat<25] = None

    trimed = pd.DataFrame()
    trimed["Latitude"] = y_flat
    trimed["Longitude"] = x_flat

    arr_AOD = ds_GOES["AOD"].data
    arr_DQF = ds_GOES["DQF"].data
    arr_AOD_flat = arr_AOD.flatten()
    arr_DQF_flat = arr_DQF.flatten()

    trimed["AOD"] = arr_AOD_flat
    trimed["DQF"] = arr_DQF_flat

## filter out None values which are outside US
    trimed_drop = trimed.dropna(subset=["Latitude"])
    trimed_drop = trimed_drop.dropna(subset=["Longitude"])
## 10km grid which is the same as nexrad extent
    xi = np.linspace(-125,-65,480)
    yi = np.linspace(25,50,330)
    xi,yi = np.meshgrid(xi,yi)

    GOES = pd.DataFrame()
    GOES["Latitude"] = yi.flatten()
    GOES["Longitude"] = xi.flatten()

    start_time = time.time()

    arr_flat_AOD = trimed_drop["AOD"]
    arr_flat_DQF = trimed_drop["DQF"]
## resample from 2km resolution to 10km resolution
    zi_AOD = griddata((trimed_drop["Longitude"], trimed_drop["Latitude"]),arr_flat_AOD, (xi,yi), method='nearest')
    zi_DQF = griddata((trimed_drop["Longitude"], trimed_drop["Latitude"]),arr_flat_DQF, (xi,yi), method='nearest')

    GOES["AOD"] = zi_AOD.flatten()
    GOES["DQF"] = zi_DQF.flatten()
    print("-------%s seconds -------" %(time.time() - start_time))

        
    if not os.path.exists("plots"):
        os.makedirs("plots")

    if plotvar !="no":
        fig=plt.figure(figsize=[20,13])
        ax = plt.subplot(projection=ccrs.PlateCarree())
        ax.add_feature(shape_feature,edgecolor='blue')
        ax.gridlines(draw_labels=True)
        ax.coastlines()
        c = ax.pcolor(xi,yi,zi_AOD,cmap='Reds',vmin=0,vmax=4)
        fig.colorbar(c, ax=ax,location="bottom")
        plt.savefig(os.path.join("plots","AOD_"+time_input +".png"))
        
        fig=plt.figure(figsize=[20,13])
        ax = plt.subplot(projection=ccrs.PlateCarree())
        ax.add_feature(shape_feature,edgecolor='blue')
        ax.gridlines(draw_labels=True)
        ax.coastlines()
        c = ax.pcolor(xi,yi,zi_DQF,cmap='coolwarm',vmin=0,vmax=3)
        fig.colorbar(c, ax=ax,location="bottom")
        plt.savefig(os.path.join("plots","DQF_"+time_input +".png"))
        
        
    return GOES
        
        
        
        
        
        
# ## alternative plot methods with xarray object
# # Convert ndarray data with regular coords to xarray objects
# ds_NEXREG = xr.DataArray(zi_AOD, coords=[yi[:,1], xi[0]], dims=["lat", "lon"])

# fig = plt.figure(figsize=[20,13])
# ax = plt.subplot(projection=ccrs.PlateCarree())
# ax.add_feature(shape_feature,edgecolor='blue')
# ax.gridlines(draw_labels=True)
# ax.coastlines()
# ds_NEXREG.plot(cmap=plt.cm.Reds, vmin=0,vmax=3, x='lon', y='lat')
# # print ("Boundry: %f,%f,%f,%f" %(x_min, x_max, y_min, y_max))
# # plt.savefig("2017-01-25" + var +".png")