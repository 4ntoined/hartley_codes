#Antoine
#plotting some data

import numpy as np
import matplotlib.pyplot as plt
from cometmeta import a

def figg():
    fig,ax = plt.subplots()
    fig.figsize=(10,6)
    fig.dpi=140   
    return fig, ax
def axxx(figgs, axxs, ymax=1., d1=2455512.5, d2=2455514.5):
    #axxs.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=0.6,zorder=1)
    axxs.set_xlim(d1,d2)
    axxs.set_ylim(-ymax*0.07, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    axxs.legend(loc="best")
    axxs.set_xlabel("Day of year")
    axxs.set_ylabel("Flux [$\propto W/m^2$]")
    #axxs.set_ylabel("$CO_2$/$H_2O$")
    #ax.set_title("")
    return

## unload the gas curves 
dateA, h2oA, co2A , dystA, flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x2_15.txt",dtype=float,unpack=True,skiprows=1)
dateb, h2ob, co2b , dystb,flagb = np.loadtxt("/home/antojr/stash/datatxt/gascurves_v9_15.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
maxes = maxes.astype(int)
#
dist = a['comet dist'].copy()
y_mri = a['mri 7-pixel'].copy()
#
y_overdist = 1/dist
scl = 1/y_overdist[253]
y_overdist *= scl
#rscl1 = np.sum(co2A[250:350]) / np.sum(y_overdist[250:350])
#y_overdist *= rscl1
y_overdist2 = y_overdist ** 2
"""
#1 for no dist correction
y1_h2o = h2o
y1_co2 = co2
#3 for dist^2 correction
y3_h2o = y1_h2o * y_overdist2
y3_co2 = y1_co2 * y_overdist2
"""
#A for alt, dist2
yA_h2o = h2oA #/ y_overdist2
yA_co2 = co2A #/ y_overdist2
yA_dus = dystA #/ y_overdist2

yb_h = h2ob * y_overdist2
yb_c = co2b * y_overdist2
yb_d = dystb * y_overdist2

#y_mri *= y_overdist2

#for ahearn plot comparison
#ahearn_scale = 1e-10 / 25
#yA_h2o /= ahearn_scale
#yA_co2 /= ahearn_scale
#yA_co2 *= 1.7

doyc = 2455196.5
d1,d2 = 2455507.45, 2455513.05
#d1,d2 = 2455494.5, 2455518.5
d1-=doyc
d2-=doyc

maxony = 4.4e-5

scale_new = a['dark level'].copy()
scale_old = a['dark best fit'].copy()

####################
####################
fig,ax = figg()
fig.tight_layout
#
ax.scatter(dateA-doyc,yA_h2o,color="blue",label="$H_2O$",s=14.,marker='+',linewidths = 0.6)
ax.scatter(dateA-doyc,yA_co2,color="green",label="$CO_2$",s=10.,marker='x',linewidths=0.6)
#ax.plot(dateA-doyc,y_mri*5e6,color='firebrick',label="dust/MRI", linewidth=1.6,zorder=0)

#ax.scatter(dateA-doyc, yA_co2/yA_h2o, color="purple",label="H2O",s=14.,marker='.',linewidths = 0.6)

#ax.scatter(dateb-doyc,yb_h,color="purple",label="H2O old",s=25.,marker='+',linewidths = 0.7)
#ax.scatter(dateb-doyc,yb_c,color="gold",label="CO2 old",s=20.,marker='x',linewidths=.7)
#
axxx(fig,ax, d1=d1, d2=d2, ymax=maxony)
#ax.set_xticks(np.arange(299.,323.,3.))

#saving the plot real quick
figdat = {'Author':'Antoine Darius','Software':'big_gas_curves.py'}
plotname='mrigascurve_4.png'
plotpath='/home/antojr/dps_bucket/gascurves/'
plt.savefig(plotpath + plotname, dpi=fig.dpi, metadata = figdat, bbox_inches='tight')
plt.show()

'''
fig,ax = plt.subplots()
fig.figsize=(10,6)
fig.dpi=140
fig.tight_layout
ax.scatter(dateA-doyc,(yA_h2o-yb_h)/yb_h,color="blue",label="H2O diff",s=25.,marker='+',linewidths = 0.7)
ax.scatter(dateA-doyc,(yA_co2-yb_c)/yb_c,color="green",label="CO2 diff",s=20.,marker='x',linewidths=.7)
ax.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=1.,zorder=1)
ax.set_xlim(d1,d2)
ax.set_ylim(-5,5)
ax.legend(loc="best")
ax.set_xlabel("Day of year")
ax.set_ylabel("Flux [$\propto W/m^2$]")
#ax.set_title("")
plt.show(block=False)
'''


'''
fig,ax = plt.subplots()
fig.figsize=(10,6)
fig.dpi=140
fig.tight_layout
ax.scatter(dateA-doyc, (scale_new-scale_old)/scale_old, color='fuchsia', s=2.)

ax.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=1.,zorder=1)
ax.set_xlim(d1,d2)
ax.legend(loc="best")
ax.set_xlabel("Day of year")
ax.set_ylabel("Flux [$\propto W/m^2$]")
#ax.set_title("")
plt.show(block=False)
'''

ender = input('ENTER TO WIN!!!')

### figure 
#ax.scatter(date-doyc,yb_h,color="violet",label="H2O",s=25.,marker='+',linewidths = 0.7)
#ax.scatter(date-doyc,yb_c,color="orange",label="CO2",s=20.,marker='x',linewidths=.7)

#ax.plot(dateA-doyc,yA_h2o,color="blue",label="H2O")
#ax.plot(dateA-doyc,yA_co2,color="green",label="CO2")

#ax.scatter(date-doyc,yA_co2 / yA_h2o, color="red",label="ratio",s=2.7,zorder=2)
#ax.scatter(date,yA_dus,color="red",label="dust",s=2)
#ax.scatter(date,y2_h2o,color="blue",label="h2o",s=2)
#ax.scatter(date,y2_co2,color="green",label="co2",s=2)
#ax.plot(date-doyc,y_mri*4.1e6,color="orange",label="MRI light curve",lw=2.5)
#ax.plot(date,y_overdist,color="lightblue",label="inverse comet dist.")
#ax.vlines(date[maxes]-doyc,ymin=0,ymax=5e-5,linewidth=0.7)


#ax.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=1.,zorder=1)
#ax.set_xlim(d1,d2)

#ax.set_ylim(0,2e-10 )#/ ahearn_scale)
#ax.set_ylim((-1e-7,0.2e-6))
#ax.set_ylim((-3,3))


#ax.legend(loc="best")
#ax.set_xlabel("Day of year")

#ax.set_ylabel("$CO_2/H_2O$")


#ax.set_ylabel("Flux [$\propto W/m^2$]")
#ax.set_title("Light curve for volatiles")
#plt.savefig("comparing_new_old_h2olightcurve.png",dpi=fig.dpi,bbox_inches='tight')


#plt.show(block=True)

