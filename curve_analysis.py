#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Antoine

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from cometmeta import a
from datafunctions import selector
#
def expon(tyme, z, y, x):
    ans = z * np.exp( -(tyme + y)) + x
    return ans
def tx(tyme, z, y, x, w):
    ans = z* (tyme+y) **(-x) + w
    return ans
def rx(tyme, z, y, x, w):
    global a 
    ans = z* (disto + y) **(-x) + w
    return ans
#read in some data
jd, h2o, co2, dust, flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x2_15.txt",dtype=float,unpack=True,skiprows=1)
maxes, jdd, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
maxes = maxes.astype(int)
#do some more data
dist = a['comet dist'].copy()
mri = a['mri 7-pixel'].copy()
# setting up comet-s/c range
y_overdist = 1/dist
scl = 1./y_overdist[253]
y_overdist *= scl
y_overdist2 = y_overdist ** 2
# dividing out range
y1_h = h2o * y_overdist2
y1_c = co2 * y_overdist2
y1_d = dust * y_overdist2
y1_m = mri * y_overdist2
#
#expo = expon(jd, 9e-5, -2455504.5, 0.) #okay fit
goo = ~np.isnan(co2)
# cutting out nans
jdx = jd[goo]
h2ox = h2o[goo]
co2x = co2[goo]
dustx = dust[goo]

#grabbing post 
#print(jdx[201])
jdp = jdx[201:]
h2op = h2ox[201:]
co2p = co2x[201:]
dustp = dustx[201:]

guess = (4e-6, -2455508.3, 0.)
pop, pup = curve_fit(expon, jdp, h2op, p0 = guess)
z1, y1, x1 = pop
print(pop)
expo = expon(jd, z1, y1, x1)

guess2 = (1.0, -2455508.3, 2, 4e-6)
pap, pep = curve_fit(tx, jdp, h2op, p0=guess2)
z2, y2, x2, w2 = pap
print(pap)
txxx = tx(jd, z2, y2, x2, w2)


#
doyc = 2455196.5
d1,d2 = 2455505.2, 2455512.5
#d1,d2 = 2455494.5, 2455519.5
d1-=doyc
d2-=doyc

fig, ax = plt.subplots()
fig.dpi = 140
fig.figsize = (9,6)

ax.scatter(jd-doyc, y1_h, s=1.)
ax.scatter(jd-doyc, y1_c, s=1.)
ax.plot(jd-doyc, expo, color='purple')
ax.plot(jd-doyc, txxx, color='darkblue')

ax.set_xlim((d1,d2))
ax.set_ylim((-4e-8, 10000e-7))
#ax.set_xscale('')
#ax.set_yscale('')
ax.set_xlabel('Day of year')
ax.set_ylabel('Y')
ax.set_title('No title')
plt.tight_layout()
plt.show(block=False)
