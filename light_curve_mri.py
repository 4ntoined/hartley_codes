#light curves
#medium resolution i-visual data
#[0, 1, 2, 3, 4, 5, 6, 7, 8,
#9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 80, 100, 120,
#140, 160, 180, 200, 220, 240, 248]
#columns 15-49 in data, 13-47 here

import numpy as np
import matplotlib.pyplot as plt

cols = np.concatenate((np.arange(1,3),np.arange(4,49)))
tabl = np.loadtxt("calibrated_files/hartley2_photometry/data/aper_phot.tab",dtype=float,usecols=cols)
filenames, image = np.loadtxt("calibrated_files/hartley2_photometry/data/aper_phot.tab",dtype=str,usecols=(0,3),unpack=True)
#tabl has had the 1st (0th) and 4th (3rd) columns removed, all the 
#flux columns are shifted 2 down,, 14 -> 12
clear = []
clear_i = []
#print(len(tabl))
for i in range(len(tabl)):
    if image[i] == "CLEAR1": #excluding non clear1 images
        clear.append(tabl[i])
        clear_i.append(i)
#print(len(clear))
tabl = np.array(clear,dtype=float)
#replace -99 with nans
err2= np.argwhere(tabl==-99.)
#print(err[])
#print(err2)
tabl[err2[:,0],err2[:,1]] = np.nan

#getting those distance values to see what we can see
dists = tabl[:,10]
flux_dist = tabl[:,28] / (tabl[:,10]**2)
print(flux_dist)
##
fig,ax = plt.subplots()
fig.figsize=(15,8)
fig.dpi=100
#
ax.scatter(tabl[:,0],flux_dist,s=1)
#
ax.set_xlim((2455495,2455520))
#ax.set_xlim((2455503,2455508))
#ax.set_ylim((-1e-27,1e-25))
ax.set_yscale("log")
#
ax.set_xlabel("julian date")
ax.set_ylabel("flux per comet distance")
ax.set_title("mri-vis aperture data, distance controlled")
plt.show()