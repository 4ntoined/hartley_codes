#Antoine Washington
#continuum removal

import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector,selector_prompt
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
h1 = 2.59
h2 = 2.77
c1 = 4.17
c2 = 4.31
ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
xsize = dat.shape[2] #spatial pixels in one (1) frame ~256

#umm lets plot a spectrum from 307.4000013
#has 38 frames, nucleus location: 199.651 11.728
#pixx, pixy = 40+170,19
pixx, pixy = 200,13
x_waves = waves[:,pixy,pixx]
y_flux = dat[:,pixy,pixx]
y_2 = dat2[:,pixy,pixx]
emiss = findEmissions(x_waves)
hs,hl = emiss[0]
cs,cl = emiss[1]
## level of spectrum at ends of h2o band
hs_av = np.nanmean( y_flux[ hs-10:hs-3])
hl_av = np.nanmean( y_flux[ hl+4:hl+9])

## continuum under h2o
wave_h = x_waves[hs-7:hl+7]
#wave_h = x_waves[hs:hl+1]
contin_h = interp1d([wave_h[0],wave_h[-1]], [hs_av,hl_av],kind="linear",bounds_error=False,fill_value="extrapolate")
contin_hline = contin_h(wave_h)
h2oline = y_flux[hs-7:hl+7] - contin_hline

## level of spectrum at ends of co2 band
cs_av= np.nanmean( y_flux[cs-10:cs-3])
cl_av= np.nanmean( y_flux[cl+4:cl+9])

## continuum under co2/chiron4/antojr/calibrated_ir/307.4000015
wave_c = x_waves[cs-7:cl+7]
contin_c = interp1d([wave_c[0],wave_c[-1]], [cs_av,cl_av],kind="linear",bounds_error=False,fill_value="extrapolate")
contin_cline = contin_c(wave_c)
co2line = y_flux[cs-7:cl+7] - contin_cline

#highlighting where the continuum is estimated
x_hend1 = x_waves[hs-10:hs-3]
x_hend2 = x_waves[hl+4:hl+9]
y_hend1 = y_flux[hs-10:hs-3]
y_hend2 = y_flux[hl+4:hl+9]

#highlighting where the continuum is estimated
x_cend1 = x_waves[cs-10:cs-3]
x_cend2 = x_waves[cl+4:cl+9]
y_cend1 = y_flux[cs-10:cs-3]
y_cend2 = y_flux[cl+4:cl+9]





##plotting
fig, ax1 = plt.subplots()
fig.dpi=140
fig.figsize=(12,12*9./16)
#
#ax1.hlines(0,xmin=0,xmax=5,label="zero",color='darkblue',linewidth=1.)
#ax1.step(x_waves,y_2,color="red",label="spectrum")      #whole spectrum
                 #zero line
ax1.step(x_waves,y_flux,color="purple",label="spectrum")      #whole spectrum
ax1.step(x_hend1,y_hend1,color="lime")    #h2o left end
ax1.step(x_hend2,y_hend2,color="lime")    #h2o right end
ax1.step(x_cend1,y_cend1,color="lime")    #co2 left end
ax1.step(x_cend2,y_cend2,color="lime",label="endpoints")    #co2 right end
ax1.plot(wave_h,contin_hline,color="orange")   #the continuum under h2o
ax1.plot(wave_c,contin_cline,color="orange",label="continuum")   #the continuum under co2

ax1.vlines((1.8,2.2,2.59,2.77,4.17,4.31),ymin=-.001, ymax=.0012)

#ax1.step(wave_h,h2oline,color="k",label="continuum removed")       #h2o continuum removed
#ax1.step(wave_c,co2line,color="k")       #co2 continuum removed



#ax2.imshow(fitter.data[1,:,:],vmin=0,vmax=9e-5)
#ax1.set_ylim((.0002,0.0012))
ax1.set_ylim((-.0001,.0015))
ax1.set_xlim((2.2,4.5))
#ax1.set_ylim(-.002,0)
#ax1.set_xlim((2.3,3.1))
#ax1.legend(loc="best")
#
#ax1.set_title(f"spectrum, 309.4008900, {pixx} {pixy}")
ax1.set_xlabel("wavelength [$\mu m$]")
ax1.set_ylabel("radiance [$W/m^2/sr/\mu m$]")
ax1.grid("both")
plt.show()
