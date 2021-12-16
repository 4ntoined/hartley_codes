#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt

date, h2o, co2 = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve.txt",dtype=float,unpack=True,skiprows=1)


fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,h2o,color="green",label="h2o",s=2)
ax.scatter(date,co2,color="red",label="co2",s=2)
#ax.plot(jd,flux,color="orange",label="mri light curve")


ax.set_xlim(2455500.1,2455504.8)
#ax.set_ylim(-0.01,0.07)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("volatile light curve")
plt.show()
