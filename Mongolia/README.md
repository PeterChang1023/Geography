# 蒙古水氣來源 — 疊圖資料包

簡報裡兩張圖的底層格點資料，加上重現它們的 notebook。

- `tags_preview.png` — 沙漠化比例、三區劃分
- `source_maps.png` — 四個區的水氣來源密度

PNG 帶著座標軸、色標和標題，疊圖時只能用眼睛對齊。
所以這裡給的是**有座標的格點資料**，疊圖可以精確對位。
等值線也以資料欄位的形式提供，不是畫死的線 —— 要畫哪一條、或一條都不畫，由你決定。

## 內容

```
data/
  mongolia_overlay.nc            所有格點資料（22 MB）
  mongolia_border.geojson        蒙古國界（EPSG:4326）
  FRONT_source_density.tif       FRONT 來源密度，GeoTIFF
  FRONT_source_cdf.tif           FRONT 累積來源，GeoTIFF
  des_fraction.tif               沙漠化比例，GeoTIFF
  zone_id.tif                    三區劃分，GeoTIFF
figures/
  tags_preview.png               簡報上的原圖
  source_maps.png                簡報上的原圖，含 50/90/99 % 等值線
  tags_preview_repro.png         由 .nc 重現
  source_maps_repro.png          由 .nc 重現，含等值線
  source_maps_repro_nocontour.png  四個區一起，無等值線
  source_FRONT_nocontour.png     FRONT 單張，無等值線
notebooks/
  重現與疊圖.ipynb                從 .nc 把上面每一張畫回來（已執行，附輸出）
README.md
DENSITY.md                       e_track 的單位與等值線算法
```

`*_repro.png` 是從 `.nc` 重畫的版本，和簡報原圖是同一份資料；
原圖一併留著，方便比對。

## `.nc` 裡的變數

| 變數 | 維度 | 內容 |
|---|---|---|
| `e_track` | zone, lat, lon | 來源密度，36 年總量（kg m⁻²）|
| `e_track_per_year` | zone, lat, lon | 同上，除以 36 的年平均 |
| `source_cdf` | zone, lat, lon | 累積來源百分比 —— 等值線從這裡畫 |
| `cell_area` | lat, lon | 每格面積（m²）|
| `des_fraction` | lat, lon | 每格沙漠化比例，蒙古境外為 NaN |
| `zone_id` | lat, lon | 0 非蒙古 / 1 DES / 2 FRONT / 3 NON |

`zone` 四個值：

| | 定義 | 格數 |
|---|---|---|
| `MN_ALL` | 全蒙古 | 2945 |
| `DES` | 沙漠化比例 ≥ 0.75 | 1822 |
| `FRONT` | 0.25 < 比例 < 0.75（前緣帶）| 465 |
| `NON` | 比例 ≤ 0.25 | 658 |

DES / FRONT / NON 互斥且合起來等於 MN_ALL。

每個變數都有 `description` 屬性：`ds['e_track'].attrs`。

## 兩件疊圖時要注意的事

1. **緯度是遞減的**（由北到南），與 GeoTIFF 的慣例相同，不要再翻轉一次。
2. 座標是**格中心**。轉 GeoTIFF 時左上角要退半格（經度 −0.125°、緯度 +0.125°）。
   notebook 最後一節已經處理好了。

## 跑 notebook

```bash
pip install numpy matplotlib xarray netcdf4
pip install regionmask rasterio      # 可選：全球國界底圖、轉 GeoTIFF
jupyter lab
```

`regionmask` 第一次執行會上網抓 Natural Earth 國界。抓不到也能跑，只是少了全球底圖，
蒙古國界仍會從 `mongolia_border.geojson` 畫出來。

## 資料來源

AguaTrack（WAM2Layers v3 的 GPU 批次版本），ERA5 0.25° 逐時驅動，內部步長 600 秒。
1990–2025，36 個完整年。

沙漠化分類來自 2021–2025 的 500 m 兩類影像，逐格面積平均到 0.25° 網格。
這是**單一時期的快照**，不是逐年變化。

本檔由 425 GB 的逐月追蹤輸出匯總而成；中間檔（2.57 GB）與 465 個前緣網格各自的來源場
（1.4 GB）沒有放進來，需要再說。
