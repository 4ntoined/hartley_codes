#Antoine
#iiiii need to parse out the scans where I need to double expsoure
#and fix the cube so the smearing gives a correct field of view by doubling the data in the frame-stacking dimension
#ummm okay

import numpy as np
import os
import astropy.io.fits as fit

q = []
for paths, dirs,fils, in os.walk("/chiron4/antojr/calibrated_ir/"):
    q.append([paths,dirs,fils])
q = np.array(q,dtype=object)
#q[n:1] is going to be empty, 2 has files, 0 has the scan_directories
scans = q[:,0]
files = q[:,2]
#decide if a scan doy 300 299 298 or 309 to 320
#pretty easy actually

for i in range(1,len(q)):
    words = scans[i].split("/") #uhh chiron4 0 antojr 1 calibrated_ir 2 scan.dir 3
    #print(words)
    doy, expi  = words[4].split(".") # doy 0 exposureid 1
    doyi = int(doy)
    if (doyi >= 298) and (doyi <= 300):
        #do the double
        cube = fit.open(scans[i]+"/cube_spatial.fit")
        cube = cube[0].data
        nframes = cube.shape[1]
        z = np.ones((512,nframes*2,256))
        z[:,0::2,:] = cube[:,:,:]
        z[:,1::2,:] = cube[:,:,:]
        z = np.array(z)
        hdu = fit.PrimaryHDU(z)
        hdu.writeto(scans[i]+"/cube_spatial_fixed.fit")
        print(scans[i])
    elif (doyi >= 309) and (doyi <= 320):
        #also do the double
        cube = fit.open(scans[i]+"/cube_spatial.fit")
        cube = cube[0].data
        nframes = cube.shape[1]
        z = np.ones((512,nframes*2,256))
        z[:,0::2,:] = cube[:,:,:]
        z[:,1::2,:] = cube[:,:,:]
        z = np.array(z)
        hdu = fit.PrimaryHDU(z)
        hdu.writeto(scans[i]+"/cube_spatial_fixed.fit")
        print(scans[i])
    pass

