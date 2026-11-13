#!/bin/bash
# Compute daily 850 hPa moist static energy (1990-2021) from merged ERA5 t, z, q.
#   MSE = Cp*T + Phi + Lv*q   [J kg-1]
#   Cp = 1004 J kg-1 K-1, Lv = 2.5e6 J kg-1
#   z in ERA5 is geopotential Phi = g*z [m2 s-2], so it is NOT multiplied by g again.
# Input : /data92/PeterChang/Geography/wind_and_MSE/mse_data/{t,z,q}850_1990-2021.nc
# Output: /data92/PeterChang/Geography/wind_and_MSE/mse_data/mse850_1990-2021.nc  (variable: mse)
set -euo pipefail

DIR=/data92/PeterChang/Geography/wind_and_MSE/mse_data
TAG=850_1990-2021
CP=1004
LV=2500000

for var in t z q; do
  [[ -f "$DIR/${var}${TAG}.nc" ]] || { echo "Missing: $DIR/${var}${TAG}.nc" >&2; exit 1; }
done

out="$DIR/mse${TAG}.nc"
echo "Computing MSE -> $out"
cdo -O -b F32 \
  -setattribute,mse@units="J kg-1",mse@long_name="Moist static energy at 850 hPa (Cp*T + Phi + Lv*q)" \
  -expr,"mse=${CP}*t+z+${LV}*q" \
  -merge "$DIR/t${TAG}.nc" "$DIR/z${TAG}.nc" "$DIR/q${TAG}.nc" \
  "$out"

echo "Done."
echo "ntime=$(cdo -s ntime "$out")"
cdo -s outputf,%.1f -fldmin -timmin "$out" | sed "s/^/global min: /"
cdo -s outputf,%.1f -fldmax -timmax "$out" | sed "s/^/global max: /"
cdo -s outputf,%.1f -fldmean -timmean "$out" | sed "s/^/global mean: /"
