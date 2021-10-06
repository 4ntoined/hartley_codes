#Antoine
#sooo I need to take a cube that has been smoothed in the spectral dimension (smooth cube)
#determine the indecies(sp?) where there are the wavelengths that im interested in
#and integrate that value to get a light curve
#bro

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from playingwithdata import a

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

def measure_light(direc, loc_nucleus, aperture_size):
    #direc, is the directory where we will find a smooth cubed with an accompanying wave cube
    #loc_nucleus should be a 2-tuple (x,y) please
    #aperture_size can be a positive integer or a 2-tuple
    #getting the appropriate data
    incube = fits.open(direc + "/cube_spectralsmooth.fit")
    inwaves = fits.open(direc + "/cube_wave.fit")
    dat = incube[0].data
    waves = inwaves[0].data
    #print(dat.shape)
    #ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
    #xsize = dat.shape[2] #pixels in one (1) frame ~256
    #settling where to look in the image
    locx, locy = loc_nucleus
    if locx < 0:
        locx = 200
        locy = 20
    else:
        locx = int(locx) - 1 #transition from ds9 [1-index] to python [0-index]
        locy = int(locy) - 1
    if type(aperture_size) == tuple:    #if aperture given as (x-long, y-long)
        dx = int(aperture_size[0])
        dy = int(aperture_size[1])
    else:                               #otherwise shape is taken to be a square
        dx = int(aperture_size)
        dy = int(aperture_size)
    ddx = dx // 2                       #integer division, with rounding down
    ddy = dy // 2                       #
    if dx%2 == 1:                       #number of pixels is odd
        xdx = [locx-ddx,locx+ddx+1]     #so do this weird plus 1 to get the right number of pixels
    else:
        xdx = [locx-ddx,locx+ddx]
    if dy%2 == 1:
        ydy = [locy-ddy,locy+ddy+1]
    else:
        ydy = [locy-ddy,locy+ddy]
    #take the data from the aperture
    dat_ap = dat[:,ydy[0]:ydy[1],xdx[0]:xdx[1]].copy()
    contin = [] #where we will store the continua extracted from the full spectra w/
                #the findcontinuum function or whatever
    for xx in range(dat_ap.shape[2]):
        for yy in range(dat_ap.shape[1]):
            spec = dat_ap[:,yy,xx]
            wave = waves[:,yy,xx]
            bounds = findIRcontinuum(wave)
            contin.append(spec[bounds[0]:bounds[1]])
            pass
        pass
    ### forcing all the spectra clips to the same length
    spectra_clip_lengths = [len(i) for i in contin]
    bestie = min(spectra_clip_lengths) #length of shortest clip
    continuum = [ contin[i][:bestie] for i in range(len(contin)) ] #replace each spectra truncated to the shortest clip
    #don't forget the wavelength array, will use one wave axis for the averaged spectral clip
    d,b = findIRcontinuum(waves[:,ydy[0],xdx[0]])
    waves_x = waves[d:d+bestie,ydy[0],xdx[0]]
    #now we have to.... average these spectra let's go
    continuum = np.array(continuum)
    #average all together
    ave = np.nanmean(continuum,axis=0)
    #light = np.trapz(ave,x=waves_x)
    #or instead of trapezoidal area over the wavelength dimension, lets just add up all the flux and see
    light = np.sum(ave)
    print(f"integrated continuum from {direc}: ",light)
    return light

#going to want to pull info/data from that new structured array? yes?

#where's the continuum?
low = 1.8
hig = 2.2

direcs = ['/chiron4/antojr/codespace/seq1','/chiron4/antojr/codespace/seq2','/chiron4/antojr/codespace/seq3', '/chiron4/antojr/codespace/seq4','/chiron4/antojr/codespace/seq5','/chiron4/antojr/codespace/seq6', '/chiron4/antojr/codespace/seq7','/chiron4/antojr/codespace/seq8','/chiron4/antojr/codespace/seq9','/chiron4/antojr/codespace/seq10','/chiron4/antojr/codespace/seq11','/chiron4/antojr/codespace/seq12','/chiron4/antojr/codespace/seq13','/chiron4/antojr/codespace/seq14','/chiron4/antojr/codespace/seq15']    #list of directories where the goods are
locs = [ (a[i]['x-nucleus'],a[i]['y-nucleus'] ) for i in range(215,230)]
print(locs)
aps = np.ones((15),dtype=int)*5

#gonna run the function a bunch of times
lights = []
for i in range(len(direcs)):
    #print(measure_light(direcs[i],locs[i],aps[i]))
    lights.append(measure_light(direcs[i],locs[i],aps[i]))
    print("everybody say love")
    pass

#okay time to plot
lig_y = np.array(lights)
tim_x = a[215:230]['julian date']

#okay gonna split up the data for the plot
goo_y = np.concatenate( [lig_y[1:3], lig_y[4:8], lig_y[9:13] ])
goo_x = np.concatenate([ tim_x[1:3], tim_x[4:8], tim_x[9:13] ] )
#print(goo_y)
boo_y = np.concatenate([lig_y[0:1],lig_y[3:4],lig_y[8:9],lig_y[13:15]])
boo_x = np.concatenate([tim_x[0:1],tim_x[3:4],tim_x[8:9],tim_x[13:15]])
### plotting ###
fig,ax = plt.subplots()
fig.figsize = (10,5.625)
fig.dpi = 140

ax.scatter(goo_x,goo_y,label="w/ ir coords",color="blue")
ax.scatter(boo_x,boo_y,label="blind guess",color="purple")
ax.plot(tim_x,lig_y,color="indigo")
plt.axhline(y=0,label="zero",color="grey")

#ax.set_xlim()
#ax.set_ylim()
ax.legend(loc=3)
ax.set_xlabel("julian date")
ax.set_ylabel(f"sum of flux over {low}-{hig} micron")
ax.set_title("light curve possibly")
plt.show()

#will need to decide how i want to wrap this up/package this information
#but for now I have class
        
