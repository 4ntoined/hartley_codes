#Antoine
#FFT

import numpy as np
import scipy.fft as fff
#import scipy.optimize as opti
import matplotlib.pyplot as plt
from playingwithdata import a

### heeeey data ###
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v3fixed3px.txt",dtype=float,unpack=True,skiprows=1)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v4150km.txt",dtype=float,unpack=True,skiprows=1)
### where to look ? ###
iab = input("Give me: Index_of_First_Scan Index_of_Last_Scan  ")
ia, ib = iab.split(" ")
ia = int(ia)
ib = int(ib)
### focusing the data on the target ###
date = date[ia:ib]
h2o = h2o[ia:ib]
co2 = co2[ia:ib]
dyst = dyst[ia:ib]
### cleaning out the zeros ###
mask = np.ones(len(h2o),dtype=bool)
mask[np.argwhere(h2o < 1e-10)] = False
h2o = h2o[mask]
date = date[mask]
co2 = co2[mask]
dyst = dyst[mask]
### taking in the numbers ###
N=len(h2o)
totaltime = date[-1] - date[0]  #measured in days
delt = totaltime / N
### accounting for distance uhh ###
dists = a['comet dist'].copy()
dists = dists[ia:ib]
dists = dists[mask]
#unit here is meters which makes these numbers big so im gonna normalize
#let's call it a unit conversion
distscl = 1 / dists[0]
dists *= distscl
# now for scaling by distance
n_dist = 2
h2o = h2o / dists ** n_dist
co2 = co2 / dists ** n_dist
dyst = dyst / dists ** n_dist
### fitting ###



### into variables for plotting ###
ts = date.copy() - 2455505.083   #centering time at closest approach
xs = co2.copy()                  #taking water for now, plotted on y
ys = fff.fft(xs)                        #transformed water curve, plotted on y
fs = fff.fftfreq(N, delt)[:N//2]        #frequency for transform ?? xaxis

### plot original ###
fig,ax = plt.subplots()
fig.figsize = (10,5.6)
fig.dpi  = 140
#
ax.scatter(ts,xs,s=0.7)
ax.hlines(0,ts[0],ts[-1],linewidth = 0.7)
ax.set_title("Original, signal vs time")
ax.set_xlabel("days from encounter")
ax.set_ylabel("signal")
#
plt.show()
### plot transform ###
fig,ax = plt.subplots()
fig.figsize = (10,5.6)
fig.dpi  = 140
#
ax.plot(fs,2/N * np.abs(ys[:N//2]))
#ax.set_ylim(0,0.0001)
ax.set_title("Transform, signal vs frequency")
ax.set_xlabel("frequency (per day)")
ax.set_ylabel("signal")
#
plt.show()
### end of the road ###
