#Antoine
#light curves for the volatiles
#Antoine much later
#cranking this up
#wish i had commented the original like at all
#i was probably definitely rushing like right now
import os
import numpy as np
import astropy.io.fits as fits
from playingwithdata import a
#
def getGases(gasmapARRAY, xnuke, ynuke, apertureradius, s):
    h2o = gasmapARRAY[0,:,:]
    co2 = gasmapARRAY[1,:,:]
    dus = gasmapARRAY[2,:,:]
    #excise a certain part
    #diff procedures depending on even or odd aperture radius
    if s%2 == 0:   #even
        h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
        c_clip = co2[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
        d_clip = dus[ynuke-apertureradius:ynuke+apertureradius,xnuke-apertureradius:xnuke+apertureradius]
    else:                       #odd
        h_clip = h2o[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
        c_clip = co2[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
        d_clip = dus[ynuke-apertureradius:ynuke+apertureradius+1,xnuke-apertureradius:xnuke+apertureradius+1]
    h_sum = np.nansum(h_clip) #/ s**2
    c_sum = np.nansum(c_clip) #/ s**2
    d_sum = np.nansum(d_clip) #/ s**2
    return h_sum, c_sum, d_sum
def sortDires(row):     #key for sorting directories by time data were taken
    cal = fits.open(row+"/cal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym
#
cata = []
dire = []
for paths, dirs, fils in os.walk("/chiron4/antojr/calibrated_ir/"):
    dire.append(paths)
    cata.append(fils)
dire = dire[1:] #getting rid of the first entry, the root directory
xlocs, ylocs = a['x-nucleus'].astype(int) , a['y-nucleus'].astype(int)
#need to reoganize dire so that these directories are actually in julian date order
dire.sort(key=sortDires)
a_radius=3
a_diamet=7
masterMap = []
for i in range(len(dire)):
    mapp = fits.open(dire[i]+"/cube_gasmaps_final_v1.fit")    #gen 1 maps
    mapp = mapp[0].data
    h2o , co2, dus = getGases(mapp, xlocs[i], ylocs[i], a_radius, a_diamet) #a['aperture radius'][i] #a['aperture size'][i]
    masterMap.append((h2o,co2,dus))
gascurves = np.array(masterMap,dtype=float)
outt = open("gas_light_curve_v6.txt","w")
outt.write("jd, h2o, co2, dust // 7x7-pixel aper\n")
for i in range(len(gascurves)):
    outt.write(f"{a['julian date'][i]} {gascurves[i,0]} {gascurves[i,1]} {gascurves[i,2]}\n")
outt.close()
