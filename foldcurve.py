#Antoine
#folding light curve

import numpy as np
import matplotlib.pyplot as plt
from PyAstronomy.pyasl import foldAt
from playingwithdata import a

def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

dateA, h2oA, co2A , dystA = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v6.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
#peaks of the mri curve
maxes = maxes.astype(int)
#unloading mri curve
y_mri = a['mri 7-pixel'].copy()
y_mri *= 4e8
#unloading distance information
dist = a['comet dist'].copy()
overdist2 = 1/dist**2
#scaling so that distance isnt a bunch of crazy big numbers (compared to small gas brightness numbers)
rscl2 = co2[250] / overdist2[250] 
overdist2 *= rscl2
#gas curves
y1_h2o = h2oA * overdist2
y1_co2 = co2A * overdist2
y1_dus = dystA * overdist2
### clearing out the zeros ###
mask = np.ones(len(h2o),dtype=bool)
mask[np.argwhere(h2o < 1e-10)] = False
h2o = h2o[mask]
date = date[mask]
co2 = co2[mask]
dyst = dyst[mask]

# folding
peri = 2.25
x_foldtimes, epochs = foldAt(dateA,peri,T0=2455508.0,getEpoch=True)
epochs = epochs.astype(int)

#for i in range(2):
#    print(x_foldtimes[i],epochs[i])
dork = np.array([dateA,y1_h2o,y1_co2,y1_dus,x_foldtimes,epochs],dtype=object)
print(dork[5,1320])
### dork[x,y] x calls a column, date h2o co2 phase epoch / y calls a row/scan
epic_i = []
for i in range(np.min(epochs),np.max(epochs)+1): #loop through different epochs
    #take epoch from dork
    ind = np.argwhere(epochs==i)
    epic_i.append(ind)
#print(x_foldtimes[epic_i[6]])
##need to normalize
normed = []
for i in range(len())


#### plotting ####
##################
fig,ax = plt.subplots()
fig.figsize = (8,6)
fig.dpi = 140
#
#ax.scatter(dateA,y1_h2o,s=1)
ax.scatter(x_foldtimes[epic_i[6]],y1_co2[epic_i[6]],s=1)
#ax.set_ylim(0,1.5e-7)
#
ax.set_xlabel("phase")
ax.set_ylabel("radiance")
ax.set_title("Folded gas Curves")
plt.show()