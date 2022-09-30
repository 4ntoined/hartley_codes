#Antoine
#this code will take in some amount of cubes, and return as many gasmaps
#other editorial notes
##################################################################################################################################
import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
from cometmeta import a
from datafunctions import selector_prompt, selector
from resistant_mean_nan import resistant_mean
import matplotlib.pyplot as plt
def findEmissions(wavey):
    global h1,h2,c1,c2,d1,d2
    ############  h2o  ###############
    #short
    h2oshort2 = int(np.argwhere(wavey>=h1)[0])                  #finds all indeces exceeding the target, grabs the shortest one
    h2oshort1 = h2oshort2 - 1
    if abs(wavey[h2oshort2] - h1) < abs(wavey[h2oshort1] - h1): #higher index is closer 
        h2oshort_i = h2oshort2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        h2oshort_i = h2oshort1
    #long
    h2olong2 = int(np.argwhere(wavey>=h2)[0])                  #finds all indeces exceeding the target, grabs the longest one
    h2olong1 = h2olong2 - 1
    if abs(wavey[h2olong2] - h2) < abs(wavey[h2olong1] - h2): #higher index is closer 
        h2olong_i = h2olong2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        h2olong_i = h2olong1
    ############  co2  ###############
    #short
    co2short2 = int(np.argwhere(wavey>=c1)[0])                  #finds all indeces exceeding the target, grabs the shortest one
    co2short1 = co2short2 - 1
    if abs(wavey[co2short2] - c1) < abs(wavey[co2short1] - c1): #higher index is closer 
        co2short_i = co2short2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        co2short_i = co2short1
    #long
    co2long2 = int(np.argwhere(wavey>=c2)[0])                  #finds all indeces exceeding the target, grabs the longest one
    co2long1 = co2long2 - 1
    if abs(wavey[co2long2] - c2) < abs(wavey[co2long1] - c2): #higher index is closer 
        co2long_i = co2long2                                  #so take that one
    else:                                                       #in the case of a tie, we go with the lower index
        co2long_i = co2long1
    ############  dust  ###############
    #short
    dshort2 = int(np.argwhere(wavey>=d1)[0])
    dshort1 = dshort2 -1
    if abs(wavey[dshort2] - d1) < abs(wavey[dshort1] - d1):
        dshort_i = dshort2
    else:
        dshort_i = dshort1
    #long
    dlong2 = int(np.argwhere(wavey>=d2)[0])
    dlong1 = dlong2 -1
    if abs(wavey[dlong2] - d2) < abs(wavey[dlong1] - d2):
        dlong_i = dlong2
    else:
        dlong_i = dlong1
    return [[h2oshort_i,h2olong_i],[co2short_i,co2long_i],[dshort_i,dlong_i]]
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
    #saving_segments = []
    ## plotting the endpoints
    if demo:
        ax1.step( waves[ h2o_shor_i[0]:h2o_shor_i[1] ], spect[ h2o_shor_i[0]:h2o_shor_i[1]], color='darkblue') #h2o short 
        ax1.step( waves[ h2o_long_i[0]:h2o_long_i[1] ], spect[ h2o_long_i[0]:h2o_long_i[1]], color='darkblue') #h2o long
        ax1.step( waves[ co2_shor_i[0]:co2_shor_i[1] ], spect[ co2_shor_i[0]:co2_shor_i[1]], color='darkblue') #co2 short
        ax1.step( waves[ co2_long_i[0]:co2_long_i[1] ], spect[ co2_long_i[0]:co2_long_i[1]], color='darkblue') #co2 long
        #saving_segments.append( ( waves[ h2o_shor_i[0]:h2o_shor_i[1] ], spect[ h2o_shor_i[0]:h2o_shor_i[1]] ) )
        #saving_segments.append( ( waves[ h2o_long_i[0]:h2o_long_i[1] ], spect[ h2o_long_i[0]:h2o_long_i[1]] ) )
        #saving_segments.append( ( waves[ co2_shor_i[0]:co2_shor_i[1] ], spect[ co2_shor_i[0]:co2_shor_i[1]] ) )
        #np.savez('/home/antojr/codespace/endpoints.npz', h1wave= waves[h2o_shor_i[0]:h2o_shor_i[1]], h2wave= waves[h2o_long_i[0]:h2o_long_i[1]],\
        #    h1spec= spect[h2o_shor_i[0]:h2o_shor_i[1]], h2spec= spect[h2o_long_i[0]:h2o_long_i[1]], \
        #    c1wave= waves[co2_shor_i[0]:co2_shor_i[1]], c2wave= waves[co2_long_i[0]:co2_long_i[1]], \
        #    c1spec= spect[co2_shor_i[0]:co2_shor_i[1]], c2spec= spect[ co2_long_i[0]:co2_long_i[1]] )
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
    saving_more = []
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
        saving_more.append(wavo)
        saving_more.append(contin_line)
        ## subtract the fabricated continuum 
        gasline = spec - contin_line #h2o emission, with continuum removed
        if demo:
            ax1.step(wavo,contin_line,color='green')
            ax1.step(wavo,gasline,color='red')
            ax1.vlines((h1,h2,c1,c2),ymin=0,ymax=0.0014,color='k')
        inta, intb = intab
        gas = np.trapz(gasline[inta:intb],x=wavo[inta:intb])
        two.append(gas)
    np.savez('/home/antojr/codespace/continuum.npz', hwaves=saving_more[0], hcon=saving_more[1], cwaves=saving_more[2], ccon=saving_more[3])
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
    return (two[0], two[1], dus)
def make_gasmaps(pathToScanDirectory,sigma_cut = 2.5,saveName='cube_gasmaps_wild.fit',inspec='cube_smooth_v1.fit', inwave='cube_wave_v1.fit'):
    datf = fits.open(pathToScanDirectory + '/' + inspec) #cube with smooth spectra
    wavesf = fits.open(pathToScanDirectory + '/' + inwave)
    dat_h = datf[0].header
    dat = datf[0].data.copy()
    waves = wavesf[0].data.copy()
    datf.close()
    wavesf.close()
    ysize = dat.shape[1] #frames in one (1) scan ~16,32,etc
    xsize = dat.shape[2] #pixels in one (1) frame ~256
    outcube = np.ones((3,ysize,xsize),dtype=float)
    for xx in range(xsize): #for each pixel in the x
        for yy in range(ysize): #take a pixel in the y
            pixelx,pixely = xx, yy #add 1 to get ds9 coordinates
            spect = dat[:,pixely,pixelx]
            wavex = waves[:,pixely,pixelx]
            h2o, co2, dust = measure_gas(spect, wavex)
            outcube[0,yy,xx] = h2o
            outcube[1,yy,xx] = co2
            outcube[2,yy,xx] = dust
            pass
        pass
    fitter = fits.PrimaryHDU(outcube,header=dat_h)
    fitter.writeto(pathToScanDirectory + '/' + saveName)
    return
#what directory to look for cubes?
d1 = 1.80
d2 = 2.20
h1 = 2.59
h2 = 2.77
c1 = 4.17
c2 = 4.31
sigma = 2.5
#directs = np.loadtxt("/home/antojr/stash/datatxt/directories.txt",dtype=object,skiprows=1)
#directs[:,0] = directs[:,0].astype(int)    #converting indeces from str to int
#
if __name__ == "__main__":
    all_some = input("All-> yes, selection -> [index range]: ")
    if all_some == 'y' or all_some == 'Y' or all_some == 'yes' \
    or all_some == 'Yes' or all_some == '1' or all_some == 'True' \
    or all_some == 'true' or all_some == 'all' or all_some == 'All':
        #setting up start and stop to produce all gas maps
        sta,sto = 0,1321
    else:
        #setting up start and stop to match indices given
        ab,bb = all_some.split()
        sta,sto = int(ab), int(bb)+1
    #regardless of setup, w start/stop defined, procedure is same
    prog_counter = 1
    for i in range(sta,sto):
        make_gasmaps( a['directory path'][i] , inspec='cube_smooth_v7.fit', inwave='cube_wave_v7.fit', saveName='cube_gasmaps_v7.fit' )
        if (i-sta)/(sto-sta) >= prog_counter * 0.1 :
            print(f'{(i-sta)/(sto-sta)*100.:.3f}% complete...')
            prog_counter+=1
        pass
    print('Okay done. Bye')
else:
    pass

