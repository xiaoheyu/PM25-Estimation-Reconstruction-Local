

#######################################################################################################
def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')




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
            value_location = xarray.sel(y = lat,x = lon, method='nearest',tolerance=0.005)
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
    print("There are %d sites matched with the raster, %d sites are out of coverage" %(n,k))
    #print("----------%d seconds -------" %(time.time()-start))
    return values




########################################################################################################

def match_lith4(AirNow_Radar_df = "",xr = ""):
    
    Sitelat = list(AirNow_Radar_df.loc[:,'Latitude'])
    Sitelon = list(AirNow_Radar_df.loc[:,'Longitude'])

    print("retrieving lith4 from  geotiff file ......")
    AirNow_Radar_df['lith4'] = find_value(Sitelat,Sitelon,xr)

#         AirNow_Radar_df.to_csv(os.path.join('Matched',outname))

    #     print("-------%s seconds -------" %(time.time() - start_time))




########################################################################################################

if __name__ == "__main__":
    star_time = time.time()
    da = xr.open_rasterio("Lithology4Class/fullareagmnarocktypedecde.tif")
    match_lith4(AirNow_Radar_df = NEXZ01_filter_NEGPLSG,xr=da)
    print("-------%s seconds -------" %(time.time() - start_time))