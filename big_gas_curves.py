#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt
from playingwithdata import a

date, h2o, co2 = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve.txt",dtype=float,unpack=True,skiprows=1)

dist = a['comet dist'].copy()

n = 0
h2o_d = h2o / dist ** n
co2_d = co2 / dist ** n


fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,h2o_d,color="blue",label="h2o",s=2)
ax.scatter(date,co2_d,color="green",label="co2",s=2)
#ax.plot(jd,flux,color="orange",label="mri light curve")


ax.set_xlim(2455502.5,2455514.5)
#ax.set_ylim(-0.001,0.004)
#ax.set_ylim(-0.01,0.07)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("volatile light curve")
plt.show()
