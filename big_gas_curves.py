#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt
from playingwithdata import a

#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v2.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve.txt",dtype=float,unpack=True,skiprows=1)
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
dateA, h2oA, co2A , dystA = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v4150km.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3150km.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
maxes = maxes.astype(int)

dist = a['comet dist'].copy()

y_mri = a['mri 7-pixel'].copy()
y_mri *= 4e8

y_overdist = 1/dist
y_overdist2 = 1/dist**2
rscl1 = co2[250] / y_overdist[250]
rscl2 = co2[250] / y_overdist2[250]
y_overdist *= rscl1
y_overdist2 *= rscl2

y1_h2o = h2o
y1_co2 = co2

y2_h2o = y1_h2o * y_overdist
y2_co2 = y1_co2 * y_overdist

y3_h2o = y1_h2o * y_overdist2
y3_co2 = y1_co2 * y_overdist2

y4_h2o = h2oA
y4_co2 = co2A


d1,d2 = 2455505.5, 2455519.5

### fixed pixel ###
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y1_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y1_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
ax.vlines(date[maxes],ymin=0,ymax=8e-3,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_xlim(2455509.5,2455519.5)
ax.set_ylim(0,0.004)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed 3 pixel, no dist")
plt.show()

### fixed w distance correction ###
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
ax.vlines(date[maxes],ymin=0,ymax=5e-5,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_xlim(2455509.5,2455519.5)
ax.set_ylim(0,1e-5)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed 3 pixel, dist once")
plt.show()

### dist squared ###
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y3_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y3_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
ax.plot(date,y_mri*2e-4,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes],ymin=0,ymax=5e-5,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_xlim(2455509.5,2455519.5)
ax.set_ylim(0,1e-6)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed 3 pixels, dist-squared")
plt.show()


### moving aperture mean ###
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y4_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y4_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
ax.vlines(date[maxes],ymin=0,ymax=1e-4,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_xlim(2455509.5,2455519.5)
#ax.set_ylim(0,0.00004)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("mean, steady 150km x 150km view")
plt.show()