#Antoine
#sooo I need to take a cube that has been smoothed in the spectral dimension (smooth cube)
#determine the indecies(sp?) where there are the wavelengths that im interested in
#and integrate that value to get a light curve
#bro

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt

def findIRcontinuum(wave_axis):
    global low,hig
    #shorter end
    loi = int(np.argwhere( wave_axis >= low )[0])
    loi_alt = loi-1
    if abs(wave_axis[loi] - low) < abs(wave_axis[loi_alt] - low): #higher index is closer
        low_i = loi #so run withi it
    else:
        low_i  = loi_alt #otherwise use the lower index
    #longer
    hii = int(np.argwhere( wave_axis >= hig )[0])
    hii_alt = hii-1
    if abs(wave_axis[hii] - hig) < abs(wave_axis[hii_alt] - hig): #higher index is closer
        hig_i = hii #so run withi it
    else:
        hig_i = hii_alt #otherwise use the lower index
    return [low_i,hig_i] #indeces of the continuum

#where's the continuum?
low = 1.5
hig = 2.5

direc = input("directory: ")
incube = fits.open(direc + "/cube_spectralsmooth.fit")
inwaves = fits.open(direc + "/cube_wave.fit")
#
dat = incube[0].data
waves = inwaves[0].data
ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
xsize = dat.shape[2] #pixels in one (1) frame ~256

#what aperture to use?
locat = input("[x y] of nucleus: ")
locx, locy = locat.split()
locx = int(locx) - 1 #transition from ds9 [1-index] to python [0-index]
locy = int(locy) - 1
dxdy = input("[dx dy] for aperture size: ") or "5 5"
dx, dy = dxdy.split()
dx = int(dx)
dy = int(dy)
xdx = [locx,locx+dx] #between 0 and xsize
ydy = [locy,locy+dy] #b/w 0 and ysize

dat_ap = dat[:,ydy[0]:ydy[1],xdx[0]:xdx[1]].copy()
#print(dat_ap)
#numpy does the work

contin = [] #where we will store the continua extracted from the full spectra w/
            #the findcontinuum function or whatever
for xx in range(dat_ap.shape[2]):
    #hey
    for yy in range(dat_ap.shape[1]):
        spec = dat_ap[:,yy,xx]
        wave = waves[:,yy,xx]
        bounds = findIRcontinuum(wave)
        contin.append(spec[bounds[0]:bounds[1]])
#making sure all spectra clips are the same length
spectra_clip_lengths = [len(i) for i in contin]
bestie = min(spectra_clip_lengths) #length of shortest clip
continuum = [ contin[i][:bestie] for i in range(len(contin)) ] #replace each spectra truncated to the shortest clip
#don't forget the wavelength array
a,b = findIRcontinuum(waves[:,ydy[0],xdx[0]])
waves_x = waves[a:a+bestie,ydy[0],xdx[0]]

#now we have to.... average these spectra let's go
continuum = np.array(continuum)
print(continuum.shape)
#average all together
ave = np.nanmean(continuum,axis=0)
light = np.trapz(ave,x=waves_x)
print("integrated continuum: ",light)

outt = open("ir_light_307_b.txt","a")
outt.write(f"{light}\n")
outt.close()

#av_spec = np.nanmean(dat_ap,axis=(1,2))
#print(dat_alt)
#print(dat_alt.shape)

'''
### plotting ###
fig,ax = plt.subplots()
fig.figsize = (10,5.625)
fig.dpi = 140

ax.plot(waves_x,continuum[0],label="lower left pixel")
ax.plot(waves_x,ave,label="aperture average")
plt.axhline(y=0,label="zero",color="grey")

#ax.set_xlim()
#ax.set_ylim()
ax.legend(loc="best")
ax.set_xlabel("wavelength [microns]")
ax.set_ylabel("data")
ax.set_title(f"continuum cutout, integrated: {light}")
plt.show()
'''
#will need to decide how i want to wrap this up/package this information
#but for now I have class
        
