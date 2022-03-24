#Antoine

import numpy as np
from playingwithdata import a
#datt = np.loadtxt('/home/antojr/stash/datatxt/positions_edit.dat',skiprows=2,dtype=float)
nsflip_list=np.zeros_like(a['DOY'], dtype=int)
double_list = np.zeros_like(a['DOY'], dtype=int)
nframes = np.zeros_like(a['DOY'],dtype=int)
for i in range(len(a['DOY'])):
    doy = a['DOY'][i]
    nframes[i] = int(a['filename'][i][19:22])
    #setting double-exposed marker
    if doy <= 300 or (doy >= 309 and doy <= 320):
        double_list[i] = 1
        
    #setting the nsflip when it happens, all post-encounter
    if doy >= 309:
        nsflip_list[i] = 1
    pass

with open('nsflip_doubled.txt','w') as f:
    f.write('julian date / ns_flip / doubled \n')
    for i in range(len(nsflip_list)):
        f.write(f'{a["julian date"][i]} {nsflip_list[i]} {double_list[i]}\n')
    pass
