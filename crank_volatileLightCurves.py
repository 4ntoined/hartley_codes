#Antoine
#light curves for the volatiles
#Antoine much later
#cranking this up

import os
import numpy as np
import astropy.io.fits as fits
from cometmeta import a
#
def getGases(gasmapARRAY, xnuke, ynuke, apertureradius, s):
    h2o = gasmapARRAY[0,:,:]
    co2 = gasmapARRAY[1,:,:]
    dus = gasmapARRAY[2,:,:]
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
    if s%2 == 0:   #even
        print("don't use an even aperture..")
        h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
        c_clip = co2[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
        d_clip = dus[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
    else:                       #odd
        h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
        c_clip = co2[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
        d_clip = dus[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
    h_sum = np.nansum(h_clip)
    c_sum = np.nansum(c_clip)
    d_sum = np.nansum(d_clip)
    return h_sum, c_sum, d_sum, clipd
def sortDires(row):     #key for sorting directories by time data were taken
    cal = fits.open(row+"/dal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym
#
#cata = []
#dire = []
#for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
#    dire.append(paths)
#    cata.append(fils)
#dire = dire[1:] #getting rid of the first entry, the root directory
xlocs, ylocs = a['x-nucleus'].astype(int) , a['y-nucleus'].astype(int)
#need to reoganize dire so that these directories are actually in julian date order
#dire.sort(key=sortDires)
dire = a['directory path'].copy()
#a_diamet=15
#a_radius=(a_diamet-1) // 2
a_size = np.load('apsizes_424800m.npy')
a_radi = (a_size - 1) // 2

masterMap = []
curve_filename = 'gascurves_x3_424km.txt'
curve_filepath = '/home/antojr/stash/datatxt/'
header_note = '424800m aperture, no corrections, made by crank_volatileLightCurves'
with open(curve_filepath + curve_filename,"w") as fil:
    fil.write("jd, h2o, co2, dust, clipped flag // " + header_note + "\n")
    for i in range(len(dire)):
        mapp = fits.open(dire[i]+"/cube_gasmaps_final_enhance_v7.fit")    #gen 3 maps
        mapp = mapp[0].data
        h2o , co2, dus, clip_flag = getGases(mapp, xlocs[i], ylocs[i], a_radi[i], a_size[i])#a_radius, a_diamet) #a['aperture radius'][i] #a['aperture size'][i]
        masterMap.append((h2o,co2,dus,int(clip_flag)))
        fil.write(f"{a['julian date'][i]} {h2o} {co2} {dus} {int(clip_flag)}\n")
        if i%100 == 0:
            print(i)
        pass
    pass
gascurves = np.array(masterMap,dtype=float)

