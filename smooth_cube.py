#Antoine
#would like to see if i can cook up a python solution for
#the smoothing a cube problem
#my idl code is very slow and i feel like python and  numpy arrays might
#be the way around here
#we'll see i guess

import os
import numpy as np
import astropy.io.fits as fits
from resistant_mean_nan import resistant_mean

def mean_spectrum(spectrum,sigma):
    smooth_spectrum=np.ones(512)
    for i in range(1,511):
        smooth_spectrum[i] = resistant_mean(spectrum[i-1:i+2],sigma)[0]
    smooth_spectrum[0] = resistant_mean(spectrum[0:2],sigma)[0]
    smooth_spectrum[511] = resistant_mean(spectrum[510:512],sigma)[0]
    return smooth_spectrum

def smoother(pathToScan):
    pat = pathToScan + '/cube_spatial.fit'
    dat = fits.open(pat)
    hdr = dat[0].header     #dump the header for later maybe
    dat = dat[0].data
    xsz = dat.shape[2]
    ysz = dat.shape[1]
    sig = 2.0
    smooth_dat = np.ones((512,ysz,xsz))
    for i in range(xsz):
        for j in range(ysz):
            smooth_dat[:,j,i] = mean_spectrum(dat[:,j,i],sig)            
            pass
        pass
    fitto = fits.PrimaryHDU(smooth_dat,header=hdr)
    fitto.writeto(pathToScan + '/cube_smoothpy.fit')
    return

a=[]
for p,d,f in os.walk("/chiron4/antojr/calibrated_ir"):
    a.append((p,d,f))
for i in range(1,7):
    smoother(a[i][0])
    print(i)
