#Antoine
#gonna look for 

import numpy as np
from scipy.signal import argrelextrema
from playingwithdata import a
import matplotlib.pyplot as plt

date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v4150km.txt",dtype=float,unpack=True,skiprows=1)

mri = a['mri 7-pixel'].copy()
maxes = argrelextrema(mri, np.greater,order=5)
maxes = maxes[0]
outt = open("mri_maxes_v3.txt","w")
outt.write("index of scan, julian date at scan; mri at these points are local maxima\n")
for i in range(len(maxes)):
    outt.write(f"{maxes[i]} {date[maxes[i]]} {a['DOY'][maxes[i]]} {a['exposure id'][maxes[i]]}\n")
outt.close()

fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,h2o,color="blue",label="h2o",s=2)
ax.scatter(date,co2,color="green",label="co2",s=2)
#ax.plot(date,mri,color="darkred",label="mri")
#ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
ax.vlines(date[maxes],ymin=0,ymax=4e-3,linewidth=0.7)

#ax.set_xlim(2455495.5,2455504.5)
#ax.set_xlim(2455509.5,2455519.5)
#ax.set_ylim(-1e-16,1e-15)
#ax.set_ylim(-0.01,0.07)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
#ax.set_title("sum, 150km x 150km view")
plt.show()