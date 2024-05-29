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

def view_seasonal_ssm(quarterly_datacube, cmap):
    # crs_wkt = quarterly_datacube.spatial_ref.crs_wkt
    m = Maps(ax=221,  crs=Maps.CRS.Equi7_EU)
    m2 = m.new_map(ax=222, crs=Maps.CRS.Equi7_EU)
    m3 = m.new_map(ax=223, crs=Maps.CRS.Equi7_EU)
    m4 = m.new_map(ax=224, crs=Maps.CRS.Equi7_EU)

    for i, j in enumerate([m, m2, m3, m4]):
        j.add_feature.preset.coastline()
        j.add_feature.preset.ocean()
        j.add_feature.preset.countries()

        dt = np.datetime_as_string(quarterly_datacube.isel(time=i).time.to_numpy(), unit='D')
        j.add_title(dt)
        j.set_data(quarterly_datacube.isel(time=i), x="x", y="y", parameter="band_data", crs=Maps.CRS.Equi7_EU)
        j.plot_map(cmap=cmap, zorder=3)
        j.add_colorbar(label="surface soil moisture (1)")

    # m.apply_layout(
    #     {
    #         "figsize": [6.4, 4.8],
    #         "0_map": [0.1, 0.6, 0.5, 0.4],
    #         "1_map": [0.6, 0.6, 0.5, 0.4],
    #         "2_map": [0.1, 0.1, 0.5, 0.4],
    #         "3_map": [0.6, 0.1, 0.5, 0.4],
    #     }
    # )
    m.show()