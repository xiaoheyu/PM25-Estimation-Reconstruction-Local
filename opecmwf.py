import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime
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
            value_location = xarray.sel(latitude = lat,longitude = lon, method='nearest',tolerance=0.1)[variable]
            if stamp.split("T")[1] != "00:00":
                value = value_location.sel(time=stamp.split("T")[0],step=str(stamp.split("T")[1] + ":00")).values
            else:
                date_time_obj =datetime.datetime.strptime(stamp.split("T")[0], '%Y-%m-%d')- datetime.timedelta(days=1)
                value = value_location.sel(time=date_time_obj.strftime('%Y-%m-%d'),step="24:00:00").values
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
            
    print("There are %d grid macthed with the ECMWF, %d grid are out of coverage from ECMWF" %(n, k))

    return values

def match_ecmwf(df = "",ECMWF_xr = "",stamp="", variables = ['u10','v10','d2m','t2m' ,'lai_hv','lai_lv','sp','sro','tp']):
    latlist = list(df['Latitude'])
    lonlist = list(df['Longitude'])
    for var in variables:
        print("retrieving %s values from ECMWF grid file ......" %(var))
        df[var] = find_value(latlist,lonlist,ECMWF_xr,stamp,var)

def plot_2decmwf (ds,shape_feature):
    # Plot with shapefile
    fig = plt.figure(figsize=(20,13))
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.add_feature(shape_feature,edgecolor='blue')
    ax.gridlines(draw_labels=True)
    (ds.t2m[16][21]-275).plot(cmap=plt.cm.coolwarm)
    plt.savefig("ECWMF_tmp.png")
        
        

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