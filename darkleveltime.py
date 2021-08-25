#Antoine
#okay I wanna see the dark level over time... that's an interesting plot, no?

import numpy as np
import matplotlib.pyplot as plt

#let's get the dark in here
dark = np.loadtxt("dark_temp_v2.dat",dtype=object,skiprows=1)
timing = dark[:,0].astype(float)
darklvl = dark[:,2].astype(float)
temp = dark[:,1].astype(float)
print(darklvl[600]/temp[600])
####some graphs####
fig,ax = plt.subplots()
fig.figsize=(11,5.5)
fig.dpi=140
#
ax.plot(timing,darklvl)
#
ax.set_xlabel("julian date")
ax.set_ylabel("dark level per exposure time, DN/ms")
ax.set_title("dark level over time")
plt.show()