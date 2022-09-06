#Antoine
#histograms and stats

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as fit
from cometmeta import a
from datafunctions import selector, selector_prompt

def unloadCube(scan_index, cubename='', wavename=''):
    cubo = fit.open( a['directory path'][scan_index] + '/' + cubename )
    dato = cubo[0].data
    dath = cubo[0].header
    cubo.close()
    if wavename: #so that we only unload if a wavename is given
        cubw = fit.open( a['directory path'][scan_index] + '/' + wavename )
        wavo = cubw[0].data
        cubw.close()
        return (dato, wavo, dath)
    else:
        return (dato, dath)
    #waves, ysize, xsize1 = dato.shape
    #imag = gasmaps.copy()
    #imag = gasmaps[:,:,170:]
    #xsize2 = imag.shape[2]

def plotHist(gas,smallmap = False):
    #gas = 0 for h2o, = 1 for co2
    global gasmap, imag
    fig,ax = plt.subplots()
    fig.figsize=(10,5.6)
    fig.dpi=140
    if smallmap:
        mappo = imag
    else:
        mappo = gasmaps
    histog = ax.hist(mappo[gas,:,:].ravel(),bins=350)
    histo = histog[0]
    ax.vlines( (0,mean[gas]), ymin=0.9,ymax=1.1*np.max(histo),color=('k','r'), linewidth=0.7)
    ax.set_yscale('log')
    #ax.set_ylim(,None)
    ax.set_ylabel('Counts')
    ax.set_xlabel('Pixel value')
    if gas == 0:
        ax.set_title(f"{a['julian date'][select]:.3f} | {a['DOY'][select]}.{a['exposure id'][select]} | H2O")
    elif gas ==1:
        ax.set_title(f"{a['julian date'][select]:.3f} | {a['DOY'][select]}.{a['exposure id'][select]} | CO2")
    else:
        ax.set_title("You broke this bro, don't even know if you should be seeing this")
    plt.show()
    return

if __name__ == '__main__':
    mode = input('What mode: ') or '1'
    if mode == '1':
        ## selecting and unloading the cube
        select = selector_prompt(default='307 4000011')
        gasmaps, heady = unloadCube(select, cubename='cube_gasmaps_final_enhance_v6.fit')
        ncolor, ysize, xsize1 = gasmaps.shape
        imag = gasmaps[:,:,170:].copy()
        xsize2 = imag.shape[2]
        
        ##  derive some stats from that mans
        mean = np.nanmean(imag,axis=(1,2))
        medi = np.nanmedian(imag,axis=(1,2))
        stan = np.nanstd(imag,axis=(1,2))
        maxx = np.nanmax(imag,axis=(1,2))
        vari = stan**2
        
        #for i in (0,1,2): #i wanna just make this a big array so I can call it later
        #    print(mean[i],medi[i],stan[i],vari[i],maxx[i])
        plotting = input('Plot? 0 for h2o, 1 for co2, else for no plotting\n:  ')
        if plotting == '0' or plotting == '1':
            plotHist(int(plotting),smallmap=True)
        else:   #do nothing if input is wrong
            print('bad input')
        pass
    elif mode == '20':
        #this'll be a bigger analysis run or whatever
        #i wanna run through all the scans and
        #somehow conglomerate the data for h2o and for co2 and
        #keep track of those measures over time ie progression
        #and I also wanna be able to add up, store, and review the histograms
        #means, maxx, stan, histogram object?
        stat_array = np.zeros((2,3,1321),dtype=float)
        #stat_array = stat_array.astype(object)
        #meanso = np.nanmean()
        for i in range( len( a['julian date'] )):
            gases, headd = unloadCube(i, cubename='cube_gasmaps_final_enhance_v6.fit' )
            gasclip = gases[:,:,170:].copy()
            mean = np.nanmean( gasclip,axis=(1,2)) #will be h2omean, co2mean, and dustmean
            stan = np.nanstd( gasclip, axis=(1,2))
            maxx = np.nanmax( gasclip, axis=(1,2))
            hm,cm = ( mean[0], mean[1])
            hs,cs = ( stan[0], stan[1])
            hx,cx = ( maxx[0], maxx[1])
            ## thats 6 i need to fill 8, 2 histograms
            #bluehist = plt.hist( gasclip[0,:,:].ravel(), bins=350)
            #greehist = plt.hist( gasclip[1,:,:].ravel(), bins=350)
            #stat_array[:,:,i] = np.array( [[hm, hs, hx, bluehist], [cm, cs, cx, greehist]],dtype=object)
            stat_array[:,:,i] = np.array( [[hm, hs, hx], [cm, cs, cx]],dtype=float)
            pass
        #really quick I'm just gonna save this information so I dont have to compute it everytime
        stor = fit.PrimaryHDU(stat_array)
        stor.writeto('scanstats.fits')
        #uhh let's plot the mean of h2o over time
        fig,ax = plt.subplots()
        fig.figsize=(12,6)
        fig.dpi=120
        ax.scatter( a['julian date'], stat_array[0,0,:],marker='+',s=1.3, label='H2O means')
        ax.scatter( a['julian date'], stat_array[1,0,:],marker='x',s=1., label='CO2 means')
        ax.hlines(0, xmin=a['julian date'][0], xmax=a['julian date'][-1],color='k',lw=0.8)
        ax.set_ylim((-0.0002,None))
        plt.legend()
        plt.show(block=True)
        pass
    elif mode == '3':
        scanstats = fit.open('/home/antojr/codespace/scanstats.fits')
        stat_array = scanstats[0].data
        
        fig,ax = plt.subplots()
        fig.figsize=(12,6)
        fig.dpi=120
        ax.hlines(0, xmin=a['julian date'][0], xmax=a['julian date'][-1],color='k',lw=0.8)
        ax.scatter( a['julian date'], stat_array[0,0,:],marker='+',s=1.3, label='H2O means')
        ax.scatter( a['julian date'], stat_array[1,0,:],marker='x',s=1., label='CO2 means')
        ax.set_ylim((-0.00002,0.00005))
        plt.legend()
        plt.show(block=True)
        pass
    elif mode == '4':
        #i want to make and plot at will histograms of the gas maps
        #stacked by day of year
        histos = []
        ii = np.arange(298,322,dtype=int)
        for i in range(len(ii)):
            batch = ( ii[i] == a['DOY'] )
            #go the histogram operation
            gases, headd = unloadCube( list(range(1321))[batch], cubename='cube_gasmaps_final_enhance_v6.fit' )
            gases[0].shape
            #plt.hist()
            #histos.append( histogram_product )
        #histos will come out with 24 histograms in it?

    else:
        pass
    #
    pass
else:
    pass
pass

## unload the cube and its data



'''
##  derive some stats from that mans
mean = np.nanmean(imag,axis=(1,2))
#print(mean.shape)
#h2o_mean, co2_mean, dus_mean = np.nanmean(imag[0,:,:]), np.nanmean(imag[1,:,:]), np.nanmean(imag[2,:,:])
medi = np.nanmedian(imag,axis=(1,2))
stan = np.nanstd(imag,axis=(1,2))
var = stan**2
maxx = np.nanmax(imag,axis=(1,2))
for i in (0,1,2):
    print(mean[i],medi[i],stan[i],var[i],maxx[i])

## debugging, cross-checking, etc
vall = gasmaps[0,14,202]
print(vall)

fig,ax = plt.subplots()
fig.figsize=(10,5.6)
fig.dpi=140
ax.hist(gasmaps[1,:,:].ravel(),bins=350)
#ax.vlines((mean[0], mean[0]+var[0]), ymin=0,ymax=50)
ax.set_yscale('log')
ax.set_ylim(1,None)
plt.show()
'''
