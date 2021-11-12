
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

    for i in range(len(Sitelat)):
#         progressBar(current,len(Sitelat))
        current+=1
        lat = Sitelat[i]
        lon = Sitelon[i]
        #print(lat, lon)
        try:
            value_location = xarray.sel(y = lat,x = lon, method='nearest',tolerance=0.03)
            value = value_location.values[0]
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
    print("There are %d sites macthed with the landcover raster, %d sites are out of coverage from Radar" %(n,k))
    #print("----------%d seconds -------" %(time.time()-start))
    return values




########################################################################################################

def match_soil(AirNow_Radar_df = "",Soil_xr = ""):
    
        Sitelat = list(AirNow_Radar_df.loc[:,'Latitude'])
        Sitelon = list(AirNow_Radar_df.loc[:,'Longitude'])

        print("retrieving soil values from  geotiff file ......")
        AirNow_Radar_df['soil'] = find_value(Sitelat,Sitelon,Soil_xr)

#         AirNow_Radar_df.to_csv(os.path.join('Matched',outname))

    #     print("-------%s seconds -------" %(time.time() - start_time))




########################################################################################################

if __name__ == "__main__":
    start_time = time.time()
    da = xr.open_rasterio("Soil/so2015v2.tif")
    print("Triming to US extent")
    da = da.where(da.y<50,drop=True).where(da.y>25,drop=True).where(da.x>-125,drop=True).where(da.x<-65,drop=True)
    match_Pop2AirNow(AirNow_Radar_df = NEXZ01_filter_NEGPL,Soil_xr=da)
    print("-------%s seconds -------" %(time.time() - start_time))