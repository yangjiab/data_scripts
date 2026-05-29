import os
import sys
os.chdir(sys.path[0])
import geopandas as gpd
import rasterio
import re
from tqdm import tqdm
import numpy as np
from rasterio.windows import from_bounds
import pyproj
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling


def sample_with_buffer_wgs84(src, geom, buffer_m=1000):
    import numpy as np
    from rasterio.windows import from_bounds

    lon, lat = geom.x, geom.y

    lat_deg = buffer_m / 111320
    lon_deg = buffer_m / (111320 * np.cos(np.deg2rad(lat)))

    minx = lon - lon_deg
    maxx = lon + lon_deg
    miny = lat - lat_deg
    maxy = lat + lat_deg

    try:
        window = from_bounds(minx, miny, maxx, maxy, src.transform)
        data = src.read(1, window=window)

        if src.nodata is not None:
            data = data[data != src.nodata]

        if data.size == 0:
            return 0

        return 1 if np.any(data == 1) else 0

    except:
        return 0

def extract_year(filename):
    match = re.search(r'(\d{4})', filename)
    return int(match.group(1)) if match else None

