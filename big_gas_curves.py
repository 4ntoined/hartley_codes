#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt
from playingwithdata import a

#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
#dateA, h2oA, co2A , dystA = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v7_11.txt",dtype=float,unpack=True,skiprows=1)
#dateA, h2oA, co2A , dystA,flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_v8_15.txt",dtype=float,unpack=True,skiprows=1)
dateA, h2oA, co2A , dystA,flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_v9_15.txt",dtype=float,unpack=True,skiprows=1)
#dateA, h2oA, co2A , dystA,flag = np.loadtxt("/home/antojr/codespace/gascurves_v8_21.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3150km.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
maxes = maxes.astype(int)

dist = a['comet dist'].copy()

y_mri = a['mri 7-pixel'].copy()

y_overdist = 1/dist
y_overdist2 = 1/dist**2
rscl1 = co2[250] / y_overdist[250]
rscl2 = co2[250] / y_overdist2[250]
y_overdist *= rscl1
y_overdist2 *= rscl2

#1 for no dist correction
y1_h2o = h2o
y1_co2 = co2
#3 for dist^2 correction
y3_h2o = y1_h2o * y_overdist2
y3_co2 = y1_co2 * y_overdist2
#A for alt, dist2
yA_h2o = h2oA * y_overdist2
yA_co2 = co2A * y_overdist2
yA_dus = dystA * y_overdist2
y_mri *= y_overdist2

#for ahearn plot comparison
#ahearn_scale = 1e-10 / 25
#yA_h2o /= ahearn_scale
#yA_co2 /= ahearn_scale
#yA_co2 *= 1.7

doyc = 2455196.5
d1,d2 = 2455505.5, 2455510.5
#d1,d2 = 2455493.5, 2455519.5
d1-=doyc
d2-=doyc

####################
####################
fig,ax = plt.subplots()
fig.figsize=(8,6)
fig.dpi=140

ax.scatter(date-doyc,yA_h2o,color="blue",label="H2O",s=25.,marker='+',linewidths = 0.7)
ax.scatter(date-doyc,yA_co2,color="green",label="CO2",s=20.,marker='x',linewidths=.7)
#ax.scatter(date-doyc,yA_co2 / yA_h2o, color="red",label="ratio",s=2.7,zorder=2)
#ax.scatter(date,yA_dus,color="red",label="dust",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date-doyc,y_mri*4.1e6,color="orange",label="MRI light curve",lw=2.5)
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes]-doyc,ymin=0,ymax=5e-5,linewidth=0.7)
#ax.hlines((1.),xmin=297,xmax=322,label="even",color='k',linewidth=1.,zorder=1)
ax.set_xlim(d1,d2)
ax.set_ylim(0,5e-10 )#/ ahearn_scale)
#ax.set_ylim(0,2.4)
#ax.legend(loc="best")
ax.set_xlabel("Day of year")
#ax.set_ylabel("$CO_2/H_2O$")
ax.set_ylabel("Flux (arbitrary units)")
#ax.set_title("Light curve for volatiles")
plt.savefig("gascurves_5days.png",dpi=fig.dpi)
plt.show(block=True)

