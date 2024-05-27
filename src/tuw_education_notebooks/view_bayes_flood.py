from eomaps import Maps
import numpy as np

from tuw_education_notebooks.calc_bayes_flood import calc_water_likelihood, calc_land_likelihood

RANGE = np.arange(-30, 0, 0.1)

def view_bayes_flood(sig0_dc, calc_posteriors=None, bayesian_flood_decision=None):

    # initialize a map on top
    m = Maps(ax=122, layer="data")

    # initialize 2 matplotlib plot-axes below the map
    ax_upper = m.f.add_subplot(221)
    ax_upper.set_ylabel("likelihood")
    ax_upper.set_xlabel("$\sigma^0 (dB)$")

    ax_lower = m.f.add_subplot(223)
    ax_lower.set_ylabel("probability")
    ax_lower.set_xlabel("$\sigma^0 (dB)$")

    # -------- assign data to the map and plot it
    if bayesian_flood_decision is not None:
        # add map
        m2 = m.new_layer(layer="map")
        m2.add_wms.OpenStreetMap.add_layer.default()
        flood_classification =  bayesian_flood_decision(sig0_dc.id, sig0_dc.SIG0)
        sig0_dc["decision"] = (('y', 'x'), flood_classification.reshape(sig0_dc.SIG0.shape))
        sig0_dc["decision"] = sig0_dc.decision.where(sig0_dc.SIG0.notnull())
        sig0_dc["decision"] = sig0_dc.decision.where(sig0_dc.decision==0)
        m.set_data(data=sig0_dc, x="x", y="y", parameter="decision", crs=sig0_dc.spatial_ref.crs_wkt)
        m.plot_map()
        m.show_layer("map", ("data", 0.5))
    else:
        m.set_data(data=sig0_dc, x="x", y="y", parameter="SIG0", crs=sig0_dc.spatial_ref.crs_wkt)
        m.plot_map()

    # -------- define a custom callback function to update the plots
    def update_plots(ID, **kwargs):
        
        # get the data
        value = sig0_dc.where(sig0_dc.id == ID, drop=True).SIG0.to_numpy()
        y1_pdf, y2_pdf = calc_water_likelihood(ID, RANGE), calc_land_likelihood(ID, RANGE)

        # plot the lines and vline
        (water,) = ax_upper.plot(RANGE, y1_pdf, 'k-', lw=2, label="water")
        (land,) = ax_upper.plot(RANGE, y2_pdf,'r-', lw=5, alpha=0.6, label="land")
        value_left = ax_upper.vlines(x=value, ymin=0, ymax=np.max((y1_pdf, y2_pdf)), lw=3, label="observed")
        ax_upper.legend(loc="upper left")

        # add all artists as "temporary pick artists" so that they
        # are removed when the next datapoint is selected
        for a in [water, land, value_left]:
            m.cb.pick.add_temporary_artist(a)

        if calc_posteriors is not None:
            f_post, nf_post = calc_posteriors(y1_pdf, y2_pdf)
            (f,) = ax_lower.plot(RANGE, f_post, 'k-', lw=2, label="flood")
            (nf,) = ax_lower.plot(RANGE, nf_post,'r-', lw=5, alpha=0.6, label="non-flood")
            value_right = ax_lower.vlines(x=value, ymin=-0.1, ymax=1.1, lw=3, label="observed")
            ax_lower.legend(loc="upper left")
            for a in [f, nf, value_right]:
                m.cb.pick.add_temporary_artist(a)

        # re-compute axis limits based on the new artists
        ax_upper.relim()
        ax_upper.autoscale()

    m.cb.pick.attach(update_plots)
    m.cb.pick.attach.mark(permanent=False, buffer=1, fc="none", ec="r")
    m.cb.pick.attach.mark(permanent=False, buffer=2, fc="none", ec="r", ls=":")

    m.apply_layout(
        {
            "figsize": [9, 4.8],
            "0_map": [0.5, 0.1, 1, 0.8],
            "1_": [0.1, 0.1, 0.35, 0.3],
            "2_": [0.1, 0.6, 0.35, 0.3],
        }
    )
    m.show()