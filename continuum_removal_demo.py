#Antoine Washington
#continuum removal

import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from playingwithdata import a
from resistant_mean_nan import resistant_mean

def findEmissions(wavey):
    ####this locates the wavlength indices of the bands of water and co2
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
#what directory to look for cubes?
"""
##########################
#pull data and wave cubes
##########################
b = []
for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
    if len(fils) < 1: #should catch the first index where its the parent directory, which has no individual files
        continue #should skip this one and move on to the next with no issue
    b.append((paths,fils))
print("the continuum demo program")
while 1:
    idoy = input("Day of year on scan: ")
    iexp = input("Exposure ID of scan: ")
    fname = '/chiron4/antojr/calibrated_ir/' + idoy + '.' + iexp
    try:
        icube=fits.open(fname + '/cube_spatial_final_v1.fit')
        icube_waves=fits.open(fname + '/cube_wave_final_v1.fit')
        icube_smo = fits.open(fname+'/cube_smooth_final_v2.fit')
    except FileNotFoundError:
        print("\nNot found. Try again")
    else:
        break #exit input loop if cubes are read in okay
    pass
"""

direc = input("directory with the smooth cube?: ") or '/chiron4/antojr/calibrated_ir/311.4400023_'
incube = fits.open(direc + "/cube_smooth_final_v2.fit") #cube with smooth spectra
cube2 = fits.open(direc + "/cube_spatial_final_v1.fit") 
inwaves = fits.open(direc + "/cube_wave_final_v1.fit")
#incube.info()
dat = incube[0].data
dat2=cube2[0].data

waves = inwaves[0].data
h1 = 2.59
h2 = 2.77
c1 = 4.17
c2 = 4.31
ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
xsize = dat.shape[2] #spatial pixels in one (1) frame ~256

#umm lets plot a spectrum from 307.4000013
#has 38 frames, nucleus location: 199.651 11.728
#pixx, pixy = 40+170,19
pixx, pixy = 200,12
x_waves = waves[:,pixy,pixx]
y_flux = dat[:,pixy,pixx]
y_2 = dat2[:,pixy,pixx]
emiss = findEmissions(x_waves)
hs,hl = emiss[0]
cs,cl = emiss[1]
## level of spectrum at ends of h2o band
hs_av,sig1,num1 = resistant_mean( y_flux[ hs-10:hs+1], 2.5 )
hl_av,sig2,num2 = resistant_mean( y_flux[ hl:hl+9], 2.5 )

## continuum under h2o
wave_h = x_waves[hs:hl+1]
contin_h = interp1d([h1,h2], [hs_av,hl_av],kind="linear",bounds_error=False,fill_value="extrapolate")
contin_hline = contin_h(wave_h)
h2oline = y_flux[hs:hl+1] - contin_hline

## level of spectrum at ends of co2 band
cs_av,sig3,num3 = resistant_mean( y_flux[cs-14:cs+1], 2.5 )
cl_av,sig4,num4 = resistant_mean( y_flux[cl:cl+8], 2.5 )

## continuum under co2/chiron4/antojr/calibrated_ir/307.4000015
wave_c = x_waves[cs:cl+1]
contin_c = interp1d([c1,c2], [cs_av,cl_av],kind="linear",bounds_error=False,fill_value="extrapolate")
contin_cline = contin_c(wave_c)
co2line = y_flux[cs:cl+1] - contin_cline

#highlighting where the continuum is estimated
x_hend1 = x_waves[hs-10:hs+1]
x_hend2 = x_waves[hl:hl+9]
y_hend1 = y_flux[hs-10:hs+1]
y_hend2 = y_flux[hl:hl+9]

#highlighting where the continuum is estimated
x_cend1 = x_waves[cs-14:cs+1]
x_cend2 = x_waves[cl:cl+8]
y_cend1 = y_flux[cs-14:cs+1]
y_cend2 = y_flux[cl:cl+8]



'''
pixelx,pixely = 167, 0 #add 1 to get ds9 coordinates
spect = dat[:,pixely,pixelx]
wavex = waves[:,pixely,pixelx]
print(np.logspace(-2.5,-3.5,300)[38:40])
emiss = findEmissions(wavex)
'''

'''
outcube = np.ones((2,ysize,xsize),dtype=float) #("cubes/waterPlusMaps_prototype1.fit")
for xx in range(xsize): #for each pixel in the x
    for yy in range(ysize): #take a pixel in the y
        #print(f"{xx}, {yy}")
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
        wave_h = wavex[h2os:h2ol+1] #way_fluxvelength ticks over h2o line
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
        #print(h2o,co2)
        outcube[0,yy,xx] = h2o
        outcube[1,yy,xx] = co2

fitter = fits.PrimaryHDU(outcube)
fitter.writeto(direc + "/waterPlusMaps.fit")
'''
##plotting
fig, ax1 = plt.subplots()
fig.dpi=140
fig.figsize=(12,12*9./16)
#
#ax1.hlines(0,xmin=0,xmax=5,label="zero",color='darkblue',linewidth=1.)
ax1.step(x_waves,y_2,color="red",label="spectrum")      #whole spectrum
                 #zero line
ax1.step(x_waves,y_flux,color="purple",label="spectrum")      #whole spectrum
ax1.step(x_hend1,y_hend1,color="lime")    #h2o left end
ax1.step(x_hend2,y_hend2,color="lime")    #h2o right end
ax1.step(x_cend1,y_cend1,color="lime")    #co2 left end
ax1.step(x_cend2,y_cend2,color="lime",label="endpoints")    #co2 right end
ax1.plot(wave_h,contin_hline,color="orange")   #the continuum under h2o
ax1.plot(wave_c,contin_cline,color="orange",label="continuum")   #the continuum under co2



#ax1.step(wave_h,h2oline,color="k",label="continuum removed")       #h2o continuum removed
#ax1.step(wave_c,co2line,color="k")       #co2 continuum removed



#ax2.imshow(fitter.data[1,:,:],vmin=0,vmax=9e-5)
#ax1.set_ylim((.0002,0.0012))
ax1.set_ylim((-.003,0.0025))
#ax1.set_ylim(-.002,0)
ax1.set_xlim((2.3,3.1))
#ax1.legend(loc="best")
#
#ax1.set_title(f"spectrum, 309.4008900, {pixx} {pixy}")
ax1.set_xlabel("wavelength [$\mu m$]")
ax1.set_ylabel("radiance [$W/m^2/sr/\mu m$]")
ax1.grid("both")
plt.show()
