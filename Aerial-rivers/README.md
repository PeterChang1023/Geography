# Aerial rivers: reproducing the drainage curves of South American aerial rivers (Weng et al., 2026)

This repository reproduces

> Weng et al. (2026). *Hydrological regimes and drainage systems of aerial rivers across South America*. Nature Communications 17:9341. https://doi.org/10.1038/s41467-026-76303-y

specifically **Fig. 2** (the four drainage types G1–G4 and their drainage curves for 724 grid cells at 1.5°) and **Fig. 3** (the turning point of each type). The algorithm follows the original code provided by the authors, and the results match the paper: median turning points are G1 95.3%, G2 68.6%, G3 48.0%, G4 35.5%, and Sorriso 46.7% (paper: 47%).

The same algorithm is then applied to ERA5 drainage curves (2020–2025, 0.25°) for every continent and for the whole globe, and the curves are additionally analysed with EOFs.

## Notebook contents (`Code/Reproduce.ipynb`)

| Section | Content |
|---|---|
| 1–6 | Paper reproduction with GLEAM+GPM data: data, lat/lon of the 724 cells, interpolation to 1000 points, clustering (the paper's fixed groups, checked with k-means), Fig. 2, turning points / Fig. 3 |
| Appendix | What was wrong with earlier attempts (data version, turning-point algorithm, linear vs. log k-means features, which axis to take ln of, lat/lon) |
| 7.1–7.2 | Author's algorithm applied to ERA5 (`data/drainage_curves_land.nc`, WAM-2layers v3, land sources only): build curves for all land cells and compare curves cell by cell with the paper (no clustering) |
| 7.3 | k-means reproduction on all 0.25° cells of the 7 South American AR6 regions (NWS, NSA, SAM, NES, SWS, SES, SSA), k = 4; choosing k with Calinski–Harabasz, Davies–Bouldin and the elbow method; comparison with the paper's groups (per 0.25° cell and majority vote back to 1.5°) |
| 7.4–7.10 | Same clustering for each other continent using its own cells (North America, Europe, Africa, Asia, Oceania), with the cos(latitude) area correction; summary table, conclusions, and mistakes in earlier ERA5 attempts |
| 8 | Global clustering: all 185,546 0.25° land cells clustered together with the Section 7 method (no split by continent) |
| 9–9.2 | EOF analysis of the South American curves with `Code/EOF.py`: explained variance, EOF1/EOF2 shapes and PC maps, how each EOF modifies the mean curve |
| 9.3 | EOF-based clustering (functional PCA + k-means): PC1 and PC2 (92.3% of the variance) → k-means with 4 groups, compared with Section 7.3 and with the paper |
| 9.4–9.10 | The same EOF analysis for North America, Europe, Africa, Asia, Oceania and the globe, plus a summary table across regions |

## Repository layout

```
Aerial-rivers/
├── Code/
│   ├── Reproduce.ipynb          Main notebook (see the table above)
│   └── EOF.py                   EOF helper (sklearn PCA) used in Section 9; `dataset` must be a tuple
├── Figures/                     Figures produced by the notebook (Fig2_GLEAMGPM.png, Fig3_GLEAMGPM.png, ERA5 figures per continent, EOF figures, etc.)
├── Original_code_from_authors/  Original code and data from the paper's authors (see below)
├── Paper/                       The paper PDF is not in the repo (see the DOI above); Zenodo/ holds the paper's moisture-tracking code
├── data/                        ERA5 drainage curves and other data; data files are not in the repo, see data/README.md
└── scripts/                     Script that splits the .nc files in data/ into per-continent CSVs
```

## Original_code_from_authors/

Files provided by the paper's authors, kept unchanged:

| File | Content |
|---|---|
| `Turningpoint_peak.ipynb` | The authors' code for the turning points, Fig. 3 and Fig. S5 |
| `gleamgpm_0615_pversion_allpoint_con.npy` | (724, 725), cumulative contribution C (%) for each cell, GLEAM+GPM 2006–2015 |
| `gleamgpm_0615_pversion_allpoint_area.npy` | (724, 725), corresponding upwind basin area (square degrees, 2.25 per cell) |
| `group_fix_4groups.txt` | Fixed grouping on the 44 × 38 grid (0 = non-land, 1–4 = G1–G4) |

## How to run

Use the `Geography` conda environment (Python 3.12). Required packages: numpy, scipy, scikit-learn, matplotlib (the ERA5 sections and the `data/` scripts also need xarray, netCDF4 and pandas).

```bash
conda activate Geography
python -m ipykernel install --user --name geography --display-name "Python (Geography)"   # first time only
jupyter nbconvert --to notebook --execute --inplace Code/Reproduce.ipynb --ExecutePreprocessor.kernel_name=geography
```

Or open `Code/Reproduce.ipynb` in VS Code / Jupyter, select the "Python (Geography)" kernel, and run all cells. Sections 1–6 only need the files in `Original_code_from_authors/`; Sections 7–9 also need `data/drainage_curves_land.nc` (see `data/README.md`).
