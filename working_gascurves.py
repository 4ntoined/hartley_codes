#Antoine
#gonna use this to make the necessary corrections to my fixed phys. size aperture

import numpy as np
from matplotlib import pyplot as plt
from cometmeta import a
from datafunctions import selector

def figg():
    fig,ax = plt.subplots()
    fig.figsize=(10,6)
    fig.dpi=140   
    return fig, ax
def axxx(figgs, axxs, ymax=1., d1=2455512.5, d2=2455514.5):
    #axxs.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.hlines((0.),xmin=297.,xmax=322.,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.set_xlim(d1,d2)
    axxs.set_ylim(-ymax*0.07, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    axxs.legend(loc="best")
    axxs.set_xlabel("Day of year")
    axxs.set_ylabel("Flux [$\propto W/m^2$]")
    #axxs.set_ylabel("$CO_2$/$H_2O$")
    #ax.set_title("")
    return

## load up the lc
dateA, hA, cA, dA, flagA = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x3_424km.txt",dtype=float,unpack=True,skiprows=1)
dateB, hB, cB, dB, flagB = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x3_15.txt",dtype=float,unpack=True,skiprows=1)
###########################################
## load up the aperture (and ap error) info
aper = np.load('apsizes_424800m.npy')
errs = np.load('aperror_424800m.npy')
## load in useful info from cometmeta
comet_dist = a['comet dist'].copy()
pix_scl = a['pixel scale'].copy()
###########################################
## finding where aperture size changes
shift_is = []
for i in range(len(aper)-1):
    ia, ib = aper[i], aper[i+1]
    if abs(ib-ia) > 0.0:
        shift_is.append(i)
    pass
###########################################
## FIRST correction
## correction for slight change in distance within scans of an aperture size
correction1 = errs **2
hA1 = hA * correction1
cA1 = cA * correction1
dA1 = dA * correction1
###########################################
## SECOND correction
## correction for great change in distance across aperture sizes
#goals = abs( (pix_scl * aper) - 424800.)
#print(goals[goals < 100])
#print( comet_dist[400:700] / pix_scl[400:700])
pscale = 424800. /  aper #pixel scale of each scan (after first correction)
psize = pscale * 1e5     #physical size of each pixel
parea = psize ** 2
#print(parea[400:700])
area_scale = np.mean(parea)
corr1 = [hA1.copy(), cA1.copy(), dA1.copy()]
corr2 = []
for i in (0,1,2):
    gas = corr1[i]
    gas *= parea
    corr2.append(gas)
hA2, cA2, dA2 = corr2
###########################################
## saving information
outname = 'gascurves_x3_424km-wild.txt'
outpath = '/home/antojr/stash/datatxt/'
noters = '424800m aperture, corrected for distance, made by working_gascurves'
with open(outpath + outname,'w') as fil:
    fil.write('julian date, h2o, co2, dust, clipped flag // '+  noters + '\n')
    for i in range(1321):
        fil.write(f'{dateA[i]} {hA2[i]} {cA2[i]} {dA2[i]} {flagA[i]}\n')
    pass

## plotting
maxony = 4.5e-3
d1,d2 = 2455500.45, 2455513.05
doyc = 2455196.5
d1 -= doyc
d2 -= doyc

fig, ax = figg()

#h2os
#ax.scatter(dateA-doyc, hA, color='blue', marker='+', s=12., linewidth=0.8, label='$H_2O$ fixed phys',zorder=7)
#ax.scatter(dateA-doyc, hA1, color='purple', marker='+', s=12., linewidth=0.8, label='$H_2O$ correction 1',zorder=9)
ax.scatter(dateA-doyc, hA2/area_scale, color='navy', marker='+', s=12., linewidth=0.8, label='$H_2O$ correction 2',zorder=11)
#ax.scatter(dateB-doyc, hB, color='blue', marker='+', s=12., linewidth=0.8, label='$H_2O$ fixed angle',zorder=13)
#co2s
#ax.scatter(dateA-doyc, cA, color='green', marker='x', s=10., linewidth=0.8, label='$CO_2$ fixed phys',zorder=8)
#ax.scatter(dateA-doyc, cA1, color='darkgoldenrod', marker='x', s=10., linewidth=0.8, label='$CO_2$ correction 1',zorder=10)
ax.scatter(dateA-doyc, cA2/area_scale, color='darkolivegreen', marker='x', s=10., linewidth=0.8, label='$CO_2$ correction 2',zorder=12)
#ax.scatter(dateB-doyc, cB, color='green', marker='x', s=10., linewidth=0.8, label='$CO_2$ fixed angle',zorder=12)

ax.vlines(dateA[shift_is]-doyc, ymin=0., ymax=1., color='k', linewidth=0.5,zorder=1)

axxx(fig,ax,ymax=maxony,d1=d1,d2=d2)
plt.show(block=True)

