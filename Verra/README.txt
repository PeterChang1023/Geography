Verra 專案:公司所屬國分析
==========================
資料來源:~/Downloads/Verra_active_project.xlsx(1657 個專案列)
環境:micromamba / conda 環境 "Geography"(與 base 分開;讀 Excel 用 pandas + calamine,不用 openpyxl)
  執行 notebook 例:
    /opt/local/bin/micromamba run -n Geography jupyter nbconvert --to notebook --execute --inplace "Geography foreign.ipynb"

資料夾
------
code/    程式
           Geography analysis.ipynb   主流程:分類公司所屬國 → 輸出 csv(含 Step 5b 公司所在地搜尋結果、Step 6 國家統計與地圖)
           Geography map.ipynb        世界地圖(cartopy)+ 五大洲公司數長條圖(畫圖設定在最上面的設定區,可自己改)
           Geography foreign.ipynb    外資分析(Step 1-8,見下方)
           country_overrides.py       手動指定的公司→國家(OVERRIDES)
           researched_ownership.py    上網查「最大股東」的結果(RESEARCHED,優先於 OVERRIDES)
           location_checks.py         「公司 company location」搜尋結果(LOCATIONS,中國/土耳其/印度推斷公司共 524 家)
           _old_scripts/              早期 .py 版本,已過時,不要執行(會蓋掉 data/ 較新的分類結果)
data/    所有 csv(分類結果、統計、明細)
Photo/   所有圖(png)

今天的工作流程
--------------
1. 分類規則
   - 跳過 "Multiple Project Proponents",以及 "Credits transferred…" / "Converted…" 這類非公司列
   - 公司有多國持股 → 取持股最大的國家;對半(平手)→ 兩國都算(存成 "A|B")
   - 單一國家持有 → 該國;使用「公司所屬國」(註冊地/母公司所在地)
   - 香港算中國;Excel 的 "Mainland China"、"Taiwan" 分開
2. 分類順序(每家公司,見 analysis notebook 的 classify):
   RESEARCHED(網路查證)→ OVERRIDES(手動)→ LOCATIONS(公司所在地搜尋)→ 專案國 + 當地法律型態(中信心)→ 單一專案國(低信心)→ 未解決
   信心 H=明確/知名公司,M=推斷或間接證據,L=未查證
3. 上網查證:未解決、低信心、單一專案未驗證、以及中國(267)/土耳其(80)/印度(177)的推斷公司,逐家查官網 About 或 "<公司名> company location",依規則 2 重新歸屬。
   結果記在 proponents_classified.csv 的 method / note 欄,與 location_search_results.csv(含證據)。
4. 地圖與統計:country_counts.csv、geography_map.png、continent_company_counts.png(五大洲公司數)
5. 外資分析(Geography foreign.ipynb)
   Step 1-5  流出型外資:公司所屬國 ≠ 專案所在國;中國/印度/土耳其/美國的外資做什麼產業(Sectoral Scope)
   Step 6    各國外資公司數(由多到少,垂直長條圖)
   Step 7    反過來:在中國/印度/土耳其/美國做的專案,公司註冊在哪些國家(含本國,本國灰色)
   Step 8    南美洲:專案在南美洲、公司註冊在國外 → 25 個專案;來源國(美、加、法、瑞士…)與產業(農林 15、能源 9、能源需求 1、廢棄物 1)

注意事項
--------
- 外資數字是「下限」:查不到持股的公司,所屬國是用專案所在國推斷,定義上不可能被算成外資。
  目前約 224 家(中國/土耳其/印度)查了但英文網路上沒有紀錄,維持推斷。
- 被跳過的 Multiple Project Proponents 專案不在任何分析內(例如土耳其有 36 個專案、其餘國家同樣有)。
- 對半持股的公司在兩個所屬國各算一次,所以各國加總會比公司/專案總數多(五大洲公司數加總 979 vs 不重複 973)。
  在「專案所在國」分析(Step 7/8)中,若所屬國包含專案所在國(如 Turkey|Germany 在土耳其)就不算外資。
- Sectoral Scope 一個專案可有多個產業,每個產業各算一次,所以產業長條總和可能大於專案數(南美 25 個專案 → 26)。
  產業名稱本身含逗號,所以是用 15 個已知產業名稱比對,不是用逗號切。
- 部分歸屬信心偏低,可抽查:Alto Maipo、Impala Terminals Colombia、Ecosecurities(南美國外公司)、Apraava(中國|加拿大平手)、
  Topigs Norsvin(中國|荷蘭)、以及名稱相似公司的比對(見 location_checks.py 的 evidence 欄)。
- 國家名稱要和 Excel 一致:COUNTRY_RENAME 把 "United States of America"→"United States"、"Korea (Republic of)"→"South Korea" 等;
  新增分析時 project_country 要先 rename 再與 home_country 比較。
- 路徑:notebook 第一格定義 CODE / DATA / PHOTO。讀寫 csv 用 DATA / "xxx.csv",存圖用 PHOTO / "xxx.png",不要寫成 HERE / ...。
- 改查證結果:加到 researched_ownership.py / country_overrides.py / location_checks.py,再重跑 Geography analysis.ipynb,
  然後依序重跑 map、foreign notebook(foreign 讀 data/proponents_classified.csv)。
- 網頁搜尋批次不要一次超過約 10 個平行查詢,容易被限流。
- macOS 對 Desktop 的 code 資料夾有寫入限制(EPERM),所以專案放在 ~/Downloads/Geography/。
