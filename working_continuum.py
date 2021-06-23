#Antoine Washington
#continuum removal

import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

checking = False
def findEmissions(wavey):
    global h1,h2,c1,c2,checking
    #toler = [3e-3,2.5e-3,2.3e-3,2e-3,1.56e-3,1.5e-3,1e-3,7e-4]
    toler = np.logspace(-2.5,-3.5,130)
    #for i in range(len(toler)):
    i = 0
    while len(np.argwhere(np.isclose(wavey,h1,rtol=toler[i]))) >= 1:
        #oh boy so this will check how many indeces fit the bill
        # its last run will be before the check returns no indices
        h2oshort_i = np.argwhere(np.isclose(wavey,h1,rtol=toler[i]))
        i+=1
        if i == len(toler)-2:
            break
    if len(h2oshort_i) > 1:
        print(f"choose from {len(h2oshort_i)} i's.")
        h2oshort_i = int(h2oshort_i[1])
    elif len(h2oshort_i) == 1:
        h2oshort_i = int(h2oshort_i)
    #
    i=0
    while len(np.argwhere(np.isclose(wavey,h2,rtol=toler[i]))) >= 1:
        #oh boy so this will check how many indeces fit the bill
        # its last run will be before the check returns no indices
        h2olong_i = np.argwhere(np.isclose(wavey,h2,rtol=toler[i]))
        i+=1
        if i == len(toler)-2:
            break
    if len(h2olong_i) > 1:
        print(f"choose from {len(h2olong_i)} i's.")
        h2olong_i = int(h2olong_i[1])
    elif len(h2olong_i) == 1:
        h2olong_i = int(h2olong_i)
    #
    i = 0
    while len(np.argwhere(np.isclose(wavey,c1,rtol=toler[i]))) >= 1:
        #oh boy so this will check how many indeces fit the bill
        # its last run will be before the check returns no indices
        co2short_i = np.argwhere(np.isclose(wavey,c1,rtol=toler[i]))
        i+=1
        if i == len(toler)-2:
            break
    if len(co2short_i) > 1:
        print(f"choose from {len(co2short_i)} i's.")
        co2short_i = int(co2short_i[1])
    elif len(co2short_i) == 1:
        co2short_i = int(co2short_i)
    #
    i=0
    while len(np.argwhere(np.isclose(wavey,c2,rtol=toler[i]))) >= 1:
        #oh boy so this will check how many indeces fit the bill
        # its last run will be before the check returns no indices
        co2long_i = np.argwhere(np.isclose(wavey,c2,rtol=toler[i]))
        i+=1
        if i == len(toler)-2:
            break
    if len(co2long_i) > 1:
        print(f"choose from {len(co2long_i)} i's.")
        co2long_i = int(co2long_i[1])
    elif len(co2long_i) == 1:
        co2long_i = int(co2long_i)
    #
        
        '''
        if len(h2oshort_i) == 1: #recording index and breaking for loop
            h2oshort_i = int(h2oshort_i)
            print("got h2o short end")
            break
        if len(h2oshort_i) >= 2: #will run until 1 or fewer indicies left
            h2oshort_i = int(h2oshort_i[1])
    #
    for i in range(len(toler)):
        h2olong_i = np.argwhere(np.isclose(wavey,h2,rtol=toler[i]))
        if len(h2olong_i) == 1: #recording index and breaking for loop
            h2olong_i = int(h2olong_i)
            print("got h2o long end")
            break
        if len(h2olong_i) >= 2: #when there are 2 left record them
            h2olong_i = int(h2olong_i[1])
    #
    for i in range(len(toler)):
        co2short_i = np.argwhere(np.isclose(wavey,c1,rtol=toler[i]))
        if len(co2short_i) == 1: #recording index and breaking for loop
            co2short_i = int(co2short_i)
            print("got co2 short end")
            break
        if len(co2short_i) >= 2: #when there are 2 left record them
            co2short_i = int(co2short_i[1])
    #
    for i in range(len(toler)):
        co2long_i = np.argwhere(np.isclose(wavey,c2,rtol=toler[i]))
        if len(co2long_i) == 1: #recording index and breaking for loop
            co2long_i = int(co2long_i)
            print("got co2 long end")
            break
        if len(co2long_i) >= 2: #when there are 2 left record them
            co2long_i = int(co2long_i[1])
    #
    
    '''
    return [[h2oshort_i,h2olong_i],[co2short_i,co2long_i]]

incube = fits.open("cubes/cube_smooth_spectra_310_v5.fit") #cube with smooth spectra
inwaves = fits.open("cubes/cube-310-wave.fit")
incube.info()
dat = incube[0].data
waves = inwaves[0].data
h1 = 2.59
h2 = 2.77
c1 = 4.17
c2 = 4.31
ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
xsize = dat.shape[2] #pixels in one (1) frame ~256

print(findEmissions(waves[:,16,196]))
#print(wavex[330:349])
#print(findEmissions(wavex))
'''
pixelx,pixely = 167, 0 #add 1 to get ds9 coordinates
spect = dat[:,pixely,pixelx]
wavex = waves[:,pixely,pixelx]
print(np.logspace(-2.5,-3.5,300)[38:40])
emiss = findEmissions(wavex)
'''
outcube = np.ones((2,ysize,xsize),dtype=float) #("cubes/waterPlusMaps_prototype1.fit")
for xx in range(xsize): #for each pixel in the x
    for yy in range(ysize): #take a pixel in the y
        print(f"{xx}, {yy}")
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
        print(h2o,co2)
        outcube[0,yy,xx] = h2o
        outcube[1,yy,xx] = co2

fitter = fits.PrimaryHDU(outcube)
fitter.writeto("cubes/waterPlusMaps_prototype1.fit")

'''
#thinking we maybe should define a function that can progressively test smaller tolerances until only a single index is left
h2oshort_index = np.argwhere(np.isclose(wavex,h1,rtol=1.5e-3))
h2olong_index = np.argwhere(np.isclose(wavex,h2,rtol=1.5e-3))
co2short_index = np.argwhere(np.isclose(wavex,c1,rtol=1.5e-3))
co2long_index = np.argwhere(np.isclose(wavex,c2,rtol=1.5e-3))
##print(h2oshort_index,h2olong_index,co2short_index,co2long_index)
        '''
'''
##settling h2o
h2oshort_avg = np.sum( spect[ int(h2oshort_index)-10:int(h2oshort_index)+1] ) / 11.
h2olong_avg = np.sum( spect[ int(h2olong_index):int(h2olong_index)+9] ) / 9.
##print(h2oshort_avg,h2olong_avg)
wave_h = wavex[int(h2oshort_index):int(h2olong_index)+1]
contin_h = interp1d([h1,h2],[h2oshort_avg,h2olong_avg],kind="linear")
contin_hline = contin_h(wave_h)

h2o = spect[int(h2oshort_index):int(h2olong_index)+1] - contin_hline
print(h2o)

##settling co2
co2short_avg = np.sum( spect[ int(co2short_index)-14:int(co2short_index)+1] ) / 15.
co2long_avg = np.sum( spect[ int(co2long_index):int(co2long_index)+8] ) / 8.
wave_c = wavex[int(co2short_index):int(co2long_index)+1]
contin_c = interp1d([c1,c2],[co2short_avg,co2long_avg],kind='linear',bounds_error=False,fill_value="extrapolate")
contin_cline = contin_c(wave_c)
co2 = spect[int(co2short_index):int(co2long_index)+1] - contin_cline
print(co2)
'''
##print(np.linspace(h1,h2,int(h2olong_index)-int(h2oshort_index)+1),"\n\n",wavex[int(h2oshort_index):int(h2olong_index)+1])
##plotting
fig,ax = plt.subplots()
fig.dpi=120
fig.figsize=(9,6)
#
ax.plot(wavex,spect,color="blue")
ax.plot(wave_h,contin_hline)
ax.plot(wave_h,h2oline)
ax.plot(wave_c,contin_cline)
ax.plot(wave_c,co2)
ax.vlines((h1,h2,c1,c2),ymin=-0.001,ymax=0.0012,color='pink')
#
#ax.set_xlim((2.,4.4))
ax.set_ylim((-.0006,.001))
ax.set_ylabel("data value")
ax.set_xlabel("wavelength, microns")
ax.set_title("spectrum")
ax.grid("both")