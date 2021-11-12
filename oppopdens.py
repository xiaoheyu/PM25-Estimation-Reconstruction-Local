import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr

########################################################################################################


# Function to read geotiff
def combinetiff(fn15,fn20,plot="no"):
    da15 = xr.open_rasterio(fn15)
    da20 = xr.open_rasterio(fn20)
#     print("Triming to US extent")
#     usda15 = da15.where(da15.y<50,drop=True).where(da15.y>25,drop=True).where(da15.x>-125,drop=True).where(da15.x<-65,drop=True)
#     usda20 = da20.where(da20.y<50,drop=True).where(da20.y>25,drop=True).where(da20.x>-125,drop=True).where(da20.x<-65,drop=True)
    usda = xr.concat([da15,da20],'year')
#     usda15.rio.to_raster("us_pop15.tif")
#     usda15.rio.to_raster("us_pop20.tif")
    if plot =="yes":
#         fig = plt.figure(figsize=(16,8))
#         ax = fig.add_subplot(111)
#         im =ax.imshow(usda15.variable.data[0],vmin=-10,vmax=100)
#         plt.colorbar(im)
#         plt.show()
#         plt.savefig("Popden2015")
        
        fig = plt.figure(figsize=(16,8))
        ax = fig.add_subplot(111)
        im =ax.imshow(da20.variable.data[0],vmin=-10,vmax=100)
        plt.colorbar(im)
        plt.show()
        plt.savefig("Popden2020")
    return usda
#######################################################################################################
def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
########################################################################################################
# function to get value from radar xarray. 
def find_value(Sitelat, Sitelon,xarray,year):
    # Sitelat: The latitude list of the timetable
    # Sitelon: The longitude list of the timetale
    # xarray: The converted radar grid file with coordinates assigned
    # Variable: The field want to retrieve
    
    #start = time.time()
    values = []
    n = 0
    m=0
    k=0
    current=1
    if year in ['2022','2021','2020','2019','2018']:
        year=1
    elif year in ['2014','2015','2016','2017']:
        year=0
    else:
        print(year+"beyond range")
    for i in range(len(Sitelat)):
#         progressBar(current,len(Sitelat))
        current+=1
        lat = Sitelat[i]
        lon = Sitelon[i]
        #print(lat, lon)
        try:
            value_location = xarray.sel(y = lat,x = lon, method='nearest',tolerance=0.01)
            value = value_location.sel(year=year).values[0]
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
    print("There are %d sites macthed with the population density raster, %d sites are out of coverage" %(n,k))
    #print("----------%d seconds -------" %(time.time()-start))
    return values




########################################################################################################

def match_popdens(AirNow_Radar_df = "",POPDEN_xr = "", year='2020'):
    AirNow_Radar_df['YEAR'] = year
    Sitelat = list(AirNow_Radar_df.loc[AirNow_Radar_df['YEAR'] == year,'Latitude'])
    Sitelon = list(AirNow_Radar_df.loc[AirNow_Radar_df['YEAR'] == year,'Longitude'])

    print("retrieving population density values in %s from CEDAC geotiff file ......" %(year))
    AirNow_Radar_df.loc[AirNow_Radar_df['YEAR'] == year, 'popden'] = find_value(Sitelat,Sitelon,POPDEN_xr,year)

#     AirNow_Radar_df.to_csv(os.path.join('Matched',outname))

    #     print("-------%s seconds -------" %(time.time() - start_time))





########################################################################################################
if __name__ == "__main__":
    start_time = time.time()
    usda = combinetiff("PopDens/us_pop15.tif",
                      "PopDens/us_pop20.tif")
    #only support pop from 15 to 23
    match_pop(AirNow_Radar_df = NEXZ01_filter_NEG,POPDEN_xr=usda, year="2020")
    print("-------%s seconds -------" %(time.time() - start_time))

    ## plot pop dens tif
    da20 = xr.open_rasterio("PopDens/us_pop20.tif")
    fig = plt.figure(figsize=(20,13))
    ax = fig.add_subplot(111)
    im =ax.imshow(da20.variable.data[0],vmin=0,vmax=100)
    plt.colorbar(im)
    plt.show()
    plt.savefig("Popden2020")