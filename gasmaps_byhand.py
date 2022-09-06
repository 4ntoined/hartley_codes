#Antoine
#this is going to open a scan, choose a pixel, and remove the continuum to measure h2o and co2
################################################################################################

import numpy as np
#import 
from cometmeta import a
from scipy.interpolate import interp1d
from datafunctions import selector,selector_prompt, unloadCube
from resistant_mean_nan import resistant_mean
from crank_gasmaps import findEmissions, h1, h2, c1, c2, d1, d2

#def, go , etc
def measure_gas(spect, waves, spectrum_scani=0, xy=(-99,-99), demo=False, resist_mean=True, resist_sig=2.5, savfig=False, saveName='continuum_removal_demo_wild.png'):
    emiss = findEmissions(waves)
    h2os,h2ol = emiss[0]
    co2s,co2l = emiss[1]
    duss,dusl = emiss[2]
    #print(emiss[0],emiss[1])
    #############  h2o  ################
    ## level of spec at h2o ends
    ###editing note: apparently this was too many resistant means even though they told me to do this
    ### so im gonna undo the resistant mean and go back to np.nanmean
    ### and also reduce the number of endpoints used by 4
    #h2oshort_avg,sig1,num1 = resistant_mean( spect[ h2os-10:h2os+1], sigma_cut )   #11 points
    #h2olong_avg,sig2,num2 = resistant_mean( spect[ h2ol:h2ol+9], sigma_cut )       #9 points
    if demo:
        fig,ax1 = plt.subplots()
        fig.dpi=140
        fig.figsize=(10,5.6)
        ax1.hlines(0,xmin=0,xmax=5,label='zero',color='k',linewidth=1.)
        ax1.step(waves,spect,color='violet',label='spectrum')              #plotting the spectrum
    #okay this is changing one last time
    #we're gonna go 7,7 for water and 5,5 for CO2
    #I think Im supposed to back off water the shortward two pixels with the continuum estimation
    #I need to check my notes
    #short indices
    h2o_shor_i = (h2os-12, h2os-5)      #short h2o indices, 7 pixel, wider gap
    co2_shor_i = (co2s-8,co2s-3)       #short co2, 7->5, 
    shor_i = (h2o_shor_i,co2_shor_i)
    #print()
    #long indices
    h2o_long_i = (h2ol+6,h2ol+13)        #long h2o, 5->7 pixel, wider gap
    co2_long_i = (co2l+4, co2l+9)       #long co2, 5 pixel, only one that's unchanged from v5
    long_i = (h2o_long_i,co2_long_i)
    ## plotting the endpoints
    if demo:
        ax1.step( waves[ h2o_shor_i[0]:h2o_shor_i[1] ], spect[ h2o_shor_i[0]:h2o_shor_i[1]], color='darkblue') #h2o short 
        ax1.step( waves[ h2o_long_i[0]:h2o_long_i[1] ], spect[ h2o_long_i[0]:h2o_long_i[1]], color='darkblue') #h2o long
        ax1.step( waves[ co2_shor_i[0]:co2_shor_i[1] ], spect[ co2_shor_i[0]:co2_shor_i[1]], color='darkblue') #co2 short
        ax1.step( waves[ co2_long_i[0]:co2_long_i[1] ], spect[ co2_long_i[0]:co2_long_i[1]], color='darkblue') #co2 long
    #wavelengths in the bands
    #this should be automated to find the index of tje median of wavelength in each of the endpoint segments
    #sigh I guess that means I have to do it...
    medians = ( (h2os-9,h2ol+10), (co2s-6,co2l+7) )
    wave_h = waves[medians[0][0]:medians[0][1]] #wavelength ticks over h2o line, between endpoints' medians
    wave_c = waves[medians[1][0]:medians[1][1]]
    wave_2 = (wave_h, wave_c)
    #spectrum in gas bands
    spec_h = spect[medians[0][0]:medians[0][1]]
    spec_c = spect[medians[1][0]:medians[1][1]]
    spec_2 = (spec_h,spec_c)
    noname = ( (9,-10),(6,-7)  )
    #hold the result
    two = []
    gases = []
    #print(spec_h.size)
    for i in (0,1): #we're gonna write once and run twice for h2o and co2
        ## unloading where the bands/endpoints are
        short = shor_i[i]
        longs = long_i[i]
        wavo = wave_2[i]
        spec = spec_2[i]
        intab = noname[i]
        ## find average of those points in short and long
        if resist_mean:
            #do resistant mean procedure
            short_av,sig1,num1 = resistant_mean( spect[ short[0]:short[1] ], resist_sig)
            longs_av,sig2,num2 = resistant_mean( spect[ longs[0]:longs[1] ], resist_sig)
        else:
            short_av = np.nanmean( spect[ short[0]:short[1] ] )
            longs_av = np.nanmean( spect[ longs[0]:longs[1] ] )
        ## create a (linear) interpolation of the continuum from the endoints
        contin = interp1d([wavo[0],wavo[-1]], [short_av, longs_av], \
                            kind="linear", bounds_error=False, fill_value="extrapolate")
        ## use the interpolation to fabricate the continuum through the gas band
        contin_line = contin(wavo)
        ## subtract the fabricated continuum 
        gasline = spec - contin_line #h2o emission, with continuum removed
        if demo:
            ax1.step(wavo,contin_line,color='green')
            ax1.step(wavo,gasline,color='red')
            ax1.vlines((h1,h2,c1,c2),ymin=0,ymax=0.0014,color='k')
        inta, intb = intab
        gases.append( (gasline[inta:intb], wavo[inta:intb])  )
        gas = np.trapz(gasline[inta:intb],x=wavo[inta:intb])
        two.append(gas)
    #############  dust  ###############
    wave_d = waves[duss:dusl+1]
    dus = np.trapz( spect[duss:dusl+1], x=wave_d)
    ########## still plotting #################
    if demo:
        concern = np.nanmin( np.argwhere(waves > 2.2) )
        max_spec = np.nanmax( spect[concern:] )
        ax1.set_ylim((max_spec/-8.,max_spec*1.1))
        ax1.set_xlim((2.2,4.5))
        ax1.set_xlabel("wavelength [$\mu m$]")
        ax1.set_ylabel("radiance [$W/m^2/sr/\mu m$]")
        ax1.set_title(f"{a['julian date'][spectrum_scani]:.3f} | {a['DOY'][spectrum_scani]}.{a['exposure id'][spectrum_scani]} | {xy[0], xy[1]}")
        ax1.grid("both")
        if savfig:
            figdata = {'Software':'crank_gasmaps.py','Author':'Antoine Darius'}
            plt.savefig(saveName,dpi=fig.dpi,bbox_inches='tight',metadata=figdata)
        plt.show(block=False)
    return (two[0], two[1], dus, gases)


if __name__ == '__main__':
    #i need to unload data from a smooth cube
    #choose a pixel and retrieve the spectrum
    #find the location of H2o and co2
    #find the endpoints
    #mean the endpoints
    #draw continuum lines
    #subtract from spectrum
    #integrate results
    scani = selector_prompt()
    dats, wavs, hdr = unloadCube(scani, cubename = 'cube_smooth_final_v5.fit', wavename = 'cube_wave_final_v1.fit')
    
    ysize = dats.shape[1] #frames in one (1) scan ~16,32,etc
    xsize = dats.shape[2] #spatial pixels in one (1) frame ~256
    nx,ny = int(a['x-nucleus'][scani]), int(a['y-nucleus'][scani])
    pixo  = input(f'Which pixel? Nucleus-> {nx} {ny}\nx|0-255 y|0-{ysize-1}: ') or (nx, ny)
    if type(pixo) == str:
        pxx, pyy = pixo.split()
        pixx, pixy = (int(pxx), int(pyy))
    else:
        pixx, pixy = int(pixo[0]),int(pixo[1])
    spect = dats[:,pixy,pixx]
    waves = wavs[:,pixy,pixx]
    h2o, co2, dus, bands = measure_gas( spect, waves, spectrum_scani = scani, xy = (pixx, pixy) )
    h2olinep, co2linep = bands
    print(np.trapz( h2olinep[0], x=h2olinep[1]) )
    print( np.sum(h2olinep[0]) )
    print(h2o)
    

else:
    #print('not main')
    pass


