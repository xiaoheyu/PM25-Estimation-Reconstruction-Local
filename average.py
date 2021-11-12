import pandas as pd
import glob
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from scipy.interpolate import griddata
import os


fname = "US_Boundary/USBoundary.shp"

shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='none')




path_list = sorted(glob.glob("nonexEstimatedPM25/Estimated*.csv"))

file_list = []
for i in path_list:
    file_list.append(os.path.basename(i))

time_list = []
for i in file_list:
    time_list.append(i[13:30])

day_list = []
for i in time_list:
    day_list.append(i.split("T")[0])

day_list = sorted(set(day_list))

###############################################################################
for i in day_list:  # iterate day stamps
    print("plotting" + i)
    df_mean = pd.DataFrame()
    matching = [p for p in path_list if i in p] # find hour stamps for a day
    for idx,j in enumerate(matching):
        print("averging:   " + j)
        n=len(matching)
        df = pd.read_csv(j)
        if len(df_mean) !=0:
            df_mean["prediction"+str(idx+1)] = df["predictions"]
        else:
            df_mean = df
    if n == 1:
        df_mean["daymean"] = df_mean.iloc[:,3]
    else:
        df_mean["daymean"] = df_mean.iloc[:, 3:-1].mean(axis=1)

    
        # plot a table with coordinates columns
    x_flat = df_mean["Longitude"]
    y_flat = df_mean["Latitude"]
    arr_flat = df_mean["daymean"]


    xi = np.linspace(-125,-65,480)
    yi = np.linspace(25,50,330)
    xi,yi = np.meshgrid(xi,yi)
    zi = griddata((x_flat, y_flat),arr_flat, (xi,yi), method='nearest')



    if not os.path.exists("day_EstimatedPM25"):
        os.makedirs("day_EstimatedPM25")

    fig=plt.figure(figsize=[20,13])
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    c = ax.pcolor(xi,yi,zi,cmap='jet', vmin=0,vmax=15)
    cax = plt.axes([0.90, 0.252, 0.02,0.5 ])
    fig.colorbar(c, cax=cax)
    ax.set_title("PM2.5 Estimation " + i,fontsize=25, y=1.0, pad=20)

    plt.savefig(os.path.join("day_EstimatedPM25","day_EstimatedPM25_"+ i +".png"))
    
    df_mean.loc[:,["Latitude","Longitude","daymean"]].to_csv(os.path.join("day_EstimatedPM25","day_EstimatedPM25_"+ i +".csv"),index=False)
    
##################################

mon_list = []
for i in time_list:
    mon_list.append(i.split("T")[0][0:7])

mon_list = sorted(set(mon_list))
mon_list


for i in mon_list:  # iterate day stamps
    print("plotting" + i)
    df_mean = pd.DataFrame()
    matching = [p for p in path_list if i in p] # find hour stamps for a day
    for idx,j in enumerate(matching):
        print("averaging:  " + j)
        n=len(matching)
        df = pd.read_csv(j)
        if len(df_mean) !=0:
            df_mean["prediction"+str(idx+1)] = df["predictions"]
        else:
            df_mean = df
    if n == 1:
        df_mean["monmean"] = df_mean.iloc[:,3]
    else:
        df_mean["monmean"] = df_mean.iloc[:, 3:-1].mean(axis=1)

    
        # plot a table with coordinates columns
    x_flat = df_mean["Longitude"]
    y_flat = df_mean["Latitude"]
    arr_flat = df_mean["monmean"]


    xi = np.linspace(-125,-65,480)
    yi = np.linspace(25,50,330)
    xi,yi = np.meshgrid(xi,yi)
    zi = griddata((x_flat, y_flat),arr_flat, (xi,yi), method='nearest')



    if not os.path.exists("mon_EstimatedPM25"):
        os.makedirs("mon_EstimatedPM25")

    fig=plt.figure(figsize=[20,13])
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    c = ax.pcolor(xi,yi,zi,cmap='jet', vmin=0,vmax=15)
    cax = plt.axes([0.90, 0.252, 0.02,0.5 ])
    fig.colorbar(c, cax=cax)
    ax.set_title("PM2.5 Estimation " + i,fontsize=25, y=1.0, pad=20)

    plt.savefig(os.path.join("mon_EstimatedPM25","mon_EstimatedPM25_"+ i +".png"))
    
    df_mean.loc[:,["Latitude","Longitude","monmean"]].to_csv(os.path.join("mon_EstimatedPM25","mon_EstimatedPM25_"+ i +".csv"),index=False)
    
    
