#Antoine
#doing some experimenting with splines

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import argrelmax
import matplotlib.pyplot as plt
from cometmeta import a

#rng = np.random.default_rng()
date, h2o, co2 , dus = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
#date3, h3, c3, d3, flag3 = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x3_424km-corrected.txt', dtype=float,unpack=True,skiprows=1)
#date2, h2, c2, d2, flag = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x3_424km-dorrected.txt', dtype=float,unpack=True,skiprows=1)
date2, h2, c2, d2, flag = np.loadtxt('/home/antojr/stash/datatxt/gascurves_x4_424km-corrected.txt', dtype=float,unpack=True,skiprows=1)
dist = a['comet dist'].copy()
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
maxes = maxes.astype(int)
#unit converting distance to less annoying units
#dist /= 578375.623  #is smallest distance in set
###############################################
#controlling light for distance
#h2o = h2o / dist**2
#co2 = co2 / dist**2
#dus = dus / dist**2
#splitting between approach and unproach
#h2oa = h2o[:230].copy()
#h2ob = h2o[230:].copy()
#co2a = co2[:230].copy()
#co2b = co2[230:].copy()
#dus = dus[:230].copy()
#dus = dus[230:].copy()
#datea = date[:230].copy()
#dateb = date[230:].copy()
# getting out no nucleus or aperture too big
ap_flag = flag.astype(bool)
good_mask = ~ap_flag
#print(np.count_nonzero(good_mask))
#print(np.count_nonzero(ap_flag))
date2m = date2[good_mask].copy()
h2m = h2[good_mask].copy()
c2m = c2[good_mask].copy()
d2m = d2[good_mask].copy()
am = a[good_mask].copy()
#maxes = maxes[good_mask].copy()
halfway = 195 #194 index of last pre, 195 first post (after removals) 229-230, otherwise
# splitting between approach and unproach
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
# spline?
s1, s2 = 0, 1321
fitting_h = 2.838e34 #2.838e34
fitting_c = 1.802e34 #1.802e34 tightest fit
fitting_h3 = 3.000e34 #2.8 is too tight
fitting_c3 = 2.500e34 #2.8 was not tight enough
h5_spl = UnivariateSpline(jdb[s1:s2], h2b[s1:s2],k=5,s=fitting_h)
c5_spl = UnivariateSpline(jdb[s1:s2], c2b[s1:s2],k=5,s=fitting_c)
h3_spl = UnivariateSpline(jdb[s1:s2], h2b[s1:s2],k=3,s=fitting_h3)
c3_spl = UnivariateSpline(jdb[s1:s2], c2b[s1:s2],k=3,s=fitting_c3)

x_posttimes = np.linspace(jdb[0],jdb[-1],1000)

maxs_c5 = argrelmax(c5_spl(x_posttimes),order=2)
maxs_h5 = argrelmax(h5_spl(x_posttimes),order=2)
maxs_c3 = argrelmax(c3_spl(x_posttimes),order=2)
maxs_h3 = argrelmax(h3_spl(x_posttimes),order=2)
c5maxs = x_posttimes[maxs_c5]
h5maxs = x_posttimes[maxs_h5]
print('co2 peaks:\n',c5maxs)
print('h2o peaks:\n',h5maxs)
#print('diff:\n', 24*60* (x_posttimes[maxs_c5]-x_posttimes[maxs_h5]))
#maxs5 = np.array([h5maxs,c5maxs],dtype=float)
save_splines = True
if save_splines:
    h2o_spline = h5_spl(x_posttimes)
    co2_spline = c5_spl(x_posttimes)
    np.save('/home/antojr/codespace/zspline_times.npy', x_posttimes)
    np.save('/home/antojr/codespace/zspline_h2o5.npy', h2o_spline)
    np.save('/home/antojr/codespace/zspline_co25.npy', co2_spline)
    #np.save('/home/antojr/codespace/yspline_max5.npy', maxs5)
plot_it=True

d1,d2 = 2455505.5, 2455519.5
#d1,d2 = 2455494.5, 2455519.5
if plot_it:
    fig,ax = plt.subplots()
    fig.figsize = (16,5.6)
    fig.dpi=140
    
    #ax.scatter(jdb,h2b,s=1.,color='k',label='h2o data',zorder=4)
    ax.plot(x_posttimes,h5_spl(x_posttimes),color='cornflowerblue',label='h2o spline5',zorder=3)
    #ax.plot(x_posttimes,h3_spl(x_posttimes),color='orangered',label='h2o spline3',zorder=2)
    #ax.scatter(jdb,c2b,s=1.,color='k',label='co2 data',zorder=6)
    ax.plot(x_posttimes,c5_spl(x_posttimes),color='lightgreen',label='co2 spline',zorder=5)
    #ax.vlines(date2[maxes],ymin=-1e3,ymax=1e30,linewidth=0.7)
    #ax.vlines(h5maxs,ymin=-1e3,ymax=1e30,linewidth=0.7,color='cornflowerblue')
    #ax.vlines(c5maxs,ymin=-1e3,ymax=1e30,linewidth=0.7,color='lightgreen')
    
    ax.set_ylim(( 3e15, 1e17 ))
    ax.set_xlim((d1,d2))
    ax.legend(loc='best')
    ax.set_xlabel("time")
    ax.set_ylabel("signal")
    ax.set_title("curvy curve")
    plt.show()
pass

