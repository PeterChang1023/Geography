#!/bin/bash
# Merge ERA5 daily 850 hPa t, z, q (1990-2021) into one file per variable (for MSE).
# Input : /work/DATA/Reanalysis/ERA5/{t,z,q}/{t,z,q}850_YYYY.nc  (daily, 0.625x0.5 grid)
# Output: /data92/PeterChang/Geography/wind_and_MSE/mse_data/{t,z,q}850_1990-2021.nc
# Units : t [K], z [m**2 s**-2] (geopotential = g*z), q [kg kg**-1]
set -euo pipefail

SRC=/work/DATA/Reanalysis/ERA5
OUT=/data92/PeterChang/Geography/wind_and_MSE/mse_data
Y0=1990
Y1=2021
LEV=850

mkdir -p "$OUT"

for var in t z q; do
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
for var in t z q; do
  echo "${var}${LEV}: ntime=$(cdo -s ntime "$OUT/${var}${LEV}_${Y0}-${Y1}.nc")"
done
