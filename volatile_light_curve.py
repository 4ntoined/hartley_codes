#Antoine
#light curves for the volatiles

#using case study doy 307

import os
import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from light_curve_mri import jd,flux

#mapss = []
dirName = None
for paths, dirs, fils in os.walk("watermaps"):
    dirName = paths
    mapss = fils

masterMap = []
for i in mapss:
    mapp = fits.open(dirName+"/"+i)
    mapp = mapp[0].data
    h2o = mapp[0,:,:]
    co2 = mapp[1,:,:]
    #excise a certain part
    h_clip = h2o[:,179:219]
    c_clip = co2[:,179:219]
    h_sum = np.nansum(h_clip)
    c_sum = np.nansum(c_clip)
    masterMap.append([h_sum,c_sum])

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