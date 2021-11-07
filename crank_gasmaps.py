#Antoine Washington
#continuum removal

import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
#import matplotlib.pyplot as plt

def findEmissions(wavey):
    global h1,h2,c1,c2
    #h2o
    #short
    h2oshort2 = int(np.argwhere(wavey>=h1)[0])                  #finds all indeces exceeding the target, grabs the shortest one
    h2oshort1 = h2oshort2 - 1
    if abs(wavey[h2oshort2] - h1) < abs(wavey[h2oshort1] - h1): #higher index is closer 
        h2oshort_i = h2oshort2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        h2oshort_i = h2oshort1
    #long
    h2olong2 = int(np.argwhere(wavey>=h2)[0])                  #finds all indeces exceeding the target, grabs the longest one
    h2olong1 = h2olong2 - 1
    if abs(wavey[h2olong2] - h2) < abs(wavey[h2olong1] - h2): #higher index is closer 
        h2olong_i = h2olong2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        h2olong_i = h2olong1
    #co2
    #short
    co2short2 = int(np.argwhere(wavey>=c1)[0])                  #finds all indeces exceeding the target, grabs the shortest one
    co2short1 = co2short2 - 1
    if abs(wavey[co2short2] - c1) < abs(wavey[co2short1] - c1): #higher index is closer 
        co2short_i = co2short2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        co2short_i = co2short1
    #long
    co2long2 = int(np.argwhere(wavey>=c2)[0])                  #finds all indeces exceeding the target, grabs the longest one
    co2long1 = co2long2 - 1
    if abs(wavey[co2long2] - c2) < abs(wavey[co2long1] - c2): #higher index is closer 
        co2long_i = co2long2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        co2long_i = co2long1
    return [[h2oshort_i,h2olong_i],[co2short_i,co2long_i]]
def make_gasmaps(pathToScanDirectory):
    datf = fits.open(pathToScanDirectory + "/cube_smooth_final.fit") #cube with smooth spectra
    wavesf = fits.open(pathToScanDirectory + "/cube_wave_final.fit")
    dat_h = datf[0].header
    dat = datf[0].data.copy()
    waves = wavesf[0].data.copy()
    datf.close()
    wavesf.close()
    ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
    xsize = dat.shape[2] #pixels in one (1) frame ~256
    outcube = np.ones((2,ysize,xsize),dtype=float) #("cubes/waterPlusMaps_prototype1.fit")
    for xx in range(xsize): #for each pixel in the x
        for yy in range(ysize): #take a pixel in the y
            pixelx,pixely = xx, yy #add 1 to get ds9 coordinates
            spect = dat[:,pixely,pixelx]
            wavex = waves[:,pixely,pixelx]
            emiss = findEmissions(wavex)
            h2os,h2ol = emiss[0]
            co2s,co2l = emiss[1]
            ## level of spec at h2o ends
            h2oshort_avg = np.sum( spect[ h2os-10:h2os+1] ) / 11.
            h2olong_avg = np.sum( spect[ h2ol:h2ol+9] ) / 9.
            ## continuum of h2o
            wave_h = wavex[h2os:h2ol+1] #wavelength ticks over h2o line
            contin_h = interp1d([h1,h2],[h2oshort_avg,h2olong_avg],kind="linear",bounds_error=False,fill_value="extrapolate") #estimated continuum
            contin_hline = contin_h(wave_h) #continuum evaluated on h2o line wavelength ticks
            h2oline = spect[h2os:h2ol+1] - contin_hline #h2o emission, with continuum removed
            h2o = np.trapz(h2oline,x=wave_h)
            ## lets go co2
            co2short_avg = np.sum( spect[co2s-14:co2s+1] ) / 15.
            co2long_avg = np.sum( spect[co2l:co2l+8] ) / 8.
            ## co2 continuum
            wave_c = wavex[co2s:co2l+1]
            contin_c = interp1d([c1,c2],[co2short_avg,co2long_avg],kind="linear",bounds_error=False,fill_value="extrapolate")
            contin_cline = contin_c(wave_c)
            co2line = spect[co2s:co2l+1] - contin_cline
            co2 = np.trapz(co2line,x=wave_c)
            outcube[0,yy,xx] = h2o
            outcube[1,yy,xx] = co2
            pass
        pass
    fitter = fits.PrimaryHDU(outcube,header=dat_h)
    fitter.writeto(pathToScanDirectory + "/cube_gasmaps_v0.fit")
    return
#what directory to look for cubes?
h1 = 2.59
h2 = 2.77
c1 = 4.17
c2 = 4.31
a=[]
q=0
for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
    if len(fils) < 1: #should catch the first index where its the parent directory, which has no individual files
        continue #should skip this one and move on to the next with no issue
    a.append((paths,dirs,fils))
    make_gasmaps(paths)
    q+=1
    if q%160==0:
        print(q)
    pass
