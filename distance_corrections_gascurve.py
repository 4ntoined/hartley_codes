#Antoine
#gonna use this to make the necessary corrections to my fixed phys. size aperture

import numpy as np
from matplotlib import pyplot as plt
#from cometmeta import a
from datafunctions import selector
from making_plots import plot_scatter

def figg():
    fig,ax = plt.subplots()
    fig.figsize=(10,6)
    fig.dpi=140   
    return fig, ax
def axxx(figgs, axxs, ymax=1., d1=2455512.5, d2=2455514.5):
    #axxs.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.hlines((0.),xmin=297.,xmax=322.,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.set_xlim(d1,d2)
    axxs.set_ylim(None, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    #axxs.set_ylim(-ymax*0.07, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    axxs.legend(loc="best")
    axxs.set_xlabel("Day of year")
    axxs.set_ylabel("Flux [$\propto W/m^2$]")
    #axxs.set_ylabel("$CO_2$/$H_2O$")
    #ax.set_title("")
    return
a = np.load('a_cometmeta.npy')
if __name__ == '__main__':
    
    ## load up the lc
    #curveset1 = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x5.txt',dtype=float,skiprows=1)
    #curveset2 = np.loadtxt()
    #usecurve = curveset1
    #datez, ha, ca, da, fa = usecurve[:,0],usecurve[:,1],usecurve[:,2],usecurve[:,3],usecurve[:,4]
    uncorrect_curves = np.load('/home/antojr/codespace/results_code/gascurves_x5.npy')
    ha, ca, da, flag_a = uncorrect_curves['h2o'].copy(),uncorrect_curves['co2'].copy(),uncorrect_curves['dust'].copy(),uncorrect_curves['clip flag'].copy()
    #print(uncorrect_curves[0])
    


    correcting = []
    dist_squared = a['comet dist'].copy()**2
    for i in (ha,ca,da): correcting.append( i * dist_squared )
    hb, cb, db = correcting
    #for i in range(1321):
    correcter = [ (hb[i],cb[i],db[i],flag_a[i]) for i in range(1321) ]
    correct_curves = np.array( correcter, dtype=uncorrect_curves.dtype)
    print(correct_curves[0])
    #np.save('results_code/gascurves_x5-correct-wild.npy',correct_curves)

    day_of_encounter = 2455505.0831866
    doe = day_of_encounter
    plot_scatter([ [a['julian date']-doe, ca/np.mean(ca)],[ a['julian date']-doe, cb/np.mean(cb) ] ],labels=['uncorrect','correct'], make_label=True)
    #saving our creations
    #correcter = np.ones((1321,4))
    #print(hb[0])
    #correcter = np.array( [[hb],[cb],[db],[flag_a]  ],dtype=uncorrect_curves.dtype )
    #correcter = np.concatenate(   hb.reshape((1,-1) ) )
    #print(correcter[0])
else:
    pass

"""
dateA, hA, cA, dA, flagA = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x3_424km.txt",dtype=float,unpack=True,skiprows=1)
dateB, hB, cB, dB, flagB = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x3_15.txt",dtype=float,unpack=True,skiprows=1)
date5, h5, c5, d5, flag5 = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x4_424km.txt",dtype=float,unpack=True,skiprows=1)
###########################################
## load up the aperture (and ap error) info
aper = np.load('apsizes_424800m.npy')
errs = np.load('aperror_424800m.npy')
#print(aper[800:900])
#print(errs[800:900])
#print(424800./a['pixel scale'][800:900])
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
correction1 = errs ** -2
hA1 = hA * correction1
cA1 = cA * correction1
dA1 = dA * correction1
###########################################
## SECOND correction
## correction for great change in distance across aperture sizes
#goals = abs( (pix_scl * aper) - 424800.)
#print(goals[goals < 100])
#print( comet_dist[400:700] / pix_scl[400:700])
#psize = 424800. /  aper #physical size of each pixel (kinda)
#psize = pscale * 1e5     #
#parea = psize ** 2
dist_sq = comet_dist**2
area_scale = np.mean(dist_sq)
corr1 = [hA1.copy(), cA1.copy(), dA1.copy()]
corr2 = []
for i in (0,1,2):
    gas = corr1[i]
    gas *= dist_sq
    corr2.append(gas)
hA2, cA2, dA2 = corr2
###########################################
## trying out the *R^2 correction on the fixed angle lcs
hB1 = hB * comet_dist**2
cB1 = cB * comet_dist**2
dB1 = dB * comet_dist**2
dist_scale = np.mean(comet_dist**2)
###########################################
h51 = h5 * dist_sq
c51 = c5 * dist_sq
d51 = d5 * dist_sq
###########################################


## saving information
outname = 'gascurves_x4_424km-wild.txt'
outpath = '/home/antojr/stash/datatxt/'
noters = '424800m INTERPOLATED aperture, corrected for distance, made by working_gascurves.py'
with open(outpath + outname,'w') as fil:
    fil.write('julian date, h2o, co2, dust, clipped flag // '+  noters + '\n')
    for i in range(1321):
        fil.write(f'{date5[i]} {h51[i]} {c51[i]} {d51[i]} {flag5[i]}\n')
    pass

## plotting
maxony = None
d1,d2 = 2455511.45, 2455516.05
doyc = 2455196.5
d1 -= doyc
d2 -= doyc

fig, ax = figg()

#h2os
#ax.scatter(dateA-doyc, hA, color='blue', marker='+', s=12., linewidth=0.8, label='$H_2O$ fixed phys',zorder=7)
#ax.scatter(dateA-doyc, hA1, color='purple', marker='+', s=12., linewidth=0.8, label='$H_2O$ correction 1',zorder=9)
#ax.scatter(dateA-doyc, hA2/dist_scale, color='navy', marker='+', s=12., linewidth=0.8, label='$H_2O$ correction 2',zorder=11)
#ax.scatter(dateB-doyc, hB, color='magenta', marker='+', s=12., linewidth=0.8, label='$H_2O$ fixed angle',zorder=13)
#ax.scatter(dateB-doyc, hB1/dist_scale, color='mediumslateblue', marker='+', s=12., linewidth=0.8, label='$H_2O$ fixed angle,*R2',zorder=15)
#ax.scatter(date5-doyc, h5, color='mediumslateblue', marker='+', s=12., linewidth=0.8, label='$H_2O$,424km,interp aper',zorder=15)
ax.scatter(date5-doyc, h51/dist_scale, color='mediumslateblue', marker='+', s=12., linewidth=0.8, label='$H_2O$,interp aper,correct2',zorder=15)
#ax.scatter(date5-doyc, h5/hA1, color='mediumslateblue', marker='+', s=12., linewidth=0.8, label='$H_2O$,interp aper/correct1',zorder=15)
#co2s
#ax.scatter(dateA-doyc, cA, color='green', marker='x', s=10., linewidth=0.8, label='$CO_2$ fixed phys',zorder=8)
#ax.scatter(dateA-doyc, cA1, color='darkgoldenrod', marker='x', s=10., linewidth=0.8, label='$CO_2$ correction 1',zorder=10)
#ax.scatter(dateA-doyc, cA2/dist_scale, color='darkolivegreen', marker='x', s=10., linewidth=0.8, label='$CO_2$ correction 2',zorder=12)
#ax.scatter(dateB-doyc, cB, color='green', marker='x', s=10., linewidth=0.8, label='$CO_2$ fixed angle',zorder=14)
#ax.scatter(dateB-doyc, cB1/dist_scale, color='olive', marker='x', s=10., linewidth=0.8, label='$CO_2$ fixed angle',zorder=16)
#ax.scatter(date5-doyc, c5, color='olive', marker='x', s=10., linewidth=0.8, label='$CO_2$,424km,interp aper',zorder=19)
ax.scatter(date5-doyc, c51/dist_scale, color='olive', marker='x', s=10., linewidth=0.8, label='$CO_2$,interp aper,correct2',zorder=19)
#ax.scatter(date5-doyc, c5/cA1, color='olive', marker='x', s=10., linewidth=0.8, label='$CO_2$,interp aper/correct1',zorder=19)


#ax.scatter(dateB-doyc, cA2/hA2, color='olive', marker='x', s=10., linewidth=0.8, label='ratio',zorder=17)

#ax.vlines(dateA[shift_is]-doyc, ymin=0., ymax=1., color='k', linewidth=0.5,zorder=1)

axxx(fig,ax,ymax=maxony,d1=d1,d2=d2)
plt.show(block=True)

"""

pass
