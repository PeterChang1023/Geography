"""Map of the six-continent split of the target cells (reads divided_data/, writes Figures/)."""
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
plt.rcParams["font.sans-serif"] = ["PingFang TC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
ROOT = HERE.parent
SRC = ROOT / "divided_data"
FIG = ROOT / "Figures"
CONT = {"南美洲": ("South America", "#e6862b"), "北美洲": ("North America", "#3b7dd8"),
        "非洲": ("Africa", "#c8a415"), "亞洲": ("Asia", "#d1495b"),
        "大洋洲": ("Oceania", "#2a9d8f"), "歐洲": ("Europe", "#7b4fb3")}

fig = plt.figure(figsize=(15, 6.5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-175, 180, -60, 65], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="#f2f2f2")
ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
rows = []
for zh, (en, col) in CONT.items():
    d = pd.read_csv(SRC / f"drainage_xy_all_{zh}.csv", usecols=["cell", "tag_lat", "tag_lon"]).drop_duplicates("cell")
    ax.scatter(d.tag_lon, d.tag_lat, s=0.6, color=col, transform=ccrs.PlateCarree(), label=f"{en} ({zh}): {len(d):,} cells")
    rows.append((zh, en, len(d), d.tag_lat.min(), d.tag_lat.max(), d.tag_lon.min(), d.tag_lon.max()))
ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.5, dms=False)
ax.legend(loc="lower left", markerscale=12, fontsize=9, frameon=True)
ax.set_title("Target cells split into six continents (0.25° cells, 60°S–60°N)")
fig.savefig(FIG / "continent_split_map.png", dpi=170, bbox_inches="tight")
pd.DataFrame(rows, columns=["zh", "en", "cells", "lat_min", "lat_max", "lon_min", "lon_max"]).to_csv(
    FIG / "continent_split_ranges.csv", index=False)
print(pd.DataFrame(rows))
