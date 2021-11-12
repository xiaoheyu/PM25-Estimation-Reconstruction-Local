import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def opnexrad(grid, shape_feature, plotvar="reflectivity"):
    xx = grid.get_point_longitude_latitude(1)[0]
    yy = grid.get_point_longitude_latitude(1)[1]
    # Convert grid to xarray object
    ds_NEXRADgrid = grid.to_xarray()
    # Assign coordinates with irregular 2D cooridnates
    # assigned lat, lon are not dimension variables, thus only where query supported. sel Does not support
    ds_NEXRADxy = ds_NEXRADgrid.assign_coords({"lon": (["y", "x"], xx)})
    ds_NEXRADxy = ds_NEXRADxy.assign_coords({"lat": (["y", "x"], yy)})
    # Filter evelvatiuons, only keep ground and 1km
    ds_NEXRADxy01 = ds_NEXRADxy.isel(z=[0,1])
    # get the composite layer
    arrs = ds_NEXRADxy01.max(dim="z")
    # set variable list
    vars = [ 'reflectivity', 'velocity',
           'spectrum_width', 'differential_phase',
           'differential_reflectivity', 'cross_correlation_ratio']


    # convert 2d coordiate and values to table
    NEXZ01 = pd.DataFrame()
    for var in vars:
        arr = arrs[var].data
        arr_flat = arr.flatten()
        x_flat = xx.flatten()
        y_flat = yy.flatten()
        NEXZ01["Latitude"] = y_flat
        NEXZ01["Longitude"] = x_flat
        NEXZ01["z01"+var] = arr_flat

    full_extent = NEXZ01[["Latitude","Longitude"]]
    
    if plotvar != "no":
        ## NEX plot with xarray object
        fig = plt.figure(figsize=(20,13))
        ax = plt.subplot(111,projection=ccrs.PlateCarree())
        ax.add_feature(shape_feature,edgecolor='blue')
        ax.gridlines(draw_labels=True)
        ax.coastlines()
        arrs[plotvar].plot(cmap=plt.cm.coolwarm, x='lon', y='lat')
        plt.savefig(plotvar+".png")
    return NEXZ01, full_extent