#Antoine
#RGB images of dust, co2 and h2o

import numpy as np
import astropy.io.fits as fits
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as clr

pathy = input("Give me a path to a scan: ") or "all"
dat = fits.open(pathy + "/cube_gasmaps_final_v1.fit")
dat = dat[0].data
sha = dat.shape

#scaling dust down so the level of h2o far from comet
#dustscaled = dust *scl
#scl = dustscaled/dust
#just checking
dscl = dat[0,sha[1]//2,60] / dat[2,sha[1]//2,60]
#dscl *= 1e6
dat[2,:,:] *= abs(dscl)

### cropping ###
################
dat = dat[:,:,170:]
sha = dat.shape

### scaling up to ~1 ###
########################
#scaling data up from like e-5 to 1
scl = 1./dat[0,sha[1]//2,30]
dat*=scl

#uhhh in my experience [wavelength 512 / gas species 3, ysize #frames in scan, xsize 256]
#if I can figure out how to slive into the cubes
red = dat[2,:,:] #will be shape = (ysize,xsize).... dust
green = dat[1,:,:] # co2
blue = dat[0,:,:]   #h2o

## stretching ##
### we don't even need to mask the bad values, norm will literally just ignore them w/ vmin vmax

#goku is what we will plot; [M rows y, N columns x, 3 colors]
goku = np.ones((sha[1],sha[2],3))
goku[:,:,0] = red.copy() #needs to be [ysize, xsize]
goku[:,:,1] = green.copy()
goku[:,:,2] = blue.copy()

fig,(ax1,ax2,ax3,ax4) = plt.subplots(4,1,sharex=True,sharey=True)
fig.dpi=180

ax1.imshow(goku)
ax2.imshow(goku[:,:,0],cmap="Reds")
ax3.imshow(goku[:,:,1],cmap="Greens")
ax4.imshow(goku[:,:,2],cmap="Blues")

plt.show()

