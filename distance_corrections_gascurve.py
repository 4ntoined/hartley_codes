#Antoine
#distance_corrections_gascurve
#gonna use this to make the necessary corrections to my fixed phys. size aperture

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from datafunctions import selector
from making_plots import plot_scatter

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
#def figg():
    #fig,ax = plt.subplots()
    #fig.figsize=(10,6)
    #fig.dpi=140   
    #return fig, ax
#def axxx(figgs, axxs, ymax=1., d1=2455512.5, d2=2455514.5):
    #axxs.hlines((0.),xmin=297,xmax=322,label="zero",color='k',linewidth=0.6,zorder=1)
    #axxs.hlines((0.),xmin=297.,xmax=322.,label="zero",color='k',linewidth=0.6,zorder=1)
    #axxs.set_xlim(d1,d2)
    #axxs.set_ylim(None, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    #axxs.set_ylim(-ymax*0.07, ymax)#-8e-6,ymax)#-ymax*0.07, ymax)
    #axxs.legend(loc="best")
    #axxs.set_xlabel("Day of year")
    #axxs.set_ylabel("Flux [$\propto W/m^2$]")
    #axxs.set_ylabel("$CO_2$/$H_2O$")
    #ax.set_title("")
    #return
a = np.load('a_cometmeta.npy')
if __name__ == '__main__':
    ####################################################################################
    ########### GASES ###########
    ## load up the lc
    uncorrect_curves = np.load('/home/antojr/codespace/results_code/gascurves_x7.npy')
    uc = uncorrect_curves
    ha, ca, da, flag_a = uncorrect_curves['h2o'].copy(),uncorrect_curves['co2'].copy(),\
        uncorrect_curves['dust'].copy(),uncorrect_curves['clip flag'].copy()
    herr, cerr, derr = uc['h error'].copy(),uc['c error'].copy(),uc['d error'].copy()
    hrej, crej, drej = uc['num hrej'].copy(),uc['num crej'].copy(),uc['num drej'].copy()
    #print(uncorrect_curves[0])
    ## MASKING ## throwing out the clipped or no nucleus points
    go1 = [] 
    for i in (ha, ca, da, a, herr, cerr, derr, hrej, crej, drej): go1.append( masking(i, flag_a)   )
    hd,cd,dd,ad,herr_d, cerr_d, derr_d, hrejd, crejd, drejd = go1
    #
    ## STERADIANS ## correcting for correct pixel size for unit purposes 1e-10 steradians per pixel
    steradians = []
    for i in (hd,cd,dd, herr_d, cerr_d, derr_d): steradians.append( i*1e-10 )
    hc, cc, dc, herr_c, cerr_c, derr_c = steradians
    ## DISTANCE CORRECTION ## correcting for distance flux etc
    correcting = []
    #f it, we ball
    # 4(pi)D^2
    dist_correct = 4.*np.pi* ad['comet dist'].copy() **2. #this will undo the /m^2 in the lightcurves, returning just W
    for i in (hc,cc,dc, herr_c,cerr_c,derr_c): correcting.append( i * dist_correct )
    hb, cb, db, herr_b, cerr_b, derr_b = correcting
    ## PACKING AND SAVING RESULTS ##
    correcter = [ (hb[i],cb[i],db[i],herr_b[i],cerr_b[i],derr_b[i],hrejd[i],crejd[i],drejd[i]) for i in range(len(cb)) ]
    gastype = np.dtype([ ('h2o','f8'),('co2','f8'),('dust','f8'),('h error','f8'),\
        ('c error','f8'),('d error','f8'),('num hrej','c8'),('num crej','c8'),('num drej','c8')])
    correct_curves = np.array( correcter, dtype=gastype)
    #print(correct_curves[0])
    save_gas=True
    save_cometmeta=False
    if save_gas: np.save('/home/antojr/codespace/results_code/gascurves_x7-correct.npy',correct_curves)
    if save_cometmeta: np.save('/home/antojr/codespace/a2_cometmeta.npy-wild', ad)
    ####################################################################################
    ######### MRI ##############
    mridata = np.load('results_code/mri_aperturedata_3.npy')
    #mri_date = mridata['date'].copy()
    #mrii = mridata[ mri.dtype.names[4:17] ].copy()    #mri stuff minus the julian date
    # correcting distance on mri #
    #dist = a['comet dist'].copy()
    dist_interp = interp1d( a['julian date'], a['comet dist'], kind='linear', bounds_error=False, fill_value='extrapolate')
    dist_onmri = dist_interp( mridata['date'] )
    #mri14_correct = mri_14 * dist_onmri
    #
    mri_correct = []
    mri_correct1 = [ mridata['date'].reshape(-1,1) ]
    for i in range(4,17):
        mri_correct.append( mridata[ mridata.dtype.names[i] ] * dist_onmri )
        resu = mridata[ mridata.dtype.names[i] ] * dist_onmri
        mri_correct1.append( resu.reshape(-1,1) )
    goo1 = np.concatenate( mri_correct1, axis=1 )
    #goo = np.array(mri_correct)
    #goo1 = np.array(mri_correct1,)
    #print(goo.shape)
    #print(goo1[1])
    goo2 = [ tuple(goo1[i]) for i in range(len(goo1)) ] 
    #goo2 = np.array(goo2)
    #print(goo2[2])
    #for i in range(len(goo1)):
    dtyp = np.dtype([ ('date','f8'),\
        ('3-pix','f8'),('4-pix','f8'),('5-pix','f8'),('6-pix','f8'),('7-pix','f8'),\
        ('8-pix','f8'),('9-pix','f8'),('10-pix','f8'),('12-pix','f8'),('14-pix','f8'),\
        ('16-pix','f8'),('18-pix','f8'),('20-pix','f8') ])
    newmri = np.array(goo2,dtype=dtyp)
    #print(newmri['14-pix'])
    save_mri=False
    if save_mri: np.save('results_code/mri_dorrect.npy',newmri)

    #day_of_encounter = 2455505.0831866
    #doe = day_of_encounter
    #plot_scatter([ [a['julian date']-doe, cc],[ a['julian date']-doe, cb ] ],labels=['steraded','fully correct'], make_label=True)
    #saving our creations
    #correcter = np.ones((1321,4))
    #print(hb[0])
    #correcter = np.array( [[hb],[cb],[db],[flag_a]  ],dtype=uncorrect_curves.dtype )
    #correcter = np.concatenate(   hb.reshape((1,-1) ) )
    #print(correcter[0])
else:
    pass
pass

