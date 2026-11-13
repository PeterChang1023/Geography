# wind_and_MSE

ERA5 850 hPa 風場與濕靜能（MSE）的 1990–2021 氣候平均分析，畫成 cartopy 世界地圖（MSE 填色＋風向量）。

## 資料夾結構

```
wind_and_MSE/
├── Code/
│   └── uv850_worldmap.ipynb   # 讀 u/v/MSE，算全期與 DJF/JJA 平均並畫圖
├── Figures/                   # notebook 輸出的圖（FIG_DIR = '../Figures'）
├── SAm_data/
│   └── prep_SAm_1990-2019.sh  # 南美洲 1990–2019：切範圍＋合併 u/v/t/z/q＋算 MSE（notebook 目前用這組）
├── wind_data/
│   └── merge_uv850.sh         # 合併 u850、v850
└── mse_data/
    ├── merge_tzq850.sh        # 合併 t850、z850、q850
    └── calc_mse850.sh         # 由 t、z、q 計算 MSE
```

**.nc 資料只在 hinton 上**，本機沒有下載：
`hinton:/data92/PeterChang/Geography/wind_and_MSE/{SAm_data,wind_data,mse_data}/`

**目前 notebook 使用的資料**：`SAm_data/{u,v,t,z,q,mse}850_SAm_1990-2019.nc`
（範圍 100°W–25°W、60°S–20°N，120×160 格，10957 天，每檔約 0.8 GB）。

以下是較早的全球 1990–2021 版本（每檔約 9–10 GB）：

| 檔案 | 變數 | 單位 |
|---|---|---|
| `wind_data/u850_1990-2021.nc` | u | m/s |
| `wind_data/v850_1990-2021.nc` | v | m/s |
| `mse_data/t850_1990-2021.nc` | t | K |
| `mse_data/z850_1990-2021.nc` | z（位勢 Φ = gz） | m²/s² |
| `mse_data/q850_1990-2021.nc` | q | kg/kg |
| `mse_data/mse850_1990-2021.nc` | mse | J/kg |

全部是日資料，11688 天（1990-01-01 – 2021-12-31），網格 576×360（0.625° × 0.5°）。

## 資料來源

hinton 上的 ERA5 日資料：`/work/DATA/Reanalysis/ERA5/<var>/<var><level>_<YYYY>.nc`
（每年一檔，1979–2021，層次 1000/925/850/700/500/250/200/100 hPa）。

## MSE

MSE = Cp·T + Φ + Lv·q

- Cp = 1004 J kg⁻¹ K⁻¹，Lv = 2.5×10⁶ J/kg
- ERA5 的 `z` 已經是位勢 Φ = g·z，**不要再乘 g**
- 圖上單位換成 kJ/kg

## 怎麼跑（在 hinton 上）

```bash
# 南美洲 1990–2019（目前使用，約 4 分鐘）
cd /data92/PeterChang/Geography/wind_and_MSE/SAm_data && nohup bash prep_SAm_1990-2019.sh > prep_SAm_1990-2019.log 2>&1 &

# --- 以下為舊的全球 1990–2021 流程 ---
# 1. 合併年檔（各約 3–6 分鐘，建議 nohup 背景跑）
cd /data92/PeterChang/Geography/wind_and_MSE/wind_data && nohup bash merge_uv850.sh > merge_uv850.log 2>&1 &
cd /data92/PeterChang/Geography/wind_and_MSE/mse_data  && nohup bash merge_tzq850.sh > merge_tzq850.log 2>&1 &

# 2. 計算 MSE（需先完成 t/z/q 合併）
cd /data92/PeterChang/Geography/wind_and_MSE/mse_data && nohup bash calc_mse850.sh > calc_mse850.log 2>&1 &

# 3. 執行 notebook（conda 環境 jupyter_git）
cd /data92/PeterChang/Geography/wind_and_MSE/Code
conda activate jupyter_git
jupyter nbconvert --to notebook --execute --inplace uv850_worldmap.ipynb
```

notebook 用相對路徑讀資料（`DATA_DIR = '../SAm_data'`，年份由 `PERIOD` 控制），所以要在 `Code/` 底下執行；在本機跑會找不到 .nc 檔。

## 注意事項

- 青藏高原、南極、格陵蘭等高地形區的 850 hPa 在地表以下，這些地方的值是 ERA5 外插出來的，解讀時要忽略。
- hinton 上沒有地表氣壓或地表位勢資料，目前無法把這些格點遮掉；要遮的話需另外從 CDS 下載 ERA5 surface geopotential。
- 畫圖範圍由 notebook 開頭的 `EXTENT`（目前南美洲 95°W–30°W、55°S–15°N）和 `REGION`（檔名後綴，目前 `SAm`）控制，輸出 `Figures/*_1990-2019_SAm.png`。
- 全球版的圖已於 2026-11-06 刪除；`Figures/*_1990-2021_SAm.png` 是用舊的全球 1990–2021 資料切南美洲範圍畫的舊版，目前的 notebook 已不再產生。
