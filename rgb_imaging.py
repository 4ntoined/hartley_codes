#Antoine
#RGB images of dust, co2 and h2o

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt

pathy = input("Give me a path to a scan: ")
dat = fits.open(pathy + "/cube_gasmaps_v1.fit")
dat = dat[0].data
sha = dat.shape

#scaling dust down so the level of h2o far from comet
#dustscaled = dust *scl
#scl = dustscaled/dust
#just checking
dscl = dat[0,sha[1]//2,60] / dat[2,sha[1]//2,60]
#dscl *= 1e6
dat[2,:,:] *= dscl

#scaling data up from like e-5 to 1
scl = 1./dat[0,sha[1]//2,200]
dat*=scl

#uhhh in my experience [wavelength 512 / gas species 3, ysize #frames in scan, xsize 256]
#if I can figure out how to slive into the cubes
red = dat[2,:,:] #will be shape = (ysize,xsize).... dust
green = dat[1,:,:] # co2
blue = dat[0,:,:]   #h2o
#goku is what we will plot; [M rows y, N columns x, 3 colors]
goku = np.ones((sha[1],sha[2],3))
goku[:,:,0] = red.copy() #needs to be [ysize, xsize]
goku[:,:,1] = green.copy()
goku[:,:,2] = blue.copy()

fig,ax = plt.subplots()
fig.dpi=140

ax.imshow(goku)

plt.show()
