#Antoine
#this will demo the continuum removal given a scan and a partcular pixel to plot
#
#########################################################################################################################################
import os
import numpy as np
import astropy.io.fits as fits
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector,selector_prompt
from resistant_mean_nan import resistant_mean
from crank_gasmaps import findEmissions, measure_gas

def unloadCube(scan_index, cubename='', wavename = ''):
    """
    will take in an index and cube_name spit out the datacube and wavecube
    """
    global a
    direc = a['directory path'][scan_index]
    c1 = fits.open(direc + cubename) #cube with smooth spectra
    cw = fits.open(direc + wavename)
    hdr = c1[0].header
    dat = c1[0].data
    wav = cw[0].data
    c1.close()
    cw.close()
    #ysize = da1.shape[1] #frames in one (1) scan ~16,32,etc
    #xsize = da1.shape[2] #spatial pixels in one (1) frame ~256
    return (dat, wav, hdr)

def selectOne():
    ### choosing a scan, by: index [0-1320]?, exposureid+DOY? [xxx yyyyyyy/y], julian date[2455494-2455517], directory
    #direc= input("directory with the smooth cube?: ") or '/chiron4/antojr/calibrated_ir/312.4300015'
    scani = selector_prompt()
    direc = a['directory path'][scani]
    c1 = fits.open(direc + spec_name_1) #cube with smooth spectra
    cw = fits.open(direc + wave_name)
    da1 = c1[0].data
    wav = cw[0].data
    #h1 = 2.59
    #h2 = 2.77
    #c1 = 4.17
    #c2 = 4.31
    ysize = da1.shape[1] #frames in one (1) scan ~16,32,etc
    xsize = da1.shape[2] #spatial pixels in one (1) frame ~256
    nx,ny = int(a['x-nucleus'][scani]), int(a['y-nucleus'][scani])
    pixo  = input(f'Which pixel? Nucleus-> {nx} {ny}\nx|0-255 y|0-{ysize-1}: ') or (nx, ny)
    
    #umm lets plot a spectrum from 307.4000013
    #has 38 frames, nucleus location: 199.651 11.728
    #pixx, pixy = 40+170,19
    if type(pixo) == str:
        pxx, pyy = pixo.split()
        pixx, pixy = (int(pxx), int(pyy))
    else:
        pixx, pixy = int(pixo[0]),int(pixo[1])
    spec = da1[:,pixy,pixx]
    wave = wav[:,pixy,pixx]
    go = measure_gas( spec, wave, demo=True )
    return

def plotSeries(series, savfig=False):
    """
    this will take in a list (iterable) of identifying tokens for scans+pixels
    and return a plot for each one of the entries noted by the iterable
    Input: series: list of tuples [(scan index, pixelx, pixely),...]
    Output: will plot each entry, option to save I guess Idk
    """
    global spec_name_1, wave_name
    for i in range(len(series)):
        scani, pixx, pixy = series[i]
        direc = a['directory path'][scani]
        c1 = fits.open(direc + spec_name_1) #cube with smooth spectra
        cw = fits.open(direc + wave_name)
        da1 = c1[0].data
        wav = cw[0].data
        c1.close()
        cw.close()
        spec = da1[:,pixy,pixx]
        wave = wav[:,pixy,pixx]
        go = measure_gas( spec, wave, demo=True, savfig=savfig )
        #okat so someone has to work out that promised saving feature
    input("Ready to go?")
    return

spec_name_1 = '/cube_smooth_final_v5.fit'
wave_name   = '/cube_wave_final_v1.fit'

if __name__ == '__main__':
    option_a = input('Which door? 1->basic, 2-> experiment:\n')
    if option_a == '2':
        #then do the thing for Lori
        #scan i = 683, pixelx is 198, 199, 200 and pixely 12, 11, 13
        #sero = [ (683, a['x-nucleus'][i], a['y-nucleus'][i]   )    for i in  ]
        sero = [
           (683, 198, 11), (683, 199, 11), (683,200, 11),
           (683, 198, 12), (683, 199, 12), (683,200,12),
           (683, 198, 13), (683, 199, 13), (683, 200, 13)
        ]
        plotSeries(sero)
    elif option_a == '1':
        #then do the basic thing with the selector prompt
        selectOne()
    elif option_a == '3':
        print("only functionality is this message so cool")
    else:
        print('nope')


