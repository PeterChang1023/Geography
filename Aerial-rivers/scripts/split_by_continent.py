"""Split the data/ .nc files by continent (using tag_lat/tag_lon) and save CSVs."""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import box

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "by_continent"
OUT.mkdir(exist_ok=True)

CN = {"South America": "南美洲", "North America": "北美洲", "Africa": "非洲",
      "Asia": "亞洲", "Oceania": "大洋洲", "Europe": "歐洲"}

shp = Path.home() / ".local/share/cartopy/shapefiles/natural_earth/cultural/ne_50m_admin_0_countries.shp"
world = gpd.read_file(shp)[["NAME", "CONTINENT", "geometry"]]
world = world[world.CONTINENT.isin(CN)].copy()

# Natural Earth puts all of Russia in Europe; move the part east of the Urals (60E) to Asia.
ru = world[world.NAME == "Russia"].geometry.iloc[0]
asia_ru = ru.intersection(box(60, -90, 190, 90))
eu_ru = ru.intersection(box(-190, -90, 60, 90))
world = world[world.NAME != "Russia"]
world = pd.concat([world, gpd.GeoDataFrame(
    {"NAME": ["Russia", "Russia"], "CONTINENT": ["Europe", "Asia"], "geometry": [eu_ru, asia_ru]},
    crs=world.crs)], ignore_index=True)


def classify(lon, lat):
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon, lat), crs=world.crs)
    j = gpd.sjoin(pts, world[["CONTINENT", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    cont = j["CONTINENT"].copy()
    miss = cont.isna()
    if miss.any():  # coastal cells that fall just offshore -> nearest continent polygon
        near = gpd.sjoin_nearest(pts[miss.values], world[["CONTINENT", "geometry"]], how="left")
        near = near[~near.index.duplicated()]
        cont[miss] = near["CONTINENT"]
    return cont.to_numpy()


for f in ["distance_curves_all", "drainage_curves_allsources", "drainage_curves_land"]:
    ds = xr.open_dataset(DATA / f"{f}.nc")
    lon = ((ds.tag_lon.values + 180) % 360) - 180
    lat = ds.tag_lat.values
    cont = classify(lon, lat)

    # tidy table: per-cell scalars + the curve as one column per x / level
    scalars = [v for v in ds.data_vars if ds[v].dims == ("cell",)]
    df = pd.DataFrame({v: ds[v].values for v in scalars}, index=ds.cell.values)
    df.index.name = "cell"
    if "mask" in ds.coords:  # scalar coordinate, keep it as a column
        df.insert(0, "mask", str(ds["mask"].values))
    curve_var = "profile" if "profile" in ds else "area_at_level"
    dim = ds[curve_var].dims[1]
    cols = [f"{curve_var}_{dim}{c:g}" for c in ds[dim].values]
    curve = pd.DataFrame(ds[curve_var].values, index=df.index, columns=cols)
    df = pd.concat([df, curve], axis=1)
    df["continent"] = cont

    for en, zh in CN.items():
        sub = df[df.continent == en].drop(columns="continent")
        p = OUT / f"{f}_{zh}.csv"
        sub.to_csv(p)
        print(f"{p.name}: {len(sub)} cells")
    print(f, "total", len(df), "unclassified", df.continent.isna().sum())
