#Antoine

import numpy as np
from datafunctions import selector


a = np.load('a_cometmeta.npy')

t_zero_h = np.load('times_zeros_h.npy')
t_zero_c = np.load('times_zeros_c.npy')
t_timeline = np.load('times_for_derivatives.npy')
t1_h = np.load('times_indexes_h1.npy')
t1_c = np.load('times_indexes_c1.npy')
t2_h = np.load('times_indexes_h2.npy')
t2_c = np.load('times_indexes_c2.npy')
ddy_h = np.load('lc_deri2_h.npy')
ddy_c = np.load('lc_deri2_c.npy')

scanid_h = [ (a[ selector(t_timeline[t1_h[i]]) ]['DOY'], a[selector(t_timeline[t1_h[i]])]['exposure id'])  for i in range(len(t1_h))  ]

for i in range(len( t1_h)):
    #print( a[selector(t_timeline[t1_h[i]])]['julian date'] - a[selector(t_zero_h[i])]['julian date'] )
    print("scan: ", scanid_h[i], " second-d: ", ddy_h[t1_h[i]] )
#for i in t_zero_h:
#    print(a[selector(i)]['DOY'], ',', a[selector(i)]['exposure id'])
#for i in t_zero_c:
#    print(a[selector(i)]['DOY'], ',', a[selector(i)]['exposure id'])
