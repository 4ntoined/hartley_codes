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

for i in range(82,len(q)):
    words = scans[i].split("/") #uhh chiron4 0 antojr 1 calibrated_ir 2 scan.dir 3
    #print(words)
    doy, expi  = words[4].split(".") # doy 0 exposureid 1
    doyi = int(doy)
    if ( (doyi >= 298) and (doyi <= 300) ) or ( (doyi >= 309) and (doyi <= 320)  ): #these scans need to have their cubes doubled in the frame direction
        #do the double
        cubed = fit.open(scans[i]+"/cube_smoothspace.fit")
        #already covered for every scan waved = fit.open(scans[i]+"/cube_wave.fit")
        hdr = cubed[0].header
        #hdr_w = waved[0].header
        cube = cubed[0].data
        #waves = waved[0].data
        nframes = cube.shape[1]
        z = np.ones((512,nframes*2,256))
        z[:,0::2,:] = cube[:,:,:].copy()
        z[:,1::2,:] = cube[:,:,:].copy()
        z=np.array(z) #maybe redundant but it makes me feel better
        #x = np.ones((512,nframes*2,256))
        #x[:,0::2,:] = waves[:,:,:].copy()
        #x[:,1::2,:] = waves[:,:,:].copy()
        #x=np.array(x)
        cubed.close()
        #waved.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_smoothspace_final.fit")
        #hduw = fit.PrimaryHDU(x,header=hdr_w)
        #hduw.writeto(scans[i]+"/cube_wave_final.fit")
        #so while we're here we will also rename the spatial_fixed into final as well
        #only these scans will have_fixed labels for the double exposure deal
        #we'll do this in the else() as well but those directories only have spatial.fit
        #so those will be renamed into final instead
        #cute = fit.open(scans[i]+"/cube_spatial_fixed.fit")
        #toe = cute[0].header
        #y = cute[0].data.copy()
        #cute.close()
        #prime = fit.PrimaryHDU(y,header=toe)
        #prime.writeto(scans[i]+"/cube_spatial_final.fit")
        #print(scans[i])
    else:
        #so what if we took this opportunity to rename all the other cubes so they're consistent all around
        #we can adopt a convention like sptatial_final and smooth_final and wave_final
        cube = fit.open(scans[i]+"/cube_smoothspace.fit")
        #waves = fit.open(scans[i]+"/cube_wave.fit")
        hdr = cube[0].header
        #hdr_w = waves[0].header
        z = cube[0].data.copy()
        #x = waves[0].data.copy()
        cube.close()
        #waves.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        #hduw = fit.PrimaryHDU(x,header=hdr_w)
        hdu.writeto(scans[i]+"/cube_smoothspace_final.fit")
        #hduw.writeto(scans[i]+"/cube_wave_final.fit")
        #okay regular spatial files now
        #cute = fit.open(scans[i]+"/cube_spatial.fit")
        #toe = cute[0].header
        #y = cute[0].data.copy()
        #cute.close()
        #prim = fit.PrimaryHDU(y,header=toe)
        #prim.writeto(scans[i]+"/cube_spatial_final.fit")
    pass

