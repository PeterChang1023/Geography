# Aerial rivers：重現 Weng et al. (2026) 的南美空中河流排水曲線

重現論文

> Weng et al. (2026). *Hydrological regimes and drainage systems of aerial rivers across South America*. Nature Communications 17:9341. https://doi.org/10.1038/s41467-026-76303-y

的 **Fig. 2**（724 個 1.5° 格點的四種排水類型 G1–G4 與排水曲線）和 **Fig. 3**（各類型的轉折點）。算法照作者提供的原始程式，結果和論文一致：轉折點中位數 G1 95.3%、G2 68.6%、G3 48.0%、G4 35.5%，Sorriso 46.7%（論文 47%）。

## 資料夾結構

```
Aerial-rivers/
├── Code/
│   └── Reproduce.ipynb          主筆記本：資料 → 經緯度 → 內插 → 分群 → Fig. 2 → 轉折點 / Fig. 3，附錄整理之前做法的錯誤；第 7 節套到 ERA5 各洲
├── Figures/                     筆記本產生的所有圖（Fig2_GLEAMGPM.png、Fig3_GLEAMGPM.png、各洲 ERA5 圖等）
├── Original_code_from_authors/  論文作者提供的原始程式與資料（見下）
├── Paper/                       論文 PDF 不放在 repo（見上方 DOI）；Zenodo/ 是論文附的軌跡追蹤程式
├── data/                        ERA5 排水曲線等資料，資料檔不放在 repo，見 data/README.md
└── scripts/                     把 data/ 的 nc 依洲切割成 CSV 的腳本
```

## Original_code_from_authors/

論文作者提供的檔案，原樣保留：

| 檔案 | 內容 |
|---|---|
| `Turningpoint_peak.ipynb` | 作者算轉折點、畫 Fig. 3 與 Fig. S5 的程式 |
| `gleamgpm_0615_pversion_allpoint_con.npy` | (724, 725)，每個格點的累積貢獻 C（%），GLEAM+GPM 2006–2015 |
| `gleamgpm_0615_pversion_allpoint_area.npy` | (724, 725)，對應的上風盆地面積（平方度，每格 2.25） |
| `group_fix_4groups.txt` | 44 × 38 網格上的固定分群（0 = 非陸地，1–4 = G1–G4） |

## 怎麼跑

使用 `Geography` conda 環境（Python 3.12），需要的套件：numpy、scipy、scikit-learn、matplotlib（`data/` 相關腳本另外需要 xarray、netCDF4、pandas）。

```bash
conda activate Geography
python -m ipykernel install --user --name geography --display-name "Python (Geography)"   # 第一次才需要
jupyter nbconvert --to notebook --execute --inplace Code/Reproduce.ipynb --ExecutePreprocessor.kernel_name=geography
```

或在 VS Code / Jupyter 開 `Code/Reproduce.ipynb`，選 kernel「Python (Geography)」後全部執行。`Reproduce.ipynb` 只需要 `Original_code_from_authors/` 裡的檔案，不需要 `data/`。
