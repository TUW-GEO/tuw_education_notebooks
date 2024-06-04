import matplotlib
import xarray as xr
import numpy as np
from pathlib import Path
from eomaps import Maps
from matplotlib.colors import LinearSegmentedColormap

def load_cmap(file: Path) -> LinearSegmentedColormap:
    def to_hex_str(c_str: str) -> str:
        r_s, g_s, b_s = c_str.split()
        return f"#{int(r_s):02x}{int(g_s):02x}{int(b_s):02x}"

    ct_lines = Path(file).read_text().splitlines()
    brn_yl_bu_colors = [to_hex_str(clr_str) for clr_str in ct_lines[:200]]
    return matplotlib.colors.LinearSegmentedColormap.from_list("", brn_yl_bu_colors)

def view_monthly_ssm(monthly_datacube, cmap):

    m = Maps(ax=221,  crs=Maps.CRS.Equi7_EU)
    m2 = m.new_map(ax=222, crs=Maps.CRS.Equi7_EU)
    m3 = m.new_map(ax=223, crs=Maps.CRS.Equi7_EU)
    m4 = m.new_map(ax=224, crs=Maps.CRS.Equi7_EU)

    STEPS = [*range(0, 12, 3)]
    for i, j in enumerate([m, m2, m3, m4]): 
        j.add_feature.preset.coastline()
        j.add_feature.preset.ocean(fc="lightgray")
        j.add_feature.preset.countries()
        dt = np.datetime_as_string(monthly_datacube.isel(time=STEPS[i]).time.to_numpy(), unit='D')
        j.add_title(dt)
        j.set_data(monthly_datacube.isel(time=STEPS[i]), x="x", y="y", parameter="band_data", crs=Maps.CRS.Equi7_EU)
        j.set_shape.shade_raster()
        j.plot_map(cmap=cmap, zorder=3)
        j.add_colorbar(label="surface soil moisture (%)", orientation="vertical")

    m.apply_layout(
        {
            "figsize": [12, 6],
            "0_map": [0.13312, 0.49336, 0.2125, 0.4],
            "1_map": [0.55585, 0.49336, 0.2125, 0.4],
            "2_map": [0.13312, 0.02, 0.2125, 0.4],
            "3_map": [0.55585, 0.02, 0.2125, 0.4],
            "4_cb": [0.38577, 0.53, 0.0915, 0.35],
            "4_cb_histogram_size": 0.8,
            "5_cb": [0.8085, 0.53, 0.0915, 0.35],
            "5_cb_histogram_size": 0.8,
            "6_cb": [0.38577, 0.11, 0.0915, 0.35],
            "6_cb_histogram_size": 0.8,
            "7_cb": [0.8085, 0.11, 0.0915, 0.35],
            "7_cb_histogram_size": 0.8,
        }
    )

    m.show()