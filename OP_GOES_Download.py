# Brian Blaylock
# Requres `s3fs`
# Website: https://s3fs.readthedocs.io/en/latest/
# In Anaconda, download via conda-forge.

import s3fs
import os
from datetime import datetime

def download_goes(utc="2020-01-06T18:00"):
    # Convert UTC time to day of the year
    UTC_format = '%Y-%m-%dT%H:%M'
    dt_object = datetime.strptime(utc,UTC_format)
    aod_timepath = datetime.strftime(dt_object, "%Y/%j/%H/*")

    # Use the anonymous credentials to access public data
    fs = s3fs.S3FileSystem(anon=True)

    # # List contents of GOES-16 bucket.
    files= fs.glob(os.path.join('noaa-goes16/ABI-L2-AODC',aod_timepath))
    out_dir = os.path.dirname(files[0])
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for i in range(len(files)):
        fs.get(files[i],files[i])
        
    return out_dir
if __name__ == "__main__":
    download_goes()