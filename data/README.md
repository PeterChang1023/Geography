# data/

這個資料夾的資料檔**沒有放進 git**（太大，GitHub 單檔上限 100 MB），只保留資料夾結構、說明與程式。要跑相關程式，請自己把下面的檔案放回原位。

`Code/Reproduce.ipynb`（論文 Fig. 2、Fig. 3 重現）**不需要**這裡的任何檔案，它只讀 `Original_code_from_authors/`。

| 檔案 | 大小 | 內容 / 來源 |
|---|---|---|
| `drainage_curves_land.nc` | 82 MB | ERA5（2020–2025）0.25° 全球陸地格點的排水曲線，只算陸地來源。WAM-2layers v3 產出的 `area_at_level`（km²） |
| `drainage_curves_allsources.nc` | 85 MB | 同上，來源含陸地與海洋 |
| `distance_curves_all.nc` | 34 MB | 同一批格點的距離（半徑）曲線 |
| `gleamgpm_0615_allpoint_con.npy` | 4 MB | 論文 GLEAM+GPM 2006–2015、724 格的累積貢獻（%），**另一版**；論文實際用的是 `Original_code_from_authors/` 裡的 pversion 版，兩版差異見 `Code/Reproduce.ipynb` 附錄 |
| `gleamgpm_0615_allpoint_area.npy` | 4 MB | 對應的面積（平方度），和 pversion 版完全相同 |
| `Taiwan Land, Water and Life Data.xlsx` | 0.5 MB | 另外的台灣資料，和本專案的論文重現無關 |
| `drainage_xy_by_continent/raw_nc_data/drainage_curves_{allsources,land}.nc` | 85 / 82 MB | 上面兩個 nc 的複本，給分洲腳本用 |
| `drainage_xy_by_continent/divided_data/drainage_xy_{all,land}_{洲名}.csv` | 12 個，共約 2.2 GB | 由 `drainage_xy_by_continent/code/drainage_xy_by_continent.py` 從上面兩個 nc 產生，可重新產生 |

`drainage_xy_by_continent/Figures/` 裡的小圖與小表格（< 1 MB）有放進 git。
