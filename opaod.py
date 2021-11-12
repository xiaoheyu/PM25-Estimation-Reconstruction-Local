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
from mpl_toolkits.axes_grid1 import make_axes_locatable


#######################################################################################################
def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
#######################################################################################################
def read_goesnc2xr(path):
    ds = xr.open_dataset(path,decode_times=False)
    sat_h = ds.variables['goes_imager_projection'].attrs["perspective_point_height"]

    # Assign coordinates
    xrcor = ds.assign_coords(x=(ds.x)*sat_h,y=(ds.y)*sat_h)
    return sat_h, xrcor




# function to get value from radar xarray. 
def find_value(Sitelat, Sitelon,xarray,sat_h,var):
    # Sitelat: The latitude list of the timetable
    # Sitelon: The longitude list of the timetale
    # xarray: The AOD nc file
    # Var: The field want to retrieve  

    #start = time.time()
    values = []
    n = 0
    m=0
    k=0


    #Convert gcs to pcs 
    pro = Proj("+proj=geos +lon_0=-75 +h=" +str(round(sat_h)) + " +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs=True") 
    for i in range(len(Sitelat)):
#         progressBar(i, len(Sitelat))
        lat = Sitelat[i]
        lon = Sitelon[i]
        lon,lat = pro(lon,lat)

        #print(lat, lon)
        try:
            value_location = xarray.sel(y = lat,x = lon, method='nearest',tolerance=2000)
            value = value_location[var].data
            if value == value:
                #print(value)
                n += 1
            else:
                value = None
                k +=1
            values.append(value)
        except:
            k +=1
            value=None
            values.append(value)
#     try:
#         for i in xarray.sel(year=year).data:
#             for j in i:
#                 if j == j:
#                     m += 1
#     except:
#         print("%s does not exist" %(stamp))
    #print(np.unique(values))
    print("There are %d sites matched with the current data file, %d sites are out of coverage" %(n,k))
    #print("----------%d seconds -------" %(time.time()-start))
    return values


def match_goes(df = "",stamp = '',vars = ['AOD','DQF']):
    missing_file = 0
    missing_stamp =[]
    UTC_format = '%Y-%m-%dT%H:%M'
    #Serching will all modes
    aodfn_prefix= "OR_ABI-L2-AODC-*_G16_s"
    aodfolder_prefix = "noaa-goes16/ABI-L2-AODC/"

    dt_object = datetime.strptime(stamp,UTC_format)
    aod_timepath = datetime.strftime(dt_object, "%Y/%j/%H/")
    aod_fn = datetime.strftime(dt_object, aodfn_prefix + "%Y%j%H")
    mins = "3"
    aod_searchpath = os.path.join(aodfolder_prefix,aod_timepath,aod_fn + mins + '*')
#         print(aod_searchpath)
    nc_path =  glob.glob(aod_searchpath)
    if nc_path:
        nc_path = nc_path
    else:
        aod_searchpath = os.path.join(aodfolder_prefix,aod_timepath,aod_fn + '*')
        nc_path = glob.glob(aod_searchpath)
#         print(nc_path)
    if nc_path:
        try:
        # Select file from lst, if more than one exist, select the first one which is closest to **:30 the mid time of an hour
            nc_path = nc_path[0]
            print("===========================================================>")
            print("%s has been found " %(nc_path))
            print("Reading ......")
            sat_h, xrcor = read_goesnc2xr(nc_path)
            print("Grid successfully read")

            Sitelat = list(df['Latitude'])
            Sitelon = list(df['Longitude'])
            for var in vars:
                print("retrieving %s values" %(var))
                df[var] = find_value(Sitelat,Sitelon,xrcor,sat_h,var)
        except:
                missing_file +=1
                missing_stamp.append(aod_searchpath)
    else:
        missing_file +=1
        missing_stamp.append(aod_searchpath)
    print("The are %d timestamps faild to find files" %(missing_file))
#     print(missing_stamp)
    return nc_path

#     df.to_csv(os.path.join('Matched',saveName))
########################################################################################################



def aod_plot(nc_path,shape_feature,plotvar):
        ## plot GOES
    start_time = time.time()
    ds_GOES = xr.open_dataset(nc_path,decode_times=False)


    sat_sweep =  ds_GOES.variables['goes_imager_projection'].attrs["sweep_angle_axis"]
    sat_h = ds_GOES.variables['goes_imager_projection'].attrs["perspective_point_height"]
    ds_GOES.variables['goes_imager_projection'].attrs["longitude_of_projection_origin"]
    pro = Proj("+proj=geos +lon_0=-75 +h=35786023 + x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs=True") 
    # proj=Proj(proj='geos', h=35786023, lon_0=-75,sweep=sat_sweep)
    if plotvar == "AOD":
        z = ds_GOES.AOD.data
    elif plotvar == "DQF":
        z = ds_GOES.DQF.data

    # z_flag = np.where((ds_GOES.variables['DQF'].data == 2.0), np.nan, ds_GOES.variables['AOD'].data) # flag filter

    xx_goes, yy_goes = np.meshgrid(ds_GOES.x.data*sat_h, ds_GOES.y.data*sat_h)
    lons, lats = pro(xx_goes, yy_goes, inverse=True)
    fig=plt.figure(figsize=[20,13])
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    c = ax.pcolor(lons,lats,z,cmap='Reds',vmin=0,vmax=3)
    plt.colorbar(c, ax=ax)
    plt.savefig(plotvar + ".png")
    print("-------%s seconds -------" %(time.time() - start_time))



    