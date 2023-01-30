#Antoine
#doing some experimenting with splines

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import lombscargle as lomb
from scipy.signal import argrelmax
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from cometmeta import a
#from boom import ps, x_days

def masking(day,ach,see,dus,flg):
    global a
    ap_flag = flg.astype(bool)
    good_mask = ~ap_flag

    date2m = day[good_mask].copy()
    h2m = ach[good_mask].copy()
    c2m = see[good_mask].copy()
    d2m = dus[good_mask].copy()
    am = a[good_mask].copy()
    halfway = 195 #194 index of last pre, 195 first post (after removals) 229-230, otherwise
    #print(am['julian date'][185:205])
    ##################################################################
    ## splitting between approach and unproach
    jda = date2m[:halfway].copy()
    jdb = date2m[halfway:].copy()
    h2a = h2m[:halfway].copy()
    h2b = h2m[halfway:].copy()
    c2a = c2m[:halfway].copy()
    c2b = c2m[halfway:].copy()
    d2a = d2m[:halfway].copy()
    d2b = d2m[halfway:].copy()
    return ((jda,jdb),(h2a,h2b),(c2a,c2b),(d2a,d2b),am)
def liner(x,m,b):
    return m*x+b
#rng = np.random.default_rng()
date, h2o, co2 , dus = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
#new data I saved 
bigg = np.load('/home/antojr/codespace/gg_curves_x4_corrected.npy')
h2= bigg['h2o'].copy()
c2= bigg['co2'].copy()
d2= bigg['dust'].copy()
date2= bigg['jd'].copy()
flag= bigg['flags'].copy()
date2, h2, c2, d2, flag = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x3_424km-corrected.txt', dtype=float,unpack=True,skiprows=1)
loaded = np.load('/home/antojr/codespace/results_code/gascurves_x5-correct.npy')
h2, c2, d2, flag = loaded['h2o'], loaded['co2'], loaded['dust'], loaded['clip flag']
dist = a['comet dist'].copy()
##################################################################
## getting out no nucleus or aperture too big
"""
ap_flag = flag.astype(bool)
good_mask = ~ap_flag
#print(np.count_nonzero(good_mask))
#print(np.count_nonzero(ap_flag))
date2m = date2[good_mask].copy()
h2m = h2[good_mask].copy()
c2m = c2[good_mask].copy()
d2m = d2[good_mask].copy()
am = a[good_mask].copy()
halfway = 195 #194 index of last pre, 195 first post (after removals) 229-230, otherwise
##################################################################
## splitting between approach and unproach
jda = date2m[:halfway].copy()
jdb = date2m[halfway:].copy()
h2a = h2m[:halfway].copy()
h2b = h2m[halfway:].copy()
c2a = c2m[:halfway].copy()
c2b = c2m[halfway:].copy()
d2a = d2m[:halfway].copy()
d2b = d2m[halfway:].copy()
#f2a = flag[:halfway].copy()
#f2b = flag[halfway:].copy()
"""
resi = masking(date2,h2,c2,d2,flag)
((jda,jdb),(h2a,h2b),(c2a,c2b),(d2a,d2b),am) = resi

################################################################
#ratting out slope in lightcurve
tencounter = 2455505.0831866
jda-=tencounter
jdb-=tencounter

cmean = np.mean(c2b)
cma=np.mean(c2a)

parah, covah = curve_fit(liner, jdb, h2b/cmean, p0=(-1.,2.))
parac, covac = curve_fit(liner, jdb, c2b/cmean, p0=(-1.,2.))

parah1, covah1 = curve_fit(liner, jda, h2a/cma, p0=(1.,2.))
parac1, covac1 = curve_fit(liner,jda,c2a/cma,p0=(1.,2.))

hcenter = h2b/cmean - liner(jdb,parah[0],parah[1])
ccenter = c2b/cmean - liner(jdb,parac[0],parac[1])

hcenter1 = h2a/cma - liner(jda,parah1[0],parah1[1])
ccenter1 = c2a/cma - liner(jda,parac1[0],parac1[1])

#print(paras,parasc)
##################################################################
## spline?
#s1, s2 = 0, 1321
#fitting_h = 5e34
#fitting_c = 5e34
#spl = UnivariateSpline(jdb[s1:s2], h2b[s1:s2],k=3,s=fitting_h)
#spl2 = UnivariateSpline(jdb[s1:s2], c2b[s1:s2],k=3,s=fitting_c)
##################################################################
## lomb-scargle
many = int(4.444e4)
x_peri = np.linspace(0.2,12,many)
pgram_c= lomb(jdb,hcenter,x_peri,normalize=True,precenter=False)
pgram_h = lomb(jdb,ccenter,x_peri,normalize=True,precenter=False)
pgram_c1= lomb(jda,hcenter1,x_peri,normalize=True,precenter=False)
pgram_h1 = lomb(jda,ccenter1,x_peri,normalize=True,precenter=False)

#print(maxc)
#print(x_peri[maxc])
#print(pgram_c[maxc])
#print(jdb[-1],jdb[0])
##################################################################
## lombing my splines
#bring in the splines
hspline = np.load('xspline_h2o5.npy')
cspline = np.load('xspline_co25.npy')
time_spl = np.load('xspline_times.npy')
maxs_spl = np.load('xspline_max5.npy')
#print(maxs_spl.shape)
spl_maxh, spl_maxc = (maxs_spl[0,:].copy(), maxs_spl[1,:].copy())
# lomb on the splines
spl_freq = np.linspace(0.01,4,int(1e4))
spl_hgram = lomb(time_spl, hspline, spl_freq, normalize=True, precenter=True)
spl_hgram2 = lomb(time_spl, hspline, spl_freq, normalize=True, precenter=False)
spl_cgram = lomb(time_spl, cspline, spl_freq, normalize=True)
# finding the peaks in the grams
peaks_spl_h = argrelmax(spl_hgram, order=2)
peaks_spl_c = argrelmax(spl_cgram, order=2)
#print(spl_hgram[peaks_spl_h])
# reconstructing the splines from the pgrams
freq_spl_h = spl_freq[peaks_spl_h]
freq_spl_c = spl_freq[peaks_spl_c]
pwer_spl_h = spl_hgram[peaks_spl_h]
pwer_spl_c = spl_cgram[peaks_spl_c]
x_spl_recon = np.linspace(0,jdb[-1]-jdb[0],1000)
parts_h = []
parts_c = []
for i in range(len(freq_spl_h)):
    parts_h.append( pwer_spl_h[i] * np.cos(1*freq_spl_h[i] * x_spl_recon))
for i in range(len(freq_spl_c)):
    parts_c.append( pwer_spl_c[i] * np.cos(1*freq_spl_c[i] * x_spl_recon))
pss_spl_h = np.array(parts_h, dtype=float)
pss_spl_c = np.array(parts_c, dtype=float)
psum_spl_h = np.sum(pss_spl_h,axis=0)
psum_spl_c = np.sum(pss_spl_c,axis=0)

######################## reconstructing ########################
maxc = argrelmax(pgram_c, order=1)
freqs = x_peri[maxc]
pwers = pgram_c[maxc]
x_recon = np.linspace(0,jdb[-1]-jdb[0],1000)
ps = []
for i in range(len(freqs)):
    ps.append( pwers[i]*np.cos(2*freqs[i] * x_recon) )
pss = np.array(ps, dtype=float)
psum = np.sum(pss,axis=0)
psum2 = np.sum(pss[1:,:], axis=0)
################################################################
d1,d2 = 2455505.5, 2455519.5
#d1,d2 = 2455494.5, 2455519.5
p_peri = (1./x_peri)*24.
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
ax.plot(p_peri*(2*np.pi)**1,pgram_h,color='cornflowerblue',label='h2o')
ax.plot(p_peri*(2*np.pi)**1,pgram_c,color='lightgreen',label='co2')
#ax.plot(p_peri*(2*np.pi)**1,pgram_h1,color='cornflowerblue',label='h2o')
#ax.plot(p_peri*(2*np.pi)**1,pgram_c1,color='lightgreen',label='co2')
#ax.plot(x_peri,pgram_h-pgram_c,color='red', label='diff')
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
