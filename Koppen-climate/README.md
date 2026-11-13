# Köppen-Geiger 氣候分類

用 Python 讀取 Beck et al. (2023) 的 Köppen-Geiger 氣候分類 GeoTIFF，並畫出全球分類圖、台灣分類圖和沙漠範圍圖。

## 資料夾結構

```
Koppen-climate/                    # 原名 Köppen climate classification
├── README.md
├── Code/
│   ├── read_koppen.py        # 腳本版：讀檔、查點、裁出台灣、統計比例、畫台灣圖
│   ├── read_koppen.ipynb     # Notebook 版：上述內容 + 全球圖 + 沙漠範圍圖
│   └── africa_desert_curves_Weng2026S4.ipynb   # 非洲沙漠格點的 Aerial-rivers 排水曲線、30°E 剖面、20°N 東→西演變（仿 Weng et al. 2026 Fig. S4）
├── Figure/
│   ├── koppen_figures/             # Köppen 分類圖
│   │   ├── koppen_taiwan.png           # 台灣 1 km 氣候分類
│   │   ├── koppen_global_0p5.png       # 全球 0.5° 氣候分類（30 類圖例）
│   │   └── desert_BWh_BWk_0p5.png      # 全球沙漠範圍（BWh + BWk）
│   └── Africa_curves/              # 非洲 Aerial-rivers 排水曲線（africa_desert_curves_Weng2026S4.ipynb）
│       ├── africa_desert_curves_selected.png  # 非洲沙漠格點挑選（≤ 30°E）
│       ├── africa_30E_curves.png              # 30°E 上全部非洲格點的曲線
│       ├── africa_30E_desert_curves.png       # 舊版：30°E 只取沙漠格點
│       └── africa_20N_E2W_curves.png          # 20°N 由 20°E 往西到 10°W（仿 Fig. S4）
├── Notes/
│   └── transect_plan/
│       └── desert_transects_sticky_notes.jpeg  # 想測試的經緯度剖面線（手寫便條：澳洲、南美、非洲、亞洲）
└── Data/                          # 原始資料 Koppen Geiger Maps 1901-2099（不要修改）
    ├── legend.txt                  # 代碼 1–30 對應的類別與 RGB 顏色
    └── 1991_2020/
        ├── koppen_geiger_0p00833333.tif   # ~1 km，43200×21600
        ├── koppen_geiger_0p1.tif          # 0.1°，3600×1800
        ├── koppen_geiger_0p5.tif          # 0.5°，720×360
        └── koppen_geiger_1p0.tif          # 1.0°，360×180
```

`Data/` 原名為 `Koppen Geiger Maps 1901-2099`。目前只有 1991–2020 這個時期，1901–2099 是指資料集涵蓋的完整範圍。

## 資料格式

- 單波段 `uint8` GeoTIFF，座標系統 EPSG:4326（經緯度），範圍 −180~180°E、−90~90°N
- 像素值 `0` 是海洋或無資料（nodata），`1`–`30` 是氣候類別，對照表在 `legend.txt`
- 檔案已內嵌論文配色的調色盤，LZW 壓縮

常用代碼：`1` Af、`4` BWh（熱沙漠）、`5` BWk（冷沙漠）、`6` BSh、`7` BSk、`14` Cfa、`29` ET、`30` EF。

## 怎麼執行

請使用 conda 的 `Geography` 環境（內含 rasterio、matplotlib）。base anaconda 的 numpy 會出現 libgfortran 錯誤，所以不要用 base。

```bash
cd /Users/peterchang/Projects/Geography/Koppen-climate
~/opt/anaconda3/envs/Geography/bin/python Code/read_koppen.py
```

Notebook：在 VS Code 打開 `Code/read_koppen.ipynb`，kernel 選 **Geography**。程式會自動找上一層的資料夾，圖片則輸出到 `Figure/`。

## 注意事項

- 沙漠用代碼篩選 `(g == 4) | (g == 5)`，不要用顏色比對。依 1991–2020 的 0.5° 資料計算，沙漠約占全球陸地（含南極）的 17.1%，其中 BWh 13.9%、BWk 3.2%。
- 經緯度網格的面積會隨緯度變小，做全球面積統計時要用 cos(緯度) 加權。
- 1 km 的檔案建議用 `rasterio.windows.from_bounds` 只讀需要的區域。

## 資料來源與引用

Beck, H. E., T. R. McVicar, N. Vergopolan, A. Berg, N. J. Lutsko, A. Dufour, Z. Zeng, X. Jiang, A. I. J. M. van Dijk, and D. G. Miralles (2023). High-resolution (1 km) Köppen-Geiger maps for 1901–2099 based on constrained CMIP6 projections. *Scientific Data*, 10, 724. https://doi.org/10.1038/s41597-023-02549-6
