#Antoine
#basic plotting the spectra

import os
from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits as fits

##########################
#pull data and wave cubes
##########################
b = []
for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
    if len(fils) < 1: #should catch the first index where its the parent directory, which has no individual files
        continue #should skip this one and move on to the next with no issue
    b.append((paths,fils))
print("the plotting program")
while 1:
    idoy = input("Day of year on scan: ")
    iexp = input("Exposure ID of scan: ")
    fname = '/chiron4/antojr/calibrated_ir/' + idoy + '.' + iexp
    try:
        icube=fits.open(fname + '/cube_spatial_final.fit')
        icube_waves=fits.open(fname + '/cube_wave_final.fit')
        icube_smo = fits.open(fname+'/cube_smooth_final.fit')
    except FileNotFoundError:
        print("\nNot found. Try again")
    else:
        break #exit input loop if cubes are read in okay

#cube
#####################
#storing fits data
##################
c1_dat = icube[0].data.copy()
c2_dat = icube_smo[0].data.copy()
waves = icube_waves[0].data.copy()

icube.close()
icube_smo.close()
icube_waves.close()

#print(c1_dat[462,10,199])
#another input loop
while 1:
    lx = int(input("x-coordinate of pixel [1-indexed]: "))
    ly = int(input("y-coordinate of pixel [1-indexed]: "))
    if lx < 1 or  lx > c1_dat.shape[2] or ly < 1 or ly > c1_dat.shape[1]:
        print("Not a valid pixel. Try again.")
    else:
        break
    pass

#what to plot?
xax = waves[:,ly-1,lx-1]
spec_1 = c1_dat[:,ly-1,lx-1]
spec_2 = c2_dat[:,ly-1,lx-1]


fig, ax = plt.subplots()
fig.figsize=(8,6)
fig.dpi=120
ax.plot(xax,spec_1,label="data",color='lightgreen')
ax.plot(xax,spec_2,label="smooth",color='lightblue')
ax.vlines((1.8,2.2,2.59,2.77,4.17,4.31),ymin=-.001, ymax=.0012)
########
ax.set_ylim((-.0001,.01))
ax.set_xlim((1.2,4.8))
#ax.set_xscale("log")
#ax.set_yscale("log")
ax.legend(loc='best')
ax.set_xlabel("wavelength (microns)")
ax.set_ylabel("data value")
ax.grid(which="both")
ax.set_title(f"spectrum {idoy}.{iexp}, y={ly},x={lx}")
#ax.set_title("temp over time")
plt.show()