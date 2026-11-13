# Geography

Code, notebooks and notes for my geography / climate research projects.
Only code, notebooks and READMEs are tracked here. Data files (`.nc`, `.tif`, `.csv`, `.npy`, …), figures and backups are excluded by `.gitignore` and stay local.

| Folder | What it is |
|---|---|
| [`Aerial-rivers/`](Aerial-rivers/) | Reproduction of Weng et al. (2026) aerial-river / drainage curves (Fig. 2–3), k-means clustering by continent, EOF analysis. Merged in with its full history from the former `Aerial-rivers` repo. |
| [`Koppen-climate/`](Koppen-climate/) | Köppen climate classification (1991–2020 GeoTIFF): reading/plotting examples and African desert curves in the style of Weng et al. (2026) Fig. S4. |
| [`MATSIRO6_IC_exp/`](MATSIRO6_IC_exp/) | MATSIRO6 land-cover experiments: forest and desert initial-condition files (`gridx01`, LAI) for the Mongolian moisture-source region at T42. |
| [`Mongolia/`](Mongolia/) | Mongolian moisture-source region (DES) mapped to T42, land-cover-only experiment and overlay figures. |
| [`wind_and_MSE/`](wind_and_MSE/) | ERA5 850 hPa wind and moist static energy maps (global and South America); shell scripts used to prepare the data on the server. |
| [`Verra/`](Verra/) | Analysis of Verra carbon-credit projects: proponent classification, foreign ownership and project locations. |
| [`Boundary condition/`](Boundary%20condition/) | Notes on the boundary-condition / parameter files for the model experiments. |

Each folder has its own README with details.

## Environment

Python via conda (`Geography` env on Mac). Raw ERA5 data lives on the lab server and is not part of this repo.
