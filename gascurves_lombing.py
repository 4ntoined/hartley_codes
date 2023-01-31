#Antoine
#doing some experimenting with splines

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import lombscargle as lomb
from scipy.signal import argrelmax
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from making_plots import plot_scatter
#from cometmeta import a
#from boom import ps, x_days

def masking(data,flg):
    """
    data: np.ndarray shaped (1321,)
    flg: array like (1321) boolean of what to mask
    """
    global a
    #setting the flags and mask
    ap_flag = flg.astype(bool)
    good_mask = ~ap_flag
    #applying the mask to the given array
    datam = data[good_mask].copy()
    return datam
def prepost_split(data, timedata):
    """
    data: np.ndarray to be split
    timedata: array-like, time elements in data were taken
    """
    global tencounter
    predata, posdata = data[ timedata < tencounter ].copy(), data[ timedata > tencounter  ].copy()
    return (predata, posdata)
def center_curve(data, timedata, para_guess=(1.,2.)):
    """
    data: gascurve segment, should give already mean-normalized!
    timedata: time data were taken
    will deslope curve and 0-mean it
    """
    pars, cova = curve_fit(liner, timedata, data, p0=para_guess)
    fitline =  liner(timedata, pars[0], pars[1])
    gascenter = data - fitline
    return (gascenter, fitline)
def liner(x,m,b): return m*x+b
a = np.load('a_cometmeta.npy')
tencounter = 2455505.0831866

if __name__ == '__main__':
    #rng = np.random.default_rng()
    #date, h2o, co2 , dus = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
    #new data I saved 
    #bigg = np.load('/home/antojr/codespace/gg_curves_x4_corrected.npy')
    #h2= bigg['h2o'].copy()
    #c2= bigg['co2'].copy()
    #d2= bigg['dust'].copy()
    #date2= bigg['jd'].copy()
    #flag= bigg['flags'].copy()
    #date2, h2, c2, d2, flag = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x3_424km-corrected.txt', dtype=float,unpack=True,skiprows=1)
    loaded = np.load('/home/antojr/codespace/results_code/gascurves_x5-dorrect.npy')
    h2, c2, d2, flag = loaded['h2o'], loaded['co2'], loaded['dust'], loaded['clip flag']
    dist = a['comet dist'].copy()
    ## getting out no nucleus or aperture too big
    go1 = [] #for applying mask
    for i in (h2, c2, d2, a): go1.append( masking(i, flag)   )
    hm,cm,dm,am = go1
    ## separating into PRE & POST ##
    go2 = []
    jdm = am['julian date'].copy()
    for i in (hm,cm,dm,am): go2.append( prepost_split(i, jdm) )
    superh, superc, superd, supera = go2
    ### SANITY - CHECK - PLOT ###
    #plotthis = [ [supera[0]['julian date'],superh[0]] , [supera[1]['julian date'], superc[1]]  ]
    #plot_scatter( plotthis, make_label=True, labels=['pre H','post C'])
    ### ##################### ###
    hpre, hpos = superh
    cpre, cpos = superc
    apre, apos = supera
    #putting time into encounter units
    t_pre = apre['julian date'] - tencounter
    t_pos = apos['julian date'] - tencounter
    ################################################################
    ## undoing slope in gascurves
    #take the mean
    cmean_pre = np.mean(cpre) #to "normalize" pre encounter
    cmean_pos = np.mean(cpos) #to "normalize" post encounter
    #go3 = []
    #for i in ( (hpre,cmean_pre),( hpos,cmean_pos), (cpre,cmean_pre), (cpos,cmean_pos)): go3.append(i[0]*i[1] )
    #h_pre_mean, h_pos_mean, c_pre_mean, c_pos_mean = go3
    # estimate sloping of lightcurve
    # fitting lines
    # POST #
    #par_h2, covah = curve_fit(liner, t_pos, hpos/cmean_pos, p0=(-1.,2.))
    #par_c2, covac = curve_fit(liner, t_pos, cpos/cmean_pos, p0=(-1.,2.))
    #hcenter2 = hpos/cmean_pos - liner(t_pos,par_h2[0],par_h2[1])
    #ccenter2 = cpos/cmean_pos - liner(t_pos,par_c2[0],par_c2[1])
    # PRE #
    #par_h1, covah1 = curve_fit(liner, t_pre, hpre/cmean_pre, p0=(1.,2.))
    #par_c1, covac1 = curve_fit(liner, t_pre, cpre/cmean_pre, p0=(1.,2.))
    #hcenter1 = hpre/cmean_pre - liner(t_pre,par_h1[0],par_h1[1])
    #ccenter1 = cpre/cmean_pre - liner(t_pre,par_c1[0],par_c1[1])
    preguess = (1.,1.)
    posguess = (-1.,1.)
    hc1,fit1 = center_curve( hpre/cmean_pre, t_pre, para_guess=preguess )
    cc1,fit2 = center_curve( cpre/cmean_pre, t_pre, para_guess=preguess )
    hc2,fit3 = center_curve( hpos/cmean_pos, t_pos, para_guess=posguess )
    cc2,fit4 = center_curve( cpos/cmean_pos, t_pos, para_guess=posguess )
    ### SANITY CHECK PLOT ###
    plot4=False
    plot5=False
    if plot4: #data and fit line comparison
        fig,ax=plt.subplots()
        # plot data
        ax.scatter( np.concatenate( (t_pre, t_pos), axis=0 ),np.concatenate((hpre/cmean_pre,hpos/cmean_pos),axis=0), label='h' )
        ax.scatter( np.concatenate( (t_pre, t_pos), axis=0 ),np.concatenate((cpre/cmean_pre,cpos/cmean_pos),axis=0), label='c' )
        ax.plot( t_pos, fit3 ,label='post h line')
        ax.plot( t_pos, fit4 ,label='post c line')
        ax.plot( t_pre, fit1 ,label='pre h line')
        ax.plot( t_pre, fit2 ,label='pre c line')
        ax.legend(loc='best')
        plt.show()
    if plot5: #centered gases
        fig,ax=plt.subplots()
        ax.plot( t_pos, hc2, label='center h post')
        ax.plot( t_pos, cc2+2., label='center c post +2')
        ax.plot( t_pre, hc1, label='center h pre')
        ax.plot( t_pre, cc1+2., label='center c pre +2')
        ax.legend(loc='best')
        plt.show()
    ##################################################################
    ## lomb-scargle
    many = int(4.444e4)
    x_peri = np.linspace(0.2*2.*np.pi,12.*2.*np.pi,many)
    pgrams = []
    go5 = (hc1,cc1,hc2,cc2)
    do5 = (t_pre,t_pre,t_pos,t_pos)
    for i in (0,1,2,3):
        pgrams.append( lomb(do5[i], go5[i], x_peri ,normalize=True, precenter=False) )
    pgram_h1, pgram_c1, pgram_h2, pgram_c2 = pgrams

    #print(maxc)
    #print(x_peri[maxc])
    #print(pgram_c[maxc])
    #print(jdb[-1],jdb[0])
    ##################################################################

    ################################################################
    #x_peri is angular frequency
    #y_peri is ordinary frequency
    #p_peri is period, hours
    y_peri = x_peri / (2.*np.pi)
    p_peri = (1./y_peri)*24.
    #saving
    saving_this=True
    if saving_this:
        #for i in range(len(p_peri)):
        pgram_sav = [ (p_peri[i], pgram_h1[i], pgram_c1[i], pgram_h2[i], pgram_c2[i]) for i in range(len(p_peri)) ]
        dtyp = np.dtype([ ('period','f8'),('pre h','f8'),('pre c','f8'),('pos h','f8'),('pos c','f8') ])
        pgram_arr = np.array( pgram_sav, dtype=dtyp )
        np.save('results_code/pgrams.npy',pgram_arr)

    
    
    
    d1,d2 = 2455505.5, 2455519.5
    #d1,d2 = 2455494.5, 2455519.5
    fig,ax = plt.subplots()
    fig.figsize = (10,5.6)
    fig.dpi=140
    
    #################### data ##########################################
    #ax.scatter(jdb,h2b/cmean,s=0.5)
    #ax.scatter(jda,h2a/cma,s=0.5)
    #ax.plot(time_spl,hspline,color='indigo')
    #ax.scatter(jdb,c2b/cmean,s=0.5)
    #ax.scatter(jda,c2a/cma,s=0.5)
    #ax.plot(jdb,liner(jdb,parah[0],parah[1]))
    #ax.plot(jda,liner(jda,parah1[0],parah1[1]))
    #ax.scatter(jdb,hcenter,s=0.7)
    #ax.scatter(jdb,ccenter,s=0.7)
    #ax.plot(jdb,liner(jdb,parac[0],parac[1]))
    #ax.plot(jda,liner(jda,parac1[0],parac1[1]))
    ################### p-grams ##############################################
#    ax.plot(p_peri*(2*np.pi)**1,pgram_h,color='cornflowerblue',label='h2o')
#    ax.plot(p_peri*(2*np.pi)**1,pgram_c,color='lightgreen',label='co2')
    #ax.plot(p_peri*(2*np.pi)**1,pgram_h1,color='cornflowerblue',label='h2o')
    #ax.plot(p_peri*(2*np.pi)**1,pgram_c1,color='lightgreen',label='co2')
    #ax.plot(x_peri,pgram_h-pgram_c,color='red', label='diff')
#    ax.plot(x_peri,pgram_h2,color='blue', label='h post')
#    ax.plot(x_peri,pgram_c2,color='red', label='c post')
    ax.plot(p_peri,pgram_h2,color='blue', label='h post')
    ax.plot(p_peri,pgram_c2,color='red', label='c post')
    ax.plot(p_peri,pgram_h1,color='green', label='h pre')
    ax.plot(p_peri,pgram_c1,color='purple', label='c pre')
    #ax.plot(spl_freq, spl_hgram, color='darkblue', label='spl,h,pgram')
    #ax.plot(spl_freq, spl_hgram2, color='darkblue', label='spl,h,pgram no precenter')
    ################### reconstructions ############################
    #ax.plot(x_recon+jdb[0], (ps[0]+ps[1]+ps[5] ) *5e16, label='reconstructed')
    #ax.plot(x_recon+jdb[0], (psum)*6e17, label='reconstructed')
    #ax.plot(ps[0]+ps[1]+ps[5])
    #ax.plot(x_spl_recon+jdb[0], psum_spl_h*5e16, label='recon,spl,h')
    #ax.plot(x_spl_recon+jdb[0], ( pss_spl_h[0]+pss_spl_h[1]+pss_spl_h[3]  )*5e16, label='recon,spl,h,parts')
    
    ax.legend(loc='best')
    #ax.set_ylim(( 3e15, 1e17 ))
    #ax.set_xlim(( d1, d2 ))
    #ax.set_xlabel("time [days]")               #time
    #ax.set_xlabel("frequency [cycles/day]")     #frequency  
    ax.set_xlabel("period [hours]")             #period
    ax.set_ylabel("signal")
    ax.set_title("curvy curve")
    plt.show()
else:
    pass
