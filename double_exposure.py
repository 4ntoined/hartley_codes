#Antoine
#iiiii need to parse out the scans where I need to double expsoure
#and fix the cube so the smearing gives a correct field of view by doubling the data in the frame-stacking dimension
#ummm okay

import numpy as np
import os
import astropy.io.fits as fit

def doubl(datta):
    nframes = datta.shape[1]
    nwave = datta.shape[0]
    z = np.ones((nwave,nframes*2,256))
    z = np.ones((nwave,nframes*2,256))
    z[:,0::2,:] = datta[:,:,:].copy()
    z[:,1::2,:] = datta[:,:,:].copy()
    z=np.array(z) #maybe redundant but it makes me feel better
    return z

q = []
for paths, dirs,fils, in os.walk("/chiron4/antojr/calibrated_ir/"):
    q.append([paths,dirs,fils])
q = np.array(q,dtype=object)
#q[n:1] is going to be empty, 2 has files, 0 has the scan_directories
scans = q[:,0]
#scans = ["/chiron4/antojr/calibrated_ir/310.4007300"]  #for one pesky scan
files = q[:,2]
#decide if a scan doy 300 299 298 or 309 to 320
#pretty easy actually

for i in range(0,len(scans)):   #we start at one to avoid the parent directory
    words = scans[i].split("/") #uhh "" 0  chiron4 1 antojr 2 calibrated_ir 3 scan.dir 4
    #print(words)
    doy, expi  = words[4].split(".") # doy 0 exposureid 1
    doyi = int(doy)
    if i%160==0:    #progress marker
        print(i)
    if ( (doyi >= 298) and (doyi <= 300) ) or ( (doyi >= 309) and (doyi <= 320)  ): #these scans need to have their cubes doubled in the frame direction
        #do the double
        #i now need to double, spatial, wave, smooth, spacesmooth, and gasmaps nice
        dat = fit.open(scans[i]+"/cube_spatial_v1.fit")
        hdr = dat[0].header
        dat = dat[0].data
        doub_dat = doubl(dat)
        hdu = fit.PrimaryHDU(doub_dat,header=hdr)
        hdu.writeto(scans[i]+"/cube_spatial_final_v1.fit")
        # wave
        dat = fit.open(scans[i]+"/cube_wave_v1.fit")
        hdr = dat[0].header
        dat = dat[0].data
        doub_dat = doubl(dat)
        hdu = fit.PrimaryHDU(doub_dat,header=hdr)
        hdu.writeto(scans[i]+"/cube_wave_final_v1.fit")
        # smooth
        dat = fit.open(scans[i]+"/cube_smooth_v1.fit")
        hdr = dat[0].header
        dat = dat[0].data
        doub_dat = doubl(dat)
        hdu = fit.PrimaryHDU(doub_dat,header=hdr)
        hdu.writeto(scans[i]+"/cube_smooth_final_v1.fit")
        # spacesmooth
        dat = fit.open(scans[i]+"/cube_smoothspace_v1.fit")
        hdr = dat[0].header
        dat = dat[0].data
        doub_dat = doubl(dat)
        hdu = fit.PrimaryHDU(doub_dat,header=hdr)
        hdu.writeto(scans[i]+"/cube_smoothspace_final_v1.fit")
        # gasmaps
        dat = fit.open(scans[i]+"/cube_gasmaps_v1.fit")
        hdr = dat[0].header
        dat = dat[0].data
        doub_dat = doubl(dat)
        hdu = fit.PrimaryHDU(doub_dat,header=hdr)
        hdu.writeto(scans[i]+"/cube_gasmaps_final_v1.fit")
        # okay we're done
    else:
        #so what if we took this opportunity to rename all the other cubes so they're consistent all around
        #we can adopt a convention like sptatial_final and smooth_final and wave_final
        dat = fit.open(scans[i]+"/cube_spatial_v1.fit")
        hdr = dat[0].header
        z = dat[0].data.copy()
        dat.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_spatial_final_v1.fit")
        #wave
        dat = fit.open(scans[i]+"/cube_wave_v1.fit")
        hdr = dat[0].header
        z = dat[0].data.copy()
        dat.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_wave_final_v1.fit")
        # smooth
        dat = fit.open(scans[i]+"/cube_smooth_v1.fit")
        hdr = dat[0].header
        z = dat[0].data.copy()
        dat.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_smooth_final_v1.fit")
        #spacesmooth
        dat = fit.open(scans[i]+"/cube_smoothspace_v1.fit")
        hdr = dat[0].header
        z = dat[0].data.copy()
        dat.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_smoothspace_final_v1.fit")
        # gasmaps
        dat = fit.open(scans[i]+"/cube_gasmaps_v1.fit")
        hdr = dat[0].header
        z = dat[0].data.copy()
        dat.close()
        hdu = fit.PrimaryHDU(z,header=hdr)
        hdu.writeto(scans[i]+"/cube_gasmaps_final_v1.fit")
        #okay done again
    pass
