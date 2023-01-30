#Antoine
#this takes from double_exposure.py to make the functionality more robust
#feels quicker than editing that one to do what I need it to do now

import numpy as np
#import os
import astropy.io.fits as fit
#from cometmeta import a
#from datafunctions import selector, selector_prompt
def doubl(direc, in_fname='/cube_wave_v1.fit', out_fname='/cube_wave_wild.fit'):
    fil = fit.open(direc + in_fname)
    hdr = fil[0].header
    dat = fil[0].data
    fil.close()
    nframes = dat.shape[1]
    nwave = dat.shape[0]
    z = np.ones((nwave,nframes*2,256))
    z = np.ones((nwave,nframes*2,256))
    z[:,0::2,:] = dat[:,:,:].copy()
    z[:,1::2,:] = dat[:,:,:].copy()
    #z=np.array(z) #maybe redundant but it makes me feel better
    hdu = fit.PrimaryHDU( z, header=hdr)
    hdu.writeto(direc + out_fname)
    return z
def fake_doubl(direc, in_fname='mans.fit', out_fname='bro.fit'):
    fil = fit.open(direc + in_fname)
    hdr = fil[0].header
    dat = fil[0].data
    fil.close()
    z = dat.copy()
    z=np.array(z) #maybe redundant but it makes me feel better
    hdu = fit.PrimaryHDU( z, header=hdr)
    hdu.writeto(direc + out_fname)
    return z
a = np.load('/home/antojr/codespace/a_cometmeta.npy')
if __name__ == '__main__':
    go = input('What to do?\n')
    if go == '1':
        #double all the maps, make fakes for all 
        dires = a['directory path'].copy()
        doubs = a['doubled flag'].copy()
        prog_counter = 1
        sta, sto = 0, 1321
        for i in range(sta,sto):
            #doubling, smooth5, gasmaps6
            if doubs[i]:
                #smooth cube
                #doubl(dires[i],in_fname='/cube_smooth_v7.fit',out_fname='/cube_smooth_final_v7.fit')
                #gasmap
                doubl(dires[i],in_fname='/cube_gasmaps_v8.fit',out_fname='/cube_gasmaps_final_v8.fit')
                #wave file
                #doubl(dires[i],in_fname='/cube_wave_v7.fit',out_fname='/cube_wave_final_v7.fit')
            #copies
            else:
                #fake_doubl(dires[i],in_fname='/cube_smooth_v7.fit',out_fname='/cube_smooth_final_v7.fit')
                fake_doubl(dires[i],in_fname='/cube_gasmaps_v8.fit',out_fname='/cube_gasmaps_final_v8.fit')
                #fake_doubl(dires[i],in_fname='/cube_wave_v7.fit',out_fname='/cube_wave_final_v7.fit')
            #what else
            #progress counter
            if (i-sto)/(sto-sta) >= prog_counter * 0.1 :
                print(f'{(i-0)/(1321-0)*100.:.3f}% complete...')
                prog_counter+=1
            pass
        print("Okay. We're done.")
    elif go =='2':
        pass
    else:
        pass
else:
    pass
#that's alll folks

