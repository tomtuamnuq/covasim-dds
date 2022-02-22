from typing import List

import covasim as cv
import numpy as np
import scipy.stats as st


def get_current_infected_ratio():
    # Returns the current ratio of infected people in germany
    number_infected = 651500  # https://www.deutschland.de/de/topic/politik/corona-in-deutschland-zahlen-und-fakten
    number_total = 83100000  # https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Bevoelkerungsstand/_inhalt.html
    infected_ratio = number_infected / number_total
    return infected_ratio


# Define baseline parameters
baseline_pars = dict(
    verbose=0,
    start_day='2022-01-01',
    n_days=60,
    pop_type='hybrid',
    pop_size=10_000,
    pop_infected=int(get_current_infected_ratio() * 10000),
    location='Germany',
    use_waning=True,  # use dynamically calculated immunity
    n_beds_hosp=80,  # https://tradingeconomics.com/germany/hospital-beds - 8 per 1000 people
    n_beds_icu=62  # https://tradingeconomics.com/germany/icu-beds - 620 per 100.000 people
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


def run_design_point(pars: dict, output_of_interest: str, n_runs: int, confidence_level: float = 0.9) -> float:
    """Runs one design point n_runs times and gets the output of interest on the last simulation point in time."""
    msim = run_simulations(cv.Sim(pars), n_runs, confidence_level)
    return msim.results[output_of_interest].values[-1]


def design_point_executor(par_list: List[str], output_of_interest: str = "cum_deaths", n_reps: int = 10) -> callable:
    """Creates a callable function that executes a design point."""

    def get_result_to_design_point(design_point: np.ndarray) -> float:
        design_pars = dict(zip(par_list, design_point))
        pars = {**baseline_pars, **design_pars}
        return run_design_point(pars, output_of_interest, n_reps)

    return get_result_to_design_point
