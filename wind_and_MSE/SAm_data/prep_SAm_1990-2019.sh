#!/bin/bash
# South America subset of ERA5 daily 850 hPa u, v, t, z, q (1990-2019) + moist static energy.
#   Domain : 100W-25W, 60S-20N  (plot domain 95W-30W, 55S-15N plus a 5-degree margin)
#   Input  : /work/DATA/Reanalysis/ERA5/<var>/<var>850_YYYY.nc  (global, daily, 0.625x0.5 grid)
#   Output : /data92/PeterChang/Geography/wind_and_MSE/SAm_data/<var>850_SAm_1990-2019.nc
#            /data92/PeterChang/Geography/wind_and_MSE/SAm_data/mse850_SAm_1990-2019.nc
#   MSE    = Cp*T + Phi + Lv*q  [J kg-1], Cp = 1004, Lv = 2.5e6; ERA5 z is already Phi = g*z.
# Existing global 1990-2021 files are not touched.
set -euo pipefail

SRC=/work/DATA/Reanalysis/ERA5
OUT=/data92/PeterChang/Geography/wind_and_MSE/SAm_data
Y0=1990
Y1=2019
LEV=850
BOX=-100,-25,-60,20     # lon1,lon2,lat1,lat2 for cdo sellonlatbox
TAG=${LEV}_SAm_${Y0}-${Y1}
CP=1004
LV=2500000

mkdir -p "$OUT"

# 1. Cut the domain and merge the yearly files for each variable
for var in u v t z q; do
  files=()
  for yr in $(seq $Y0 $Y1); do
    f="$SRC/$var/${var}${LEV}_${yr}.nc"
    [[ -f "$f" ]] || { echo "Missing: $f" >&2; exit 1; }
    files+=("$f")
  done
  out="$OUT/${var}${TAG}.nc"
  echo "[$var] ${#files[@]} files -> $out"
  cdo -O -b F32 -sellonlatbox,$BOX -mergetime "${files[@]}" "$out"
done

# 2. Moist static energy
out="$OUT/mse${TAG}.nc"
echo "[mse] -> $out"
cdo -O -b F32 \
  -setattribute,mse@units="J kg-1",mse@long_name="Moist static energy at 850 hPa (Cp*T + Phi + Lv*q)" \
  -expr,"mse=${CP}*t+z+${LV}*q" \
  -merge "$OUT/t${TAG}.nc" "$OUT/z${TAG}.nc" "$OUT/q${TAG}.nc" \
  "$out"

# 3. Quick check: every file should have 10957 days (1990-01-01 .. 2019-12-31)
echo "Done."
for var in u v t z q mse; do
  f="$OUT/${var}${TAG}.nc"
  echo "${var}: ntime=$(cdo -s ntime "$f")  grid=$(cdo -s griddes "$f" | grep -E "xsize|ysize" | tr -s " " | tr "\n" " ")"
done
