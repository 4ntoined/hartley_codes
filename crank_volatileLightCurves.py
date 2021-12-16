#Antoine
#light curves for the volatiles
#Antoine much later
#cranking this up
#wish i had commented the original like at all
#i was probably definitely rushing like right now

import os
import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
#from light_curve_mri import jd,flux
from playingwithdata import a

def getGases(gasmapARRAY, xnuke, ynuke, apertureradius):
    h2o = gasmapARRAY[0,:,:]
    co2 = gasmapARRAY[1,:,:]
    #excise a certain part
    h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
    c_clip = co2[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
    h_sum = np.nansum(h_clip)
    c_sum = np.nansum(c_clip)
    return h_sum, c_sum
def sortDires(row):
    cal = fits.open(row+"/cal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym
cata = []
dire = []
for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
    dire.append(paths)
    cata.append(fils)
    #no directories in these directories
dire = dire[1:] #getting rid of the first entry, the root directory
xlocs, ylocs = a['x-nucleus'].astype(int) , a['y-nucleus'].astype(int)
#need to reoganize dire so that these directories are actually in julian date order
#OBSMIDJD
dire.sort(key=sortDires)
masterMap = []
for i in range(len(dire)):
    mapp = fits.open(dire[i]+"/cube_gasmaps_v0.fit")    #gen 0 maps
    mapp = mapp[0].data
    h2o , co2 = getGases(mapp, xlocs[i], ylocs[i], 3)
    masterMap.append((h2o,co2))
gascurves = np.array(masterMap,dtype=float)
outt = open("gas_light_curve.txt","w")
outt.write("jd, h2o, co2\n")
for i in range(len(gascurves)):
    outt.write(f"{a['julian date'][i]} {gascurves[i,0]} {gascurves[i,1]}\n")
outt.close()

"""
dat = np.loadtxt("dark_temp_v2.dat",dtype=object,skiprows=1)
tims = dat[215:230,0].astype(float)

flux=flux*7e8

points = np.array(masterMap,dtype=float)

fig,ax = plt.subplots()
fig.figsize=(9,6)
fig.dpi=140

ax.scatter(tims,points[:,0],color="blue",label="h2o")
ax.scatter(tims,points[:,1],color="green",label="co2")
#ax.plot(jd,flux,color="orange",label="mri light curve")

ax.set_xlim(2455503.4,2455504.5)
ax.set_ylim(-0.01,0.07)
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("radiance")
ax.set_title("volatile light curve")
plt.show()
"""