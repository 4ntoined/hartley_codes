#Antoine
#RGB images of dust, co2 and h2o

import numpy as np
import astropy.io.fits as fits
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mpl_toolkits.axes_grid1 import make_axes_locatable
#from cometmeta import a
#from datafunctions import selector, selector_prompt

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
    vmin = np.min( vmin_fact * np.nanmax( goku[:,170:,1:3], axis=(0,1) ) )
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
    else:
        plt.close()
    #input('Ready?')
    #plt.close(fig)
    return bigg

def normalize(data):
    return (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))

a = np.load('a_cometmeta.npy')

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
        #co2 experiments
        rng = np.random.default_rng()
        scanz = np.linspace(100,800,21).astype(int)
        all_em = list(range(1321))
        scan1 = 250
        save_here = '/chiron4/antojr/co2_movie/'
        #co2pic = picture[:,:,1]
        for i in scanz:
            picture = centering( a['directory path'][i], i, usemap='/cube_gasmaps_final_enhance_v7.fit', plot_it=False, save_plot=False, scaling='root', vmin_fact=0.07)
            fig,ax = plt.subplots()
            fig.dpi=140
            ax.imshow(picture[:,:,1],origin='lower',cmap='inferno')
            if a['x-nucleus'][i] == 0.0 or a['y-nucleus'][i] == 0.0:
                ax.set_title(f"{a['julian date'][i]:.3f} | {a['DOY'][i]}.{a['exposure id'][i]} | no nucleus")
            else:
                ax.set_title(f"{a['julian date'][i]:.3f} | {a['DOY'][i]}.{a['exposure id'][i]}")
            figdat = {'Author':'Antoine Darius','Software':'gasimaging.py'}
            #plt.savefig(save_here+ f"co2movie_v1_nobar_{i:0>4}.png",metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
            plt.show(block=True)
            plt.close()
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
            centering(directs[i],i,usemap='/cube_gasmaps_final_enhance_v7.fit', save_plot=True,red=True,grn=True,blu=True, save_here = '/chiron4/antojr/rgb_centered/v4_nobars/', figdpi=140, scaling='root',vmin_fact=0.07)
            pass
        print('Complete. Quitting...')
        #quit()
    elif option_1 == '4':
        #create and save a select few images
        peaks_i = np.load('results_code/peak_indeces.npy').astype(int)
        #peaks_i[ h2o/co2, peak/trough, 6 cycles, 3 peaks per cycle ]
        save_locs = ['pngs_peaks1/','pngs_peaks2/','pngs_peaks3/','pngs_trous1/','pngs_trous2/','pngs_trous3/']
        gas_name =  ['h2o','co2' ]
        cycle_name = [ 'A','B','C','D','E','F'] 
        #peaks
        for j in (0,1,2): #running over 3 peaks in the cycles
            for i in range(2): #running over h2o and co2
                for h in range(6): #running though 6 cycles
                    topic = peaks_i.copy()[i,0,h,j]
                    if topic == -9999:
                        #do nothing
                        print('miss')
                        pass
                    else:
                        picture = centering(a['directory path'].copy()[topic], topic, usemap='/cube_gasmaps_final_enhance_v7.fit', plot_it=False, save_plot=False, figdpi=140, scaling='root',vmin_fact=0.07)
                        fig,ax = plt.subplots()
                        fig.dpi=140
                        if i==0: ii = 2
                        elif i==1: ii = 1
                        ax.imshow(picture[:,:,ii],origin='lower',cmap='inferno')
                        if a['x-nucleus'][topic] == 0.0 or a['y-nucleus'][topic] == 0.0:
                            ax.set_title(f"{a['julian date'][topic]:.3f} | {a['DOY'][topic]}.{a['exposure id'][topic]} | no nucleus")
                        else:
                            ax.set_title(f"{a['julian date'][topic]:.3f} | {a['DOY'][topic]}.{a['exposure id'][topic]}")
                        figdat = {'Author':'Antoine Darius','Software':'gasimaging.py'}
                        plt.savefig("results_code/" + save_locs[j]+ gas_name[i] + "_" + cycle_name[h] + ".png",metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
                        #plt.show(block=True)
                        plt.close()
                    pass
                pass
            pass
        for j in (3,4,5): #running over 3 troughs
            for i in range(0,1): #h2o/co2
                for h in range(6):
                    topic = peaks_i.copy()[i,1,h,j-3]
                    if topic == -9999:
                        #do nothing
                        print('miss')
                        pass
                    else:
                        picture = centering(a['directory path'].copy()[topic], topic, usemap='/cube_gasmaps_final_enhance_v7.fit', plot_it=False, save_plot=False, figdpi=140, scaling='root',vmin_fact=0.07)
                        fig,ax = plt.subplots()
                        fig.dpi=140
                        if i==0: ii = 2
                        elif i==1: ii = 1
                        ax.imshow(picture[:,:,ii],origin='lower',cmap='inferno')
                        if a['x-nucleus'][topic] == 0.0 or a['y-nucleus'][topic] == 0.0:
                            ax.set_title(f"{a['julian date'][topic]:.3f} | {a['DOY'][topic]}.{a['exposure id'][topic]} | no nucleus")
                        else:
                            ax.set_title(f"{a['julian date'][topic]:.3f} | {a['DOY'][topic]}.{a['exposure id'][topic]}")
                        figdat = {'Author':'Antoine Darius','Software':'gasimaging.py'}
                        plt.savefig("results_code/" + save_locs[j] + gas_name[i] + "_" + cycle_name[h] + ".png",metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
                        #plt.show(block=True)
                        plt.close()
                    pass
                pass
            pass
        pass
    else:
        #nothing here
        pass
else:
    #module things?
    pass

