import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from scipy.interpolate import griddata
import os


def modelPredict(time_input, mdl_type,df_model,full_extent,predictors,Mdl,shape_feature):
    df_model["uv10"]= np.sqrt((df_model["u10"]*df_model["u10"]+ df_model["v10"]*df_model["v10"]).tolist())
    df_model["Month"] = 1



    predict_df= df_model.loc[:,predictors]
    predict_df["predictions"]= Mdl.predict(predict_df)
    # predict_in_out = pd.concat([predict_in, predict_out],axis=1)

    predict_out = predict_df["predictions"]


    ### Prediection result visualization

    ## mager the predicted table to the full extend for plotting purpose
    merged = pd.merge(full_extent,predict_out, left_index=True, right_index=True,how="left")

    # plot a table with coordinates columns
    x_flat = merged["Longitude"]
    y_flat = merged["Latitude"]
    arr_flat = merged["predictions"]


    xi = np.linspace(-125,-65,480)
    yi = np.linspace(25,50,330)
    xi,yi = np.meshgrid(xi,yi)
    zi = griddata((x_flat, y_flat),arr_flat, (xi,yi), method='nearest')

    
    
    if not os.path.exists(mdl_type + "EstimatedPM25"):
        os.makedirs(mdl_type + "EstimatedPM25")
    
    data_crs = ccrs.PlateCarree()
    projection_albert=ccrs.AlbersEqualArea(central_longitude=-98.35, central_latitude=39.5)
    fig=plt.figure(figsize=[15,10])
    ax = plt.subplot(projection=projection_albert)
#     ax.set_extent([80, 170, -45, 30])
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    c = ax.pcolor(xi,yi,zi,cmap='jet', vmin=0,vmax=15,transform=data_crs)
    cax = plt.axes([0.93, 0.19, 0.02, 0.62])
    cbar = fig.colorbar(c, cax=cax)
    cbar.ax.tick_params(labelsize=30)
    cbar.set_label('PM2.5(µg/$m^3$)', rotation=270, fontsize=30,labelpad=40, y=0.45)
     
    ax.set_title("PM2.5 Estimation " + time_input,fontsize=35, y=1.0, pad=30)
    plt.savefig(os.path.join(mdl_type+ "EstimatedPM25","PredictedAOD_"+time_input +".png"))
    

#     # Convert ndarray data with regular coords to xarray objects
#     ds_NEXREG = xr.DataArray(zi, coords=[yi[:,1], xi[0]], dims=["lat", "lon"])

#     fig = plt.figure(figsize=[20,13])
#     ax = plt.subplot(projection=ccrs.PlateCarree())
#     ax.add_feature(shape_feature,edgecolor='blue')
#     ax.gridlines(draw_labels=True)
#     ax.coastlines()
#     ds_NEXREG.plot(cmap=plt.cm.coolwarm, x='lon', y='lat')
#     print ("Boundry: %f,%f,%f,%f" %(x_min, x_max, y_min, y_max))
#     plt.savefig("AOD_trim_grid.png")

    merged.to_csv(os.path.join(mdl_type+ "EstimatedPM25","EstimatedPM25"+time_input +".csv"),index=False)
    
    return merged