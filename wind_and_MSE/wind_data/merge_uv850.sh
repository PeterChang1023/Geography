#!/bin/bash
# Merge ERA5 daily 850 hPa u and v (1990-2021) into one file per variable.
# Input : /work/DATA/Reanalysis/ERA5/{u,v}/{u,v}850_YYYY.nc  (daily, 0.625x0.5 grid)
# Output: /data92/PeterChang/Geography/wind_and_MSE/wind_data/{u,v}850_1990-2021.nc
set -euo pipefail

SRC=/work/DATA/Reanalysis/ERA5
OUT=/data92/PeterChang/Geography/wind_and_MSE/wind_data
Y0=1990
Y1=2021
LEV=850

mkdir -p "$OUT"

for var in u v; do
  files=()
  for yr in $(seq $Y0 $Y1); do
    f="$SRC/$var/${var}${LEV}_${yr}.nc"
    [[ -f "$f" ]] || { echo "Missing: $f" >&2; exit 1; }
    files+=("$f")
  done
  out="$OUT/${var}${LEV}_${Y0}-${Y1}.nc"
  echo "Merging ${#files[@]} files -> $out"
  cdo -O -b F32 mergetime "${files[@]}" "$out"
done

echo "Done."
cdo sinfon "$OUT/u${LEV}_${Y0}-${Y1}.nc" | head -20
