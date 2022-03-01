<h2>About Covasim project</h2>

<dt>The COVID-19 pandemic has created an urgent need for models that can project epidemic trends, explore intervention scenarios, and estimate resource needs. Here we describe the methodology of Covasim (COVID-19 Agent-based Simulator), an open-source model developed to help address these questions.Covasim includes country-specific demographic information on age structure and population size; realistic transmission networks in different social layers, including households, schools, workplaces, long-term care facilities, and communities; age-specific disease outcomes; and intrahost viral dynamics, including viral-load-based transmissibility.Covasim also supports an extensive set of interventions, including non-pharmaceutical interventions, such as physical distancing and protective equipment; pharmaceutical interventions, including vaccination; and testing interventions, such as symptomatic and asymptomatic testing, isolation, contact tracing, and quarantine. These interventions can incorporate the effects of delays, loss-to-follow-up, micro-targeting, and other factors.Implemented in pure Python, Covasim has been designed with equal emphasis on performance, ease of use, and flexibility: realistic and highly customized scenarios can be run on a standard laptop in under a minute.<dt>
In this project our focus was on the Germany population with the SIR model and we used Covasim as a stochastic agent-based simulator for performing COVID-19 analyses.
 Our Global sensitivity analysis method:
 
<img src="https://github.com/AzadehKSH/Covasim-Project/blob/main/callibration%20method.PNG">
 
 Our calibration method:
 <li>
 Nelder-Mead 
 </li>
 <li> 
 Powel
 </li>
 
  <h2> Software requirements</h2>
 <li>
 Covasim <href>https://docs.idmod.org/projects/covasim/en/latest/modules.html
 </li>
 <li> 
 SALib <href>https://salib.readthedocs.io/en/latest/
 </li>
Prerequisites:
 <li>
 Numpy library <href>https://numpy.org/
 </li>
 <li> 
Scipy library <href>https://scipy.org/
 </li> 
 <li> 
Matplotlib library <href>https://matplotlib.org/
 </li>

  <h2> Refrences</h2>
 
  Covasim: <href>http://paper.covasim.org
  
   Controlling COVID-19 via test-trace-quarantine: <href> https://doi.org/10.1101/2020.07.15.20154765
