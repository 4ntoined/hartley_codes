#Antoine
#gonna look at the level of the darks over temp

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt

sev_dat = np.loadtxt("seven.dat", dtype=object,skiprows=1)
sev_means = fits.open("darkmeans_7.fit")
sev_means2 = fits.open("darkmeansv2_7.fit")

eig_dat = np.loadtxt("eight.dat", dtype=object,skiprows=1)
eig_means = fits.open("darkmeans_8.fit")
eig_means2 = fits.open("darkmeansv2_8.fit")

twe_dat = np.loadtxt("twleve.dat", dtype=object,skiprows=1)
twe_means = fits.open("darkmeans_12.fit")
twe_means2 = fits.open("darkmeansv2_12.fit")

pot = [[float(sev_dat[i,5]),sev_means[0].data[i]/7000.33,sev_means2[0].data[i]/7000.33] for i in range(len(sev_dat))]
pot2 = [[float(eig_dat[i,5]),eig_means[0].data[i]/8000.33,eig_means2[0].data[i]/8000.33] for i in range(len(eig_dat))]
pot3 = [[float(twe_dat[i,5]),twe_means[0].data[i]/12000.33,twe_means2[0].data[i]/12000.33] for i in range(len(twe_dat))]
pot=np.array(pot)
pot2=np.array(pot2)
pot3=np.array(pot3)

##
fig,ax = plt.subplots()
fig.dpi=120
fig.figsize=(10,6)
ax.scatter(pot[:,0],pot[:,1],color="blue",s=1,label="7s")
#plt.show()
ax.scatter(pot2[:,0],pot2[:,1],color="red",s=1,label="8s")
#plt.show()
ax.scatter(pot3[:,0],pot3[:,1],color="green",s=1,label="12s")
ax.legend(loc="best")
ax.set_title("dark vs temperature, non-linearized")
ax.set_xlabel("temp, K (not smoothed)")
ax.set_ylabel("last frame mean/exptime (data/millisecond)")
plt.show()
##
fig,ax = plt.subplots()
fig.dpi=120
fig.figsize=(10,6)
ax.scatter(pot[:,0],pot[:,2],color="blue",s=1,label="7s")
#plt.show()
ax.scatter(pot2[:,0],pot2[:,2],color="red",s=1,label="8s")
#plt.show()
ax.scatter(pot3[:,0],pot3[:,2],color="green",s=1,label="12s")
ax.legend(loc="best")
ax.set_title("dark vs temperature, linearized")
ax.set_xlabel("temp, K (not smoothed)")
ax.set_ylabel("last frame mean/exptime (data/millisecond)")
plt.show()