#Antoine
#this is gonna plot my latest spectra w my best tools

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector, selector_prompt
from continuum_removal_demo import selectOne

def selectSpec(scani, specname='name',wavename='name'):
    ### choosing a scan, by: index [0-1320]?, exposureid+DOY? [xxx yyyyyyy/y], julian date[2455494-2455517], directory
    #direc= input("directory with the smooth cube?: ") or '/chiron4/antojr/calibrated_ir/312.4300015'
    direc = a['directory path'][scani]
    c1 = fits.open(direc + specname) #cube with smooth spectra
    cw = fits.open(direc + wavename)
    da1 = c1[0].data
    wav = cw[0].data
    ysize = da1.shape[1] #frames in one (1) scan ~16,32,etc
    xsize = da1.shape[2] #spatial pixels in one (1) frame ~256
    nx,ny = int(a['x-nucleus'][scani]), int(a['y-nucleus'][scani])
    pixo  = input(f'Which pixel? Nucleus-> {nx} {ny}\nx|0-255 y|0-{ysize-1}: ') or (nx, ny)
    if type(pixo) == str:
        pxx, pyy = pixo.split()
        pixx, pixy = (int(pxx), int(pyy))
    else:
        pixx, pixy = int(pixo[0]),int(pixo[1])
    spec = da1[:,pixy,pixx]
    wave = wav[:,pixy,pixx]
    #go = measure_gas( spec, wave, spectrum_scani=scani, demo=True, xy=(pixx,pixy))
    #input('Ready?')
    return (spec, wave, pixx, pixy)



if __name__ == '__main__':
    h1, h2 = (2.59,2.77)
    c1, c2 = (4.17,4.31)
    opt1 = input('What mode? ')
    if opt1 == '1':
        scani = selector_prompt()
        spect, waves, nx, ny = selectSpec(scani, specname='/cube_smooth_final_v7.fit', wavename='/cube_wave_final_v7.fit')

        ##unloading continuum removal specs
        endss = np.load('endpoints.npz')
        conts = np.load('continuum.npz')


        #plot#
        fig, ax = plt.subplots()
        fig.dpi=140
        fig.figsize= (8,5)
        #
        ax.step(waves,spect,color='firebrick',linewidth=1.3,zorder=5)
        #
        endpoint_color = 'gold'
        ax.step(endss['h1wave'], endss['h1spec'], color=endpoint_color, linewidth=1.3, zorder=7) #h2o short 
        ax.step(endss['h2wave'], endss['h2spec'], color=endpoint_color, linewidth=1.3, zorder=8) #h2o short 
        ax.step(endss['c1wave'], endss['c1spec'], color=endpoint_color, linewidth=1.3, zorder=9) #h2o short 
        ax.step(endss['c2wave'], endss['c2spec'], color=endpoint_color, linewidth=1.3, zorder=10) #h2o short 
        #
        contin_color = 'lightslategray'
        ax.step(conts['hwaves'], conts['hcon'], color=contin_color, linewidth=1.5, zorder=4 )
        ax.step(conts['cwaves'], conts['ccon'], color=contin_color, linewidth=1.5, zorder=3 )
        #
        ax.hlines((0), xmin=2.1, xmax=4.99, color='k', linewidth=0.7, zorder=1)
        ax.vlines((h1,h2,c1,c2),ymin=0.,ymax=1.0, color='k',linewidth=0.7, linestyles='dashed', zorder=2)
        #
        ax.set_xlim((2.3,4.5))
        concern = np.nanmin( np.argwhere(waves > 2.2) )
        max_spec = np.nanmax( spect[concern:] )
        ax.set_ylim((max_spec/-8.,max_spec*1.1))
        ax.set_xlabel('Wavelength [$\mu m$]')
        ax.set_ylabel(' Radiance [$W/m^2/sr/\mu m$]')
        ax.set_title(f"{a['julian date'][scani]:.3f} | {a['DOY'][scani]}.{a['exposure id'][scani]} | {nx, ny}")
        #saving the plot real quick
        figdat = {'Author':'Antoine Darius','Software':'specplot.py'}
        plotname='spec_2demo.png'
        plotpath='/home/antojr/dps_bucket/spectra/'
        #plt.savefig(plotpath + plotname, dpi=fig.dpi, metadata = figdat, bbox_inches='tight')
        plt.show(block=True)

    elif opt1 == '2':
        pass
    else:
        pass
    pass
else:
    pass
#hey

