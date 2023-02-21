#Antoine
#light curves for the volatiles
#Antoine much later
#cranking this up

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
        for ix in (h_clip, c_clip, d_clip):
            ia = ix.copy() #the copy of the aperture that will 0 the middle and apply a correction to the borders
            #making the non-border parts 0
            ia[1:-1,1:-1]=0
            #correction the border
            ia*=overspill
            #borders are determined
            #onto getting the aperture w/o border
            ix[0,:]=0
            ix[-1,:]=0
            ix[:,-1]=0
            ix[:,0]=0
            #borders in ix are zeroed out, borders in ia are corrected, we add
            res = ia + ix
            ress.append(res)
        ### use RESISTANT MEAN ###
        #x_sum = ( ress )
        means = []
        sigs = []
        nrej = []
        apsize = s
        for i in range(3): 
            onemean, onesigma, numrej = resistant_mean( ress[i], sigma_cutoff )
            means.append(onemean)
            sigs.append(onesigma)
            nrej.append(numrej)
        #hmean, cmean, dmean = means
        hsig, csig, dsig = sigs
        hrej, crej, drej = nrej
        # turn means into sums by using aperture size and number of rejected pixels
        sums = []
        for i in range(3): sums.append( means[i] * apsize**2  )
        hsum, csum, dsum = sums
        hpack = (hsum, hsig, hrej)
        cpack = (csum, csig, crej)
        dpack = (dsum, dsig, drej)
        #
        #h_sum = np.nansum(ress[0])
        #c_sum = np.nansum(ress[1])
        #d_sum = np.nansum(ress[2])
    else:
        hpack = (0.0, 0.0, 0)
        cpack = (0.0, 0.0, 0)
        dpack = (0.0, 0.0, 0)
    return hpack, cpack, dpack, clipd
def sortDires(row):     #key for sorting directories by time data were taken
    cal = fits.open(row+"/dal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym
#
a = np.load('a_cometmeta.npy')
#cata = []
#dire = []
#for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
#    dire.append(paths)
#    cata.append(fils)
#dire = dire[1:] #getting rid of the first entry, the root directory
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
    curve_filename = 'gascurves_x6.txt'
    curve_filepath = '/home/antojr/stash/datatxt/'
    header_note = '424800m aperture, no corrections, interpolated aperture,'+\
        'uses v8 gasmaps, made by crank_lightcurves, resisting_mean, more data'
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
                f"{h2o[1]} {co2[1]} {dus[1]} {int(h2o[2])} {int(co2[2])} {int(dus[2])} {int(clip_flag)}\n")
            if (i-sta)/(sto-sta) >= prog_counter * 0.1 :
                print(f'{(i-sta)/(sto-sta)*100.:.3f}% complete...')
                prog_counter+=1
            pass
        print('.txt file produced.')
    gastype = np.dtype([ ('h2o','f8'),('co2','f8'),('dust','f8'), \
            ('h error','f8'),('c error','f8'),('d error','f8'), ('num hrej','i4'),('num crej','i4'),\
            ('num drej','i4'), ('clip flag','i4') ])
    gascurves = np.array(masterMap,dtype=gastype)
    np.save('results_code/gascurves_x6.npy', gascurves)
    print('.npy array saved.')
else:
    pass
