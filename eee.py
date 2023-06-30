#Antoine
#this one I want to use to sort the raw data
#we should sort by doy_exposureid
#while sorting record for each scan: exposure time, number of frames, frame size, jd of first frame
#   n/s? spacecraft-target range?

import os
import numpy as np
from astropy.io import fits

class scanner:
    def __init__(self):
        return

    def walker(self,topdir):
        #f
        p = []
        d = []
        f = []
        for a,b,c in os.walk(topdir):
            p.append(a)
            #print(c)
            #print('\n\n\n')
            f.append( [ fi for fi in c if fi.endswith(".fit") ] )
            d.append(b)
        #ind the fils
        self.scanpaths = p[1:]
        self.scanfiles = f[1:]
        return

    def scanning(self,savehere):
        for j in range(len( self.scanpaths )):
            for i in range(len(self.scanfiles[j])):
                scanscan( self.scanpaths[j] +'/' + self.scanfiles[j][i], savehere=savehere)
                print(j,i)
        return

    def blank(self):
        return

def scanscan(filepath,savehere='/alcyone1/antojr/downloading_h2/raw/'):
    #will take a filepath, open the fits file there
    #record the doy, exposure id and save the file in the appropriate place
    frame = fits.open(filepath)
    mhdr = frame[0].header
    filen = mhdr['filename'].lower()
    doy = int ( float( filepath[37:40]  ))
    hour = int( float( filen[8:10] ))
    expid = mhdr['expid']    #string
    savedir = f'{doy}_{expid}_{hour:0>2}/'
    savedir_1 = f'{doy}_{expid}_{(hour+1)%24:0>2}/'
    savedir_2 = f'{doy}_{expid}_{(hour-1)%24:0>2}/'

    if not os.path.exists( savehere+savedir ):
        #check if hour-1 or hour+1 already exists
        if os.path.exists( savehere + savedir_1) and hour!=23: #they exist:
            savedir = savedir_1
        elif os.path.exists( savehere + savedir_2 ) and hour!=00:
            savedir = savedir_2
        else:
            os.mkdir(savehere+savedir)
    
    frame.writeto(savehere+savedir+filen)
    #swit = fits.PrimaryHDU( frame[0].data )
    #swit.writeto(savehere+savedir+filen)
    return


if __name__ == '__main__':
    search_dir = '/alcyone1/antojr/downloading_h2/2010/'
    save_dir = '/alcyone1/antojr/downloading_h2/rap/'
    s1 = scanner()
    s1.walker(search_dir)
    s1.scanning(save_dir)
    
else:
    pass

"""
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
"""
