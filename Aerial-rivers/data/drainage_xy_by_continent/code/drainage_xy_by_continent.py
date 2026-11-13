"""One drainage curve per target cell -> (x, y) points, split by continent, saved as CSV.

x = area_at_level  : smallest upwind area (km2) delivering cumulative share y of the cell's rain
y = level          : cumulative share C of the rain (0.005 .. 0.995)
Two source masks: 'all' (drainage_curves_allsources.nc) and 'land' (drainage_curves_land.nc).
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "raw_nc_data"
OUT = ROOT / "divided_data"
OUT.mkdir(exist_ok=True)

FILES = {"all": "drainage_curves_allsources.nc", "land": "drainage_curves_land.nc"}
CN = {"South America": "南美洲", "North America": "北美洲", "Africa": "非洲",
      "Asia": "亞洲", "Oceania": "大洋洲", "Europe": "歐洲"}

shp = Path.home() / ".local/share/cartopy/shapefiles/natural_earth/cultural/ne_50m_admin_0_countries.shp"
world = gpd.read_file(shp)[["NAME", "CONTINENT", "geometry"]]
world = world[world.CONTINENT.isin(CN)].copy()

# Natural Earth puts all of Russia in Europe; the part east of 60E goes to Asia.
ru = world[world.NAME == "Russia"].geometry.iloc[0]
world = world[world.NAME != "Russia"]
world = pd.concat([world, gpd.GeoDataFrame(
    {"NAME": ["Russia", "Russia"], "CONTINENT": ["Europe", "Asia"],
     "geometry": [ru.intersection(box(-190, -90, 60, 90)), ru.intersection(box(60, -90, 190, 90))]},
    crs=world.crs)], ignore_index=True)


def classify(lon, lat):
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon, lat), crs=world.crs)
    j = gpd.sjoin(pts, world[["CONTINENT", "geometry"]], how="left", predicate="within")
    cont = j[~j.index.duplicated()]["CONTINENT"].copy()
    miss = cont.isna()
    if miss.any():  # coastal cells just offshore -> nearest continent
        near = gpd.sjoin_nearest(pts[miss.values], world[["CONTINENT", "geometry"]], how="left")
        cont[miss] = near[~near.index.duplicated()]["CONTINENT"]
    cont = cont.to_numpy()
    # Natural Earth's France/Spain polygons carry overseas parts (French Guiana, Antilles, Canaries,
    # Madeira) labelled Europe; give those cells to the continent they actually sit on.
    eu = cont == "Europe"
    cont[eu & (lon < -30) & (lat < 8)] = "South America"
    cont[eu & (lon < -50) & (lat >= 8)] = "North America"
    cont[eu & (lon >= -30) & (lon < 0) & (lat < 34)] = "Africa"
    return cont


cont = None
for mask, fname in FILES.items():
    ds = xr.open_dataset(RAW / fname)
    lat, lon = ds.tag_lat.values, ds.tag_lon.values
    if cont is None:
        cont = classify(((lon + 180) % 360) - 180, lat)
    area = ds.area_at_level.values            # (cell, level) km2
    level = ds.level.values                   # (level,)
    cells = ds.cell.values
    n = len(level)
    for en, zh in CN.items():
        idx = np.flatnonzero(cont == en)
        df = pd.DataFrame({
            "cell": np.repeat(cells[idx], n),
            "tag_lat": np.repeat(lat[idx], n),
            "tag_lon": np.repeat(lon[idx], n),
            "x_area_km2": area[idx].ravel(),
            "y_cum_share": np.tile(level, len(idx)),
        })
        p = OUT / f"drainage_xy_{mask}_{zh}.csv"
        df.to_csv(p, index=False, float_format="%.6g")
        print(p.name, len(idx), "cells,", len(df), "rows", flush=True)
