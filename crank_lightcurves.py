#Antoine
#light curves for the volatiles
#cranking this up
#so up until this point we have been evaluating the gases in the aperture using
#a straight (nan)sum, i think at some point we used the (nan)mean
#now we are using the resistant mean
#the first iteration of this did the res-mean on the whole aperture
#the next will use the res-mean on the two parts of the aperture, core +
#border separately and add the results

import os
import numpy as np
import astropy.io.fits as fits
from resistant_mean_nan import resistant_mean
#from cometmeta import a
#
def getGases(gasmapARRAY, xnuke, ynuke, apertureradius, s, overspill, sigma_cutoff=2.5):
    h2o = gasmapARRAY[0,:,:].copy()
    co2 = gasmapARRAY[1,:,:].copy()
    dus = gasmapARRAY[2,:,:].copy()
    ysize, xsize = h2o.shape
    ### chekcing if the nuc. loc. and aperture radius combo takes a shot that goes off image
    inx1 = (xnuke-apertureradius > 0) and (xnuke+apertureradius < 80)
    inx2 = (xnuke-apertureradius > 170) and (xnuke+apertureradius < xsize+1)
    xoff = not ( inx1 or inx2)
    y0off = ynuke - apertureradius < 0
    yfoff = ynuke + apertureradius > ysize + 1
    clipd = xoff or y0off or yfoff
    #excise a certain part
    #diff procedures depending on even or odd aperture radius
    #if s%2 == 0:   #even
    #if 1 == 2: #too lazy to restructure this thing now that im mixing things up, actually...
    #    print("don't use an even aperture..")
    #    h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
    #    c_clip = co2[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
    #    d_clip = dus[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
    if not clipd: #only continue if data is not clipped
        h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius+1,\
            xnuke-apertureradius:xnuke+apertureradius+1] #apertures with integer radius just greater than necessary
        c_clip = co2[ynuke-apertureradius:ynuke+apertureradius+1,\
            xnuke-apertureradius:xnuke+apertureradius+1]
        d_clip = dus[ynuke-apertureradius:ynuke+apertureradius+1,\
            xnuke-apertureradius:xnuke+apertureradius+1]
        #isolate the borders of the (too big) aperture
        #border_aps = []
        ress = []
        means = []
        sigs = []
        nrej = []
        apsize = int(apertureradius*2+1)
        n_core = (apsize - 2) ** 2
        n_bord = 4*apsize - 4
        clips = (h_clip, c_clip, d_clip)
        for i in range(3):
            ix = clips[i].copy()
            ia = clips[i].copy() #the copy of the aperture that will 0 the middle and apply a correction to the borders
            bordermask = np.ones_like( ia ).astype(bool) #True on borders, false on core
            bordermask[1:-1,1:-1] = False
            #making the non-border parts 0
            ia[np.logical_not( bordermask )] = 0.
            #correction the border
            #borders are determined
            #onto getting the aperture w/o border
            #ix[0,:]=0.
            #ix[-1,:]=0.
            #ix[:,-1]=0.
            #ix[:,0]=0.
            ix[bordermask] = 0.
            #borders in ix are zeroed out, borders in ia are corrected, we add
            #mask for ia to avoid using zeros in the mean
            coremean, coresigma, corerej = resistant_mean( ix[np.logical_not( bordermask )], sigma_cutoff )
            bordmean, bordsigma, bordrej = resistant_mean( ia[ bordermask ], sigma_cutoff )
            #bordmean *= overspill
            #bordsigma *= overspill
            coresum = coremean * n_core
            bordsum = bordmean * n_bord
            bordsum *= overspill
            coresigma *= n_core
            bordsigma *= (n_bord * overspill)
            # total mean
            tot_sum = coresum + bordsum
            # total standard deviation
            tot_sig = np.sqrt(  coresigma**2. + bordsigma**2.  )
            # number of rejected pixels, stored as a complex number
            rejects = complex(corerej, bordrej)
            #
            means.append(tot_sum)
            sigs.append(tot_sig)
            nrej.append(rejects)
        #hmean, cmean, dmean = means
        hrej, crej, drej = nrej
        # turn means into sums by using aperture size and number of rejected pixels
        #sums = []
        #nsig = []
        #for i in range(3):
        #    sums.append( means[i] * apsize**2.  )
        #    nsig.append( sigs[i] * apsize**2.  )
        hsum, csum, dsum = means
        hsig, csig, dsig = sigs
        #
        hpack = (hsum, hsig, hrej)
        cpack = (csum, csig, crej)
        dpack = (dsum, dsig, drej)
        #
        #h_sum = np.nansum(ress[0])
        #c_sum = np.nansum(ress[1])
        #d_sum = np.nansum(ress[2])
    else:
        hpack = (0.0, 0.0, complex(0, 0))
        cpack = (0.0, 0.0, complex(0, 0))
        dpack = (0.0, 0.0, complex(0, 0))
    return hpack, cpack, dpack, clipd
def sortDires(row):     #key for sorting directories by time data were taken
    cal = fits.open(row+"/dal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym
#
a = np.load('a_cometmeta.npy')
if __name__ == '__main__':
    xlocs, ylocs = a['x-nucleus'].astype(int) , a['y-nucleus'].astype(int)
    dire = a['directory path'].copy()
    #aperture size pre-information saved
    a_size = np.load('apsizes_424km_floats.npy')
    a_radi = (a_size - 1.) / 2.
    a_radi_ceils = np.ceil(a_radi).astype(int)
    a_radi_floor = np.floor(a_radi).astype(int)
    errs2 = a_radi - a_radi_floor
    #empty list to fill with lightcurve data
    masterMap = []
    curve_filename = 'gascurves_x7.txt'
    curve_filepath = '/home/antojr/stash/datatxt/'
    header_note = '424800m aperture, no corrections, interpolated aperture,'+\
        'uses v8 gasmaps, made by crank_lightcurves, resisting_mean, more data'+\
        'now doing 2 res means, one for core and one for interpolated border, will add results etc'+\
        '# rejected pixels now stored as core, border rejects, turning means into sums separate now'
    #sta, sto = (250, 270)
    sta, sto = (0, 1321)
    prog_counter=1
    with open(curve_filepath + curve_filename,"w") as fil:
        fil.write("jd, h2o, co2, dust, h-error, c-error, d-error, h-rej, c-rej, d-rej, clipped flag // " + header_note + "\n")
        for i in range(sta,sto):
            #open the gas maps
            mapp = fits.open(dire[i]+"/cube_gasmaps_final_enhance_v8.fit")    #gen 3 maps
            mapp = mapp[0].data
            #measure the gases and whatever
            h2o, co2, dus, clip_flag = getGases(mapp, xlocs[i], ylocs[i], a_radi_ceils[i], a_size[i], errs2[i])
            #getting it all together for the data array
            masterMap.append(( h2o[0],co2[0],dus[0],h2o[1],co2[1],dus[1],h2o[2],co2[2],dus[2],int(clip_flag) ))
            fil.write(f"{a['julian date'][i]} {h2o[0]} {co2[0]} {dus[0]} " +\
                f"{h2o[1]} {co2[1]} {dus[1]} {int( h2o[2].real )} {int( h2o[2].imag )} " + \
                f"{int( co2[2].real )} {int( co2[2].imag )} {int( dus[2].real )} " + \
                f"{int( dus[2].imag )} {int( clip_flag )}\n")
            if (i-sta)/(sto-sta) >= prog_counter * 0.1 :
                print(f'{(i-sta)/(sto-sta)*100.:.3f}% complete...')
                prog_counter+=1
            pass
        print('.txt file produced.')
    gastype = np.dtype([ ('h2o','f8'),('co2','f8'),('dust','f8'), \
            ('h error','f8'),('c error','f8'),('d error','f8'), ('num hrej','c8'),('num crej','c8'),\
            ('num drej','c8'), ('clip flag','i4') ])
    gascurves = np.array(masterMap,dtype=gastype)
    np.save('results_code/gascurves_x7.npy', gascurves)
    print('.npy array saved.')
else:
    pass
