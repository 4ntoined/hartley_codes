#Antoine

import numpy as np
#from playingwithdata import a

#a=np.load('a_cometmeta.npy')

meta_expid, meta_fcount = np.loadtxt('/home/antojr/stash/datatxt/filtered_list.txt',dtype=str,skiprows=1,unpack=True,usecols=(1,4))
doyy = [int(i[:3]) for i in meta_expid ]
fcount = [ int(i) for i in meta_fcount ]

#datt = np.loadtxt('/home/antojr/stash/datatxt/positions_edit.dat',skiprows=2,dtype=float)
nsflip_list = np.zeros_like(doyy, dtype=int)
double_list = np.zeros_like(doyy, dtype=int)
nframes = np.zeros_like(doyy,dtype=int)
for i in range(len(doyy)):
    doy = doyy[i]
    nframes[i] = fcount[i]
    #setting double-exposed marker
    if doy <= 300 or (doy >= 309 and doy <= 320):
        double_list[i] = 1
        nframes[i] *= 2
    #setting the nsflip when it happens, all post-encounter
    if doy >= 309:
        nsflip_list[i] = 1
    pass
with open('nsflip_doubled_3.txt','w') as f:
    f.write('julian date / ns_flip / doubled / number of frames (final image) | created by meta_nsflip\n')
    for i in range(len(nsflip_list)):
        f.write(f'{nsflip_list[i]} {double_list[i]} {nframes[i]}\n')
    pass
