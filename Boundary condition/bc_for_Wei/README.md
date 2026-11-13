# bc_for_Wei

This repository collects MATSIRO land-surface input maps and parameter tables, and produces global overview figures. 

## Brief data summary

The dataset combines global maps on a 128 × 64 longitude-latitude grid with lookup tables indexed by land-cover or soil class.

| File | Contents | Time dimension |
| --- | --- | --- |
| `glfrc01.y1850` | Natural vegetation fraction derived from LUH2 v2h | One field for 1850 |
| `glfrc02.y1850` | Crop fraction derived from LUH2 v2h | One field for 1850 |
| `gridx01` | Primary land-surface class index | Constant |
| `gridx02` | Secondary land-surface class index | Constant |
| `grlai01` | Natural vegetation leaf area index (LAI) derived from MODIS | Twelve monthly fields |
| `grlai02` | Crop LAI derived from MODIS | Twelve monthly fields |
| `slidx` | Dominant soil-texture class index derived from ISLSCP Initiative I | Constant |
| `LANDPARA.mat4c-ice.g66` | Land-cover-dependent vegetation and surface parameter table | Lookup table |
| `SOILPARA.mat2.g66` | Soil-class-dependent thermal and hydraulic parameter table | Lookup table |

`glfrc01.y1850` and `glfrc02.y1850` are complementary. Their values sum to exactly 1.0 at all 8,192 grid cells in the converted files.

## Meaning of `idx` and `val` in the parameter tables

The two `*PARA*` files are Fortran namelist-style lookup tables rather than gtool map files. In each record, `name` identifies a model parameter, `idx` identifies the land-cover or soil class, and `val` gives the value assigned to that class. A notation such as `val=6*0.421` repeats `0.421` for all six soil layers.

The parameter meanings below follow Tables 1.8 and 1.9 of Guo et al. (2021), *Description of MATSIRO6*.

### `LANDPARA.mat4c-ice.g66`

| Name | Meaning | Unit |
| --- | --- | --- |
| `ALB` | Surface albedo | 1 |
| `Z0` | Surface roughness length | m |
| `DFG` | Surface thermal conductivity | W m⁻¹ K⁻¹ |
| `VEGH` | Vegetation height, or canopy-top height | m |
| `VEGB` | Height of the canopy bottom | m |
| `ROOTD` | Fraction of roots in each soil layer | 1 |
| `RLFV`, `RLFN` | Leaf albedo in the visible and near-infrared bands | 1 |
| `TLFV`, `TLFN` | Leaf transmissivity in the visible and near-infrared bands | 1 |
| `VGCOV` | Vegetation coverage | 1 |
| `CDL` | Leaf-atmosphere momentum exchange coefficient | 1 |
| `CHL` | Leaf-atmosphere heat exchange coefficient | 1 |
| `VMAX0` | Rubisco reaction capacity | m s⁻¹ |
| `GRADM` | Slope of the net-photosynthesis-stomatal-conductance relationship | 1 |
| `BINTER` | Intercept of the net-photosynthesis-stomatal-conductance relationship | m s⁻¹ |
| `RESPCP` | Respiratory coefficient | 1 |
| `HHTI`, `HLTI` | Critical temperatures for high- and low-temperature suppression | K |

The file also contains additional photosynthesis and stomatal-response parameters (`ATHETA`, `BTHETA`, `EFFCON`, `PSICR`, and `RSTMIN`). Their numerical values are selected by `idx` in the same way.

### `SOILPARA.mat2.g66`

| Name | Meaning | Unit |
| --- | --- | --- |
| `GRCP` | Specific heat of soil | J m⁻³ |
| `DFG` | Soil thermal conductivity | W m⁻¹ K⁻¹ |
| `GWS` | Soil porosity, or saturated volumetric water content | m³ m⁻³ |
| `DFWS` | Saturated hydraulic conductivity | m s⁻¹ |
| `PSIS` | Soil matric potential at saturation | m |
| `CHB` | Index of the soil-moisture potential curve | 1 |

