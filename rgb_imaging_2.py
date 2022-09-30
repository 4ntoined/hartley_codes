#Antoine
#RGB images of dust, co2 and h2o

import numpy as np
import astropy.io.fits as fits
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cometmeta import a
from datafunctions import selector, selector_prompt

def rgb(pathToScan,scan_i,plot_it = False,save_plot=False, scaling = 'linear', vmin_fact=1e-3, blu = False, grn = False, red = False):
    """
    Inputs:
        pathToScan - path to scan directory
        scan_i - the index i of the scan, 0 for first, 1320 for last in time order
                    this will be used for retrieving more scan info for image
        plot_it - True if you want a matplotlib image, False for no image
        save_plot - True if you want to save the plot (change directory)
        red - True if you wanna print a red with that
        grn - True if you wanna separate that green out
        blu - True best color
    Returns
    -------
    the image in cube form [ysize,xsize,colors]
    plotting optional, saving plot optional
    """
    ### nucleus location ###
    xo, yo = int(a['x-nucleus'][scan_i]), int(a['y-nucleus'][scan_i])
    dat = fits.open(pathToScan + "/cube_gasmaps_final_enhance_v6.fit")
    dat = dat[0].data
    sha = dat.shape
    ### assigning colors ###
    rdd = dat[2,:,:] #will be shape = (ysize,xsize).... dust
    green = dat[1,:,:] # co2
    blue = dat[0,:,:]   #h2o
    ### assembling image, kind of an unnecessary step here
    goku = np.ones((sha[1],sha[2],3))
    goku[:,:,0] = rdd.copy() #needs to be [ysize, xsize]
    goku[:,:,1] = green.copy()
    goku[:,:,2] = blue.copy()
    #### should we make a vmin.vmax cut here?
    vmin = np.min( vmin_fact * np.nanmean( goku[:,170:,1:3], axis=(0,1) ) )
    goku[ goku <= vmin ] = vmin
    if scaling=='linear':
        pass
    elif scaling=='log':
        goku[:,170:,1:3] = np.log10(goku[:,170:,1:3])
    elif scaling=='root': 
        goku[:,170:,1:3] = ( goku[:,170:,1:3] )**0.5
    else:
        print("Uhh")
    #the log10
    #the root sq
    #to flip the color gradient, will be rgb though
    #goku[:,170:,0] *= -1

    ## normalize h2o and co2 together ###
    goku[:,170:,1:3] = normalize(goku[:,170:,1:3])
    ### scale dust to be on par with gases ###
    dscl = np.nanmean( goku[sha[1]//2, 55:65, 1] ) / np.nanmean( goku[sha[1]//2, 55:65, 0] )
    goku[:,:,0] *= abs(dscl)
    ### scaling modes, linear, power, exponent, log10
    
    ### marking nucleus location ###
    goku[yo,xo,:] = 0.0
    ### cropping antisaturation filter###
    goku = goku[:,170:,:]
    sha = goku.shape
    #goku *= -1
    #print(sha)
    ### plott ###
    ##############
    ######figure settings#####
    ### figure size###
    figdpi = 120
    ####checking if we're plotting colors separate
    clrs = np.array([red,grn,blu],dtype=int)
    #print(clrs)
    for colr in list(enumerate(clrs)): #index[0] records color index[1] whether we want it or not
        if colr[1]:
            #make a figure for that color
            fig,axc = plt.subplots()
            fig.dpi = figdpi
            colortags = ('red','grn','blu')
            cmapss = ('Reds','Greens','Blues')
            axc.imshow(goku[:,:,colr[0]], cmap= cmapss[colr[0]], origin = 'lower')
            if xo == 0.0 or yo ==0.0:
                axc.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]} | no nucleus")
            else:
                axc.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]}")
            if save_plot:
                plt.savefig(f"/chiron4/antojr/rgbs/rgb_v3_{scan_i:0>4}_{colortags[colr[0]]}.png")
            if plot_it:
                plt.show()
            plt.close(fig)
        #if none of these are true...
        pass
    #plor the big one
    fig,ax1 = plt.subplots()
    fig.dpi=figdpi       
    ax1.imshow(goku,origin='lower')
    if xo == 0.0 or yo ==0.0:
        ax1.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]} | no nucleus")
    else:
        ax1.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]}")
    if save_plot:
        plt.savefig(f"/chiron4/antojr/rgbs/rgb_v3_{scan_i:0>4}_rgb.png")
    if plot_it:
        plt.show()
    plt.close(fig)
    return goku

def centering(pathToScan, scan_i, usemap='cube_gasmap_final_enhance_v7.fit', plot_it = False, save_plot=False, save_here='/home/antojr/hartley2/results/', red = False, grn = False, blu = False, figdpi = 120, scaling='linear', vmin_fact=1e-3):
    """
    Inputs: see above
    Returns
    -------
    the image centered [ysize,xsize,colors] in a much larger frame
    """
    xo, yo, ysize = int(a['x-nucleus'][scan_i])-170, int(a['y-nucleus'][scan_i]), a['number frames'][scan_i]
    imag = rgb(pathToScan, scan_i, plot_it = False, save_plot=False, scaling=scaling, vmin_fact=vmin_fact)
    #bigg = np.zeros((131,181,3),dtype=float)
    bigg = np.zeros((93,135,3),dtype=float)
    #print(imag.shape)
    if imag.shape[0] != ysize:
        print(f"got a mismatched size for {scan_i}")
        pass
    elif xo > 0.0:    #only do the centering if there is nuke info
        #print(42-xo, 42+86-xo)
        #print(bigg.shape)
        #print(bigg[43-yo:43+ysize-yo,67-xo:67+86-xo,:].shape)
        #print(xo)
        bigg[46-yo:46+ysize-yo,67-xo:67+86-xo,:] = imag
    else:
        bigg[:ysize,:86,:] = imag
    ### plott ###
    ## plotting the colors ##
    clrs = np.array([red,grn,blu],dtype=int)
    colortags = ('red','grn','blu')
    cmapss = ('Reds','Greens','Blues')
    for colr in list(enumerate(clrs)): #index[0] records color index[1] whether we want it or not
        if colr[1]:
            #make a figure for that color
            fig,axc = plt.subplots()
            fig.dpi = figdpi
            plo = axc.imshow(bigg[:,:,colr[0]], cmap= cmapss[colr[0]], origin = 'lower')
            #divider = make_axes_locatable(axc)
            #caxx = divider.append_axes("right",size="5%",pad=0.1)
            #plt.colorbar(plo,cax=caxx)
            if xo <= 0.0 or yo ==0.0:
                axc.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]} | no nucleus")
            else:
                axc.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]}")
            if save_plot:
                figdat = {'Author':'Antoine Darius','Software':'rgb_imaging_v2.py'}
                plt.savefig(save_here+ f"rgbc_v4_{colortags[colr[0]]}_nobar_{scan_i:0>4}.png",metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
            if plot_it:
                plt.show(block=False)
            #plt.close(fig)
            pass
        #if none of these are true...
        pass
    ## plotting the whole shebang ##
    fig,ax2 = plt.subplots()
    fig.dpi = 120
    ax2.imshow(bigg,origin='lower')
    if xo <= 0.0 or yo == 0.0:
        ax2.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]} | no nucleus")
    else:
        ax2.set_title(f"{a['julian date'][scan_i]:.3f} | {a['DOY'][scan_i]}.{a['exposure id'][scan_i]}")
    plt.tight_layout
    if save_plot:
        figdat = {'Author':'Antoine Darius','Software':'rgb_imaging_v2.py'}
        plt.savefig(save_here+ f"rgbc_v4_rgb_nobar_{scan_i:0>4}.png",metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
    if plot_it:
        plt.show(block=False)
    #input('Ready?')
    #plt.close(fig)
    return bigg

def normalize(data):
    return (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))

if __name__ == '__main__':
    #what to do
    option_1 = input('What to do? 1-> plot range, 2-> reframe experiment\n: ')
    if option_1 == '1':
        #do the basic stuff from before
        directs = a['directory path']               #np.loadtxt("/home/antojr/stash/datatxt/directories.txt",dtype=object,skiprows=1)
        #directs[:,0] = directs[:,0].astype(int)    #converting indeces from str to int
        rangor = input('index range: ')
        scalor = input('scale: ')
        minimu = input('min value cutoff: ') or '1e-3'
        versio = input('map version 6/7: ') or '7'
        try:
            mini = float(minimu)
            sta, sto = rangor.split()
            if versio == '6' or versio == '7':
                pass
            else:
                raise ValueError
        except ValueError:
            print("NO!")
        except:
            print('Yeah you super broke it.')
        pass
        if versio == '6':
            maptouse = '/cube_gasmaps_final_enhance_v6.fit'
        elif versio == '7':
            maptouse = '/cube_gasmaps_final_enhance_v7.fit'
        else:
            print('NO!')
            quit()
        for i in range(int(sta),int(sto),1):
            #centering(directs[i],i,plot_it=True, grn = True, blu = True, red= True, save_plot=False, scaling=scalor,vmin_fact=mini)
            centering( directs[i], i, usemap=maptouse, plot_it=True, grn=True, blu=True, red=False, save_plot=False, scaling=scalor, vmin_fact=mini )
        pass
        input('Done.')
        print('Quitting...')
        #quit()
    elif option_1 == '2':
        #uhhh

        pass
    elif option_1 == '3':   
        #batch create and save the rgb images
        print("saving a bunch of pictures")
        directs = a['directory path'].copy()
        for i in range(200,301):
            print(i)
            #if i%100 == 0:
            #    centering(directs[i],i,save_plot=True,plot_it=True)
            #else:
            centering(directs[i],i,usemap='/cube_gasmaps_final_enhance_v7.fit', save_plot=True,red=True,grn=True,blu=True, save_here = '/chiron4/antojr/rgb_centered/v4_nobars/', figdpi=140, scaling='root',vmin_fact=0.0)
            pass
        print('Complete. Quitting...')
        #quit()
    else:
        #nothing here
        pass
else:
    #module things?
    pass


#no longer necessary directs = directs[1:]                       #getting rid of first entry, parent directory
#do = rgb(directs[227,1],directs[227,0],plot_it=True,save_plot=False)
#rgb("/chiron4/antojr/calibrated_ir/306.4000031",202,plot_it=True)
""" #testing centering method
pair = []
nuke = []
ysize = []
for i in range(277,279):
    pair.append(rgb(directs[i,1],directs[i,0]))
    nuke.append( (int(a['x-nucleus'][i])-170, int(a['y-nucleus'][i])) )
    ysize.append( a['number frames'][i] )
#print(ysize[1])

bigs = np.zeros((131,181,3,2),dtype=float)
bigs[65-nuke[0][1]:65+ysize[0]-nuke[0][1],90-nuke[0][0]:176-nuke[0][0],:,0] = pair[0].copy()
bigs[65-nuke[1][1]:65+ysize[1]-nuke[1][1],90-nuke[1][0]:176-nuke[1][0],:,1] = pair[1].copy()
"""
#bigs = centering(directs[210,1],directs[210,0],plot_it=True)

#fig,ax = plt.subplots()
#fig.dpi=120
#ax.imshow(bigs,origin='lower')
#plt.show()
### for batch saving with ocassional(sp?) plotting
"""
for i in range(0,1321):
    print(i)
    if i%100 == 0:
        centering(directs[i,1],directs[i,0],save_plot=True,plot_it=True,red=True,grn=True,blu=True)
    else:
        centering(directs[i,1],directs[i,0],save_plot=True,red=True,grn=True,blu=True)
    pass

"""
# for batch plotting
#"""
#"""
#scaling dust down so the level of h2o far from comet
#dustscaled = dust *scl
#scl = dustscaled/dust
#just checking


#uhhh in my experience [wavelength 512 / gas species 3, ysize #frames in scan, xsize 256]

#fig,(ax1,ax2,ax3,ax4) = plt.subplots(4,1,sharex=True,sharey=True)
#ax2.imshow(goku[:,:,0],cmap="Reds",origin='upper')
#ax3.imshow(goku[:,:,1],cmap="Greens",origin='upper')
#ax4.imshow(goku[:,:,2],cmap="Blues",origin='upper')


