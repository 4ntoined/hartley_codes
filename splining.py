#Antoine
#doing some experimenting with splines

import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from playingwithdata import a

rng = np.random.default_rng()
date, h2o, co2 , dus = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
dist = a['comet dist'].copy()
#unit converting distance to less annoying units
dist /= 578375.623  #is smallest distance in set
#controlling light for distance
h2o = h2o / dist**2
co2 = co2 / dist**2
dus = dus / dist**2
#splitting between approach and unproach
h2oa = h2o[:231].copy()
h2ob = h2o[231:].copy()
co2a = co2[:231].copy()
co2b = co2[231:].copy()
dus = dus[:231].copy()
dus = dus[231:].copy()
datea = date[:231].copy()
dateb = date[231:].copy()
#spline?
s1, s2 = 500, 850
spl = UnivariateSpline(dateb[s1:s2], h2ob[s1:s2],k=3,s=3.5e-14)
spl2 = UnivariateSpline(dateb[s1:s2], co2b[s1:s2],k=3,s=6.3e-13)


fig,ax = plt.subplots()
fig.figsize = (10,5.6)
fig.dpi=140

ax.scatter(dateb,h2ob,s=0.5)
ax.plot(dateb,spl(dateb),color='indigo')
#ax.scatter(dateb,co2b,s=0.5)
#ax.plot(dateb,spl2(dateb),color='red)
ax.set_ylim(( -1e-8, 1e-7 ))
ax.set_xlabel("time")
ax.set_ylabel("signal")
ax.set_title("curvy curve")
plt.show()