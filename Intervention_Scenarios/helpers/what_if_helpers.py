from functools import partial
from typing import Tuple

import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


def get_current_infected_ratio():
    # Returns the current ratio of infected people in germany
    number_infected = 651500  # https://www.deutschland.de/de/topic/politik/corona-in-deutschland-zahlen-und-fakten
    number_total = 83100000  # https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/_inhalt.html
    infected_ratio = number_infected / number_total
    return infected_ratio


delta_variant = cv.variant('delta', days=0)  # delta is the dominant variant in germany

# Define baseline parameters
baseline_pars = dict(
    start_day='2022-01-01',
    n_days=60,
    pop_type='hybrid',
    pop_size=10_000,
    pop_infected=int(get_current_infected_ratio() * 10000),
    location='Germany',
    use_waning=True,  # use dynamically calculated immunity
    n_beds_hosp=80,  # https://tradingeconomics.com/germany/hospital-beds - 8 per 1000 people
    n_beds_icu=62,  # https://tradingeconomics.com/germany/icu-beds - 620 per 100.000 people
    variants=[delta_variant],
)


def run_simulations(sim: cv.Sim, n_runs: int, confidence_level: float, method: str = "t") -> cv.MultiSim:
    msim = cv.MultiSim(sim)
    msim.run(n_runs=n_runs)
    if method == "t":  # use t-distribution
        bounds = st.t.interval(alpha=confidence_level, df=n_runs - 1)[1]
    else:  # use normal distribution
        bounds = st.norm.interval(alpha=confidence_level)[1]
    bounds = bounds / np.sqrt(n_runs)
    msim.mean(bounds=bounds)
    return msim


def run_base_and_intervention(base_sim: cv.Sim, intervention_sim: cv.Sim, n_runs: int = 100,
                              confidence_level: float = 0.9) -> cv.MultiSim:
    base_msim = run_simulations(base_sim, n_runs, confidence_level)
    intervention_msim = run_simulations(intervention_sim, n_runs, confidence_level)
    return cv.MultiSim([base_msim.base_sim, intervention_msim.base_sim])


# calculate by hand for reference

def calculate_mean_and_confidence(msim: cv.MultiSim, result_key: str, method: str = "t",
                                  confidence_level: float = 0.9) -> Tuple[np.array, np.array, np.array]:
    data = np.array([s.results[result_key] for s in msim.sims], dtype=float)
    data_mean = np.mean(data, axis=0)
    data_sem = st.sem(data, axis=0)
    if method == "t":
        conf_intervals = st.t.interval(alpha=confidence_level, df=data.shape[0] - 1, loc=data_mean, scale=data_sem)
    else:
        conf_intervals = st.norm.interval(alpha=confidence_level, loc=data_mean, scale=data_sem)
    lower_band, upper_band = conf_intervals
    return data_mean, lower_band, upper_band


# plot by hand for reference

def plot_with_bands(base_msim: cv.MultiSim, intervention_msim: cv.MultiSim, result_key: str, ax=None,
                    colors_base=("b", "c"), colors_intervention=("r", "tab:orange"), show_dates=False):
    if ax is None:
        _, ax = plt.subplots()
        ax.set_title(result_key)
    if show_dates:
        x = base_msim.results['date']
    else:
        x = base_msim.results['t']
    for sim, c in ((base_msim, colors_base), (intervention_msim, colors_intervention)):
        data_mean, lower_band, upper_band = calculate_mean_and_confidence(sim, result_key)
        ax.fill_between(x, lower_band, upper_band, alpha=.75, linewidth=0, label=f"{sim.label} band", color=c[1])
        ax.plot(x, data_mean, label=sim.label, color=c[0])
    if show_dates:
        cv.date_formatter(sim=base_msim.base_sim, ax=ax)
    else:
        # show intervention as vertical line
        for intervention in intervention_msim.base_sim.get_interventions():
            intervention.plot_intervention(intervention_msim.base_sim, ax)
    ax.legend()
    return ax


def _inf_thresh(self: cv.Intervention, sim: cv.Sim, thresh: int):
    ''' Dynamically define on and off days with respect to the number of infected people.
    See https://docs.idmod.org/projects/covasim/en/latest/tutorials/tut_interventions.html#Dynamic-triggering'''

    if sim.people.infectious.sum() > thresh:
        if not self.active:
            self.active = True
            self.t_on = sim.t
            self.plot_days.append(self.t_on)
    else:
        if self.active:
            self.active = False
            self.t_off = sim.t
            self.plot_days.append(self.t_off)

    return [self.t_on, self.t_off]


def inf_thresh_callback(thresh: int = 500):
    return partial(_inf_thresh, thresh=thresh)


def init_intervention_for_inf_thresh(c: cv.Intervention):
    """Setup attributes for `inf_thresh_callback`"""
    c.t_on = np.nan
    c.t_off = np.nan
    c.active = False
    c.plot_days = []
    return c
