# Land-cover experiments over the FRONT moisture-source region (forest and desert)

Two MATSIRO land-surface experiments. Both change the **same 110 T42 grid cells** (about 2.8°): the moisture-source region of
Mongolia's FRONT zone (inside the red line), without Mongolia's DES zone (green line). Each experiment changes the land-cover class
(`gridx01`) and the LAI (`grlai01`, `grlai02`) in those cells; everything else is identical to the original input files.

| Experiment | `gridx01` in the 110 cells | LAI (`grlai01` and `grlai02`) in the 110 cells | Files | Code | Figures |
|---|---|---|---|---|---|
| **Forest** | **5** coniferous forest & woodland (93 cells actually change) | **higher**: monthly mean `grlai01` of the cells that are already class 5 in Asia north of 40°N (July 3.32, January 0.18) | `Forest_IC_files/` | `Code/build_forest_experiment/` | `Figure/build_forest_experiment/` |
| **Desert** | **8** shrubs & bare ground (98 cells actually change) | **lower**: monthly mean `grlai01` of Mongolia's DES zone (July 0.38, January 0.06) | `Desert_IC_files/` | `Code/build_desert_experiment/` | `Figure/build_desert_experiment/` |

Mean LAI over the 110 cells in the original files: `grlai01` July 1.86, January 0.12; `grlai02` July 1.88, January 0.05.

![region](Figure/build_forest_experiment/source_region_check.png)

- **Red line:** moisture-source region of Mongolia's FRONT zone (cumulative source ≤ 50 %).
- **Green line:** Mongolia's DES zone (desertified fraction ≥ 0.75). It is **not** modified.
- **Black boxes (panel B):** the 110 T42 cells that are changed. The 13 orange boxes also contain DES cells and are therefore left out.

## What was changed (both experiments)

| File | Change |
|---|---|
| **`gridx01.nc`** | **110 cells set to the experiment's class** (5 or 8). Original classes of the 110 cells: 4: 6 cells, 5: 17, 6: 17, 8: 12, 9: 1, 10: 57 |
| **`grlai01.nc`, `grlai02.nc`** | **110 cells set to 12 monthly values** (the same for all 110 cells and for both files), the area-weighted mean `grlai01` of a reference set of cells (see below) |
| `gridx02.nc`, `glfrc01.y1850.nc`, `glfrc02.y1850.nc`, `slidx.nc` | **not changed** (identical copies of the originals) |

Reference cells for the LAI:
- **Forest** (`METHOD = "class5_mean"`): the 69 T42 cells that are class 5 in the original `gridx01`, inside 20–140°E, 40–75°N,
  not among the 110; weighted by cos(latitude). 26 northern cells that already had high LAI get a slightly lower July `grlai01` (by up to 0.96).
- **Desert** (`METHOD = "des_mean"`): the 16 T42 cells that are at least 50 % DES by area; weighted by cell area x DES share
  (they are class 8: 9 cells and class 10: 7 cells in the original `gridx01`).
- `grlai02` (crop LAI) gets the same values as `grlai01` in both experiments (`REF_FROM`). For the desert this is necessary because
  the DES zone has almost no crops (crop fraction about 0.08 %), so its own `grlai02` values are filled-in numbers (July about 1.2).

All other cells are identical to the original files. The parameter tables (`LANDPARA`, `SOILPARA`) are not changed; classes 5 and 8
already exist in `LANDPARA`, so the model picks up their parameters automatically.

## Folder contents

```
Forest_IC_files/                 the 7 input files of the forest experiment
Desert_IC_files/                 the 7 input files of the desert experiment
Code/build_forest_experiment/    notebooks of the forest experiment + source_region_T42.npz
Code/build_desert_experiment/    notebooks of the desert experiment + source_region_T42.npz
Code/_old/                       earlier notebooks, replaced (kept for reference only; their paths are no longer valid)
Figure/build_forest_experiment/  figures of the forest experiment
Figure/build_desert_experiment/  figures of the desert experiment
README.md
```

## Code

Each experiment folder has the same two notebooks; run them in order. Paths are relative to the notebook's location (the notebooks
go up three levels to `Geography/`), so this folder must stay inside `Geography/`, next to `Mongolia/` and `Boundary condition/`.
Figures go to `Figure/<experiment folder>/`.

| Notebook | Does | Writes |
|---|---|---|
| `1_DES_source_region_to_T42.ipynb` | selects the 110 T42 cells (identical in both folders) | `source_region_T42.npz` (same folder), `source_region_check.png` |
| `2_make_forest_files_and_compare.ipynb` / `2_make_desert_files_and_compare.ipynb` | sets `gridx01` (`LC_CLASS`) and `grlai01`/`grlai02` (`METHOD`) in those cells, copies the 4 other files unchanged, checks everything, draws original vs modified | the 7 `.nc` files in `Forest_IC_files/` or `Desert_IC_files/` (if `WRITE = True`); `gridx01_compare.png`, `grlai01_compare.png`, `grlai02_compare.png`, `grlai_seasonal_cycle.png` |

The two step-2 notebooks differ only in their settings (`LC_CLASS`, `METHOD`) and output folder names.

Inputs read by the notebooks: `Mongolia/data/` (`mongolia_overlay.nc`, `mongolia_border.geojson`) and
`Boundary condition/bc_for_Wei/data/netcdf/` (the original input files).

Requires `numpy`, `xarray`, `netcdf4`, `matplotlib`, `cartopy`, `regionmask`.

## How the cells were chosen

1. Take the FRONT zone's cumulative source `source_cdf ≤ 50 %` (the smallest area supplying half of FRONT's moisture;
   from `Mongolia/data/mongolia_overlay.nc`).
2. Remove water bodies (e.g. the Caspian Sea) and the DES zone.
3. Map onto MATSIRO T42 cells: a cell is selected if at least 50 % of its area lies in this region and it is land in the model.
4. Remove the 13 T42 cells that also contain DES cells, so DES is not touched → **110 cells**.

## Notes and limitations

- Crop fractions (`glfrc01/02`) and soil class (`slidx`) are deliberately left unchanged. The affected cells therefore have the new
  class's parameters (vegetation height, stomata, roots, ...) combined with the new LAI and their original crop fraction and soil.
- The cells are whole T42 cells, so the edge of the modified area is stepped and does not follow the red line exactly.
- The files have been checked for content only. They have not been run in the model, and the model source code was not inspected.
