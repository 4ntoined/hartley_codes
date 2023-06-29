#Antoine
#this one I want to use to sort the raw data
#we should sort by doy_exposureid
#while sorting record for each scan: exposure time, number of frames, frame size, jd of first frame
#   n/s? spacecraft-target range?

import os
import numpy as np
from astropy.io import fits

def scanscan(filepath,savehere='/alcyone1/antojr/downloading_h2/raw/'):
    #will take a filepath, open the fits file there
    #record the doy, exposure id and save the file in the appropriate place

    frame = fits.open(filepath)
    mhdr = frame[0].header
    filen = mhdr['filename'].lower()
    doy = filepath[37:40]  
    hour = int( float( filen[8:10] ))
    expid = mhdr['expid']    #string
    savedir = f'{doy}_{expid}_{hour}/'
    savedir_1 = f'{doy}_{expid}_{(hour+1)%24}/'
    savedir_2 = f'{doy}_{expid}_{(hour-1)%24}/'

    if not os.path.exists( savehere+savedir ):
        #check if hour-1 or hour+1 already exists
        if os.path.exists( savehere + savedir_1): #they exist:
            savedir = savedir_1
        elif os.path.exists( savehere + savedir_2 ):
            savedir = savedir_2
        else:
            os.mkdir(savehere+savedir)
    
    frame.writeto(savehere+savedir+filen)
    #swit = fits.PrimaryHDU( frame[0].data )
    #swit.writeto(savehere+savedir+filen)
    return

search_dir = '/alcyone1/antojr/downloading_h2/2010/'
paths = []
dirs = []
fils = []
for a,b,c in os.walk(search_dir):
    paths.append(a)    
    #print(c)
    #print('\n\n\n')
    fils.append( [ fi for fi in c if fi.endswith(".fit") ] )
    dirs.append(b)
#
paths = paths[1:]
fils = fils[1:]
#
#need to remove non-fits files from fils[:]
#print(fils[0])
#nfils = [ fi for fi in fils if fi.endswith(".fit")  ]
#print(fils[:2])

print(paths[0])
print(fils[0])

for j in range(len(paths)):
    for i in range(len(fils[j])):
        scanscan( paths[j] +'/' + fils[j][i] )
        print(j,i)
#print(len(paths))
#print(len(fils))



