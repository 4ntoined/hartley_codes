#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt
from playingwithdata import a

#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
dateA, h2oA, co2A , dystA = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3150km.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
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

#1 for no dist correction
y1_h2o = h2o
y1_co2 = co2
#2 for dist^1 correction (wrong)
y2_h2o = y1_h2o * y_overdist
y2_co2 = y1_co2 * y_overdist
#3 for dist^2 correction
y3_h2o = y1_h2o * y_overdist2
y3_co2 = y1_co2 * y_overdist2
#A for alt, dist2
yA_h2o = h2oA * y_overdist2
yA_co2 = co2A * y_overdist2
#4 for alt, no dist
y4_h2o = h2oA
y4_co2 = co2A


d1,d2 = 2455504.5, 2455519.5
'''
###################
### fixed pixel ###
###################
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y1_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y1_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes],ymin=0,ymax=8e-3,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_ylim(0,0.004)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed pixel number, no dist")
plt.show()

###################################
### fixed w distance correction ###
###################################
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes],ymin=0,ymax=5e-5,linewidth=0.7)

ax.set_xlim(d1,d2)
#ax.set_ylim(0,1e-5)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed pixels, dist once")
plt.show()
'''
####################
### 13-pixels ###
####################
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,y3_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,y3_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri*2e-4,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes],ymin=0,ymax=5e-5,linewidth=0.7)

ax.set_xlim(d1,d2)
ax.set_ylim(-1e-11,4e-11)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed 13-pixels")
plt.show()

####################
### 7-pixel aper ###
####################
fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(date,yA_h2o,color="blue",label="h2o",s=2)
ax.scatter(date,yA_co2,color="green",label="co2",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date,y_mri*2e-4,color="orange",label="mri light curve")
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes],ymin=0,ymax=5e-5,linewidth=0.7)

ax.set_xlim(d1,d2)
ax.set_ylim(-1e-9,1e-9)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("fixed 7-pixels")
plt.show()
'''
############################
### moving aperture mean ###
############################
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
#ax.set_ylim(0,0.00004)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("mean, steady 150km x 150km view")
plt.show()
'''
