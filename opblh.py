import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#######################################################################################################
def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
####################################################################################################################
# function to get value from radar xarray. 
def find_value(Sitelat, Sitelon,xarray,stamp,variable):
    # Sitelat: The latitude list of the timetable
    # Sitelon: The longitude list of the timetable
    # xarray: The converted radar grid file with coordinates assigned
    # Variable: The field want to retrieve
    

    values = []
    n = 0
    m=0
    k=0

    for i in range(len(Sitelat)):
#         progressBar(i,len(Sitelat))
        lat = Sitelat[i]
        lon = Sitelon[i]
        #print(lat, lon)
        # Check i
        try:
            value_location = xarray.sel(latitude = lat,longitude = lon, method='nearest',tolerance=0.25)[variable]
            value = value_location.sel(time=stamp).values
            if value == value:
                n += 1
            else: 
                # na string could exist
                value = None
                k +=1
            values.append(value)
        except:
#             print(lat,lon)
            k +=1
            value=None
            values.append(value)
            
    print("There are %d grid macthed with the ECMWF, %d grid are out of coverage from blh" %(n, k))

    return values

def match_blh(df = "",blh_xr = "", stamp="", variables = ['blh']):
    latlist = list(df['Latitude'])
    lonlist = list(df['Longitude'])
    for var in variables:
        print("retrieving %s values from blh grid file ......" %(var))
        df[var] = find_value(latlist,lonlist,blh_xr,stamp,var)

def plot_2deblh (ds,shape_feature):
    # Plot with shapefile
    fig = plt.figure(figsize=(20,13))
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    ds.blh.plot(cmap=plt.cm.coolwarm)
    plt.savefig("ECWMF_blh.png")
        
        

#########################################################################################################################
# N represents filter non Nexrad values, E means ECMWF values
if __name__ == "__main__":
    base = "/home/xiaohe/Documents"
    fname = os.path.join(base,'NEXRAD/AirNow/US_Boundary/USBoundary.shp')
    shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='none')
    ds = xr.load_dataset(os.path.join(base,'NEXRAD/Model/Operation/era5_US_Land_2020_1_6_1800.grib'), engine='cfgrib')
    match_ecmwf(filter_NG,ECMWF_xr=ds)
    filter_NEG = filter_NG.dropna()

    ## plot emcwf
    plot_2decmwf(ds,shapfeature)