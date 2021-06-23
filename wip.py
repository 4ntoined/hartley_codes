#Antoine Washington
#comet stuff

from matplotlib import pyplot as plt
#import numpy as np
from astropy.io import fits as fits

##########################
#pull data and wave cubes
##########################
icube=fits.open("cubes/cube-310-data.fit")
icube_waves=fits.open("cubes/cube-310-wave.fit")
scube = fits.open("cubes/cube_smooth_spectra_310.fit")
tcube = fits.open("cubes/cube_smooth_spectra_310_v5.fit")
#icube = fits.open("cubes/cube_308_5000008_data.fit")
#icube_waves = fits.open("cubes/cube_308_5000008_wave.fit")

##########################
#pull data from individual frames
##########################
#for cube(x=200,y=10 [1-indexed]), file=17-y=7
#cube(x=201,y=18 [1-indexed]), file = 33-y=15
#ifile=fits.open("calibrated_files/308.5000008/cal_308_5000008_15.fit")

#resistant mean
#ofile=fits.open("comet_310_mean4.fit")
#another=fits.open("spec_mean41.fit")
#meanspec = fits.open("specav.fit")

#cube
#####################
#storing fits data
##################
cube_dat=icube[0].data
waves=icube_waves[0].data
scube_dat = scube[0].data
tcube_dat = tcube[0].data
#file_dat = ifile[0].data

#resist_dat = ofile[0].data
#spectral_mean_dat = meanspec[0].data

#spectra
#xax=wave[:,17,200]

#what to plot?
ds9_x = 198
ds9_y = 16
ds9_x1 = 191
ds9_y1 = 16

xax = waves[:,ds9_y-1,ds9_x-1]
spec_cube = cube_dat[:,ds9_y-1,ds9_x-1]
spec_scube = scube_dat[ds9_x-1,ds9_y-1,:]
spec_tcube = tcube_dat[:,ds9_y-1,ds9_x-1]
#xax1 = waves[:,ds9_y1-1,ds9_x1-1]
#spec_cube1 = cube_dat[:,ds9_y1-1,ds9_x1-1]

print(spec_cube[462])
print(spec_scube[462])
print(spec_tcube[462])

print(xax)
#spec_fileA=file_dat[256-ds9_x]
#spec_fileB=file_dat[200]

#spec_specmean[]
#spec_resist=resist_dat
#spec_2waymean=another[0].data


fig, ax = plt.subplots()
fig.figsize=(8,6)
fig.dpi=120
ax.plot(xax,spec_cube,label="data",color='lightgreen')
#ax.plot(xax,spec_scube,label="smoothed",color='blue',lw=1)
ax.plot(xax,spec_tcube,label="smoothed2",color='blue',lw=1)
#ax.plot(xax1,spec_cube1,label="on nucleus",color='green')
#ax.plot(temp1[15800:16000,0],temp1[15800:16000,1],label="smooth",color='orange',lw=2.)
#ax.plot(temp1[15800:16000,0],temp2[15800:16000],label="extra smooth",color='green',lw=1.)
#ax.vlines((2.59,2.77,4.17,4.31),ymin=-.001, ymax=.0012)
#ax.plot(xax,spec_fileA,label="from file")
#ax.plot(xax,resist_dat,label="spatial dimension mean")
#ax.plot(xax,spec_2waymean,label="2 way mean")
#ax.plot(wave,cube2[0].data[:,9,55],label='data',color='orange')
#ax.plot(xax,spectral_mean_dat,label='spectral mean',color='darkblue')
ax.set_ylim((-.0006,.001))
#ax.set_xscale("log")
#ax.set_yscale("log")
ax.legend(loc='best')
ax.set_xlabel("wavelength (microns)")
ax.set_ylabel("data value")
ax.grid(which="both")
ax.set_title(f"spectrum 310.4007500, y={ds9_y},x={ds9_x}")
#ax.set_title("temp over time")
plt.show()