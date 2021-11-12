
from pyproj import Proj



#######################################################################################################
def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
#######################################################################################################

# function to get value from radar xarray. 
def find_value(Sitelat, Sitelon,xarray):
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
    #Convert gcs to pcs beacause Lancover tiff use pcs
    pro = Proj('+proj=aea +lat_0=23 +lon_0=-96 +lat_1=29.5 +lat_2=45.5 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs=True')
    for i in range(len(Sitelat)):
#         progressBar(current,len(Sitelat))
        current+=1
        lat = Sitelat[i]
        lon = Sitelon[i]
        lon,lat = pro(lon,lat)

        #print(lat, lon)
        try:
            value_location = xarray.sel(y = lat,x = lon, method='nearest',tolerance=990)
            value = value_location.values[0]
            if value == value:
                #print(value)
                n += 1
            else:
                k +=1
                value = None
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
    print("There are %d sites macthed with the landcover raster, %d sites are out of coverage from raster" %(n,k))
    #print("----------%d seconds -------" %(time.time()-start))
    return values




########################################################################################################

def match_landcover(AirNow_Radar_df = "",LandCover_xr = "",outname=""):
    
        Sitelat = list(AirNow_Radar_df.loc[:,'Latitude'])
        Sitelon = list(AirNow_Radar_df.loc[:,'Longitude'])

        print("retrieving landcover values from  geotiff file ......")
        AirNow_Radar_df['landcover'] = find_value(Sitelat,Sitelon,LandCover_xr)

#         AirNow_Radar_df.to_csv(os.path.join('Matched',outname))

    #     print("-------%s seconds -------" %(time.time() - start_time))




########################################################################################################

if __name__ == "__main__":
    start_time = time.time()
    da = xr.open_rasterio("LandCover/Reclass_NLCD_Re1kmMajorit.tif")
    match_Pop2AirNow(AirNow_Radar_df = NEXZ01_filter_NEGP,LandCover_xr=da)
    print("-------%s seconds -------" %(time.time() - start_time))