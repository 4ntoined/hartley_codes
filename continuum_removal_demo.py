#Antoine
#this will demo the continuum removal given a scan and a partcular pixel to plot
#
#########################################################################################################################################
import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector,selector_prompt
from resistant_mean_nan import resistant_mean
from crank_gasmaps import findEmissions, measure_gas

def shrug():
    return

spec_name_1 = '/cube_smooth_v1.fit'
wave_name   = '/cube_wave_v1.fit'

### choosing a scan, by: index [0-1320]?, exposureid+DOY? [xxx yyyyyyy/y], julian date[2455494-2455517], directory
#direc= input("directory with the smooth cube?: ") or '/chiron4/antojr/calibrated_ir/312.4300015'
scani = selector_prompt()
direc = a['directory path'][scani]
c1 = fits.open(direc + spec_name_1) #cube with smooth spectra
cw = fits.open(direc + wave_name)
da1 = c1[0].data
wav = cw[0].data
#h1 = 2.59
#h2 = 2.77
#c1 = 4.17
#c2 = 4.31
ysize = da1.shape[1] #frames in one (1) scan ~16,32,etc
xsize = da1.shape[2] #spatial pixels in one (1) frame ~256
nx,ny = int(a['x-nucleus'][scani]), int(a['y-nucleus'][scani])
pixo  = input(f'Which pixel? Nucleus-> {nx} {ny}\nx|0-255 y|0-{ysize-1}: ') or (nx, ny)

#umm lets plot a spectrum from 307.4000013
#has 38 frames, nucleus location: 199.651 11.728
#pixx, pixy = 40+170,19
if type(pixo) == str:
    pxx, pyy = pixo.split()
    pixx, pixy = (int(pxx), int(pyy))
else:
    pixx, pixy = int(pixo[0]),int(pixo[1])
spec = da1[:,pixy,pixx]
wave = wav[:,pixy,pixx]
go = measure_gas( spec, wave, demo=True )

