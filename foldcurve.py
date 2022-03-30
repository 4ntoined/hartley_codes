#Antoine
#folding light curve

import numpy as np
import matplotlib.pyplot as plt
from PyAstronomy.pyasl import foldAt
from playingwithdata import a

def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
def boxcar_smooth(data, result_array):
    #result_array should be the same shape as data
    result_array[1:-1] = np.sum((data[1:-1],data[0:-2],data[2:]),axis=0) / 3.
    result_array[0] = np.sum((data[0],data[1])) /2.
    result_array[-1] = np.sum((data[-1],data[-2])) / 2.
    return result_array
    
date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v6.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
#date, h2o, co2 , dyst = np.loadtxt("/home/antojr/stash/datatxt/gas_light_curve_v5.txt",dtype=float,unpack=True,skiprows=1)
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
y1_h2o = h2o * overdist2
y1_co2 = co2 * overdist2
y1_dus = dyst * overdist2
### clearing out the zeros ###
mask = np.ones(len(y1_h2o),dtype=bool)
mask[np.argwhere(h2o < 1e-10)] = False
y1_h2o = y1_h2o[mask]
date = date[mask]
y1_co2 = y1_co2[mask]
y1_dus = y1_dus[mask]

# folding
peri = 2.3
x_foldtimes, epochs = foldAt(date,peri,T0=2455508.0,getEpoch=True)
epochs = epochs.astype(int)

#for i in range(2):
#    print(x_foldtimes[i],epochs[i])
dork = np.array([date,y1_h2o,y1_co2,y1_dus,x_foldtimes,epochs],dtype=object)
#print(dork[5,1320])
### dork[x,y] x calls a column, date h2o co2 phase epoch / y calls a row/scan
epic_i = []
for i in range(np.min(epochs),np.max(epochs)+1): #loop through different epochs
    #take epoch from dork
    ind = np.argwhere(epochs==i)
    epic_i.append(ind)
#print(x_foldtimes[epic_i[6]])
###
#like over here
#we will smooth the already epoch-sliced curves
smooth_fold = []    #for smoothing the curves
normed = []         #for normalizing
smonorm = []
for i in range(len(epic_i)):
    smo_h = np.zeros_like(y1_h2o[epic_i[i]],dtype=float)
    smo_c = np.zeros_like(y1_co2[epic_i[i]],dtype=float)
    smo_d = np.zeros_like(y1_dus[epic_i[i]],dtype=float)
    smoo = np.array((boxcar_smooth(y1_h2o[epic_i[i]], smo_h), boxcar_smooth(y1_co2[epic_i[i]], smo_c), boxcar_smooth(y1_dus[epic_i[i]], smo_d)),dtype=float)
    smooth_fold.append(smoo)
    normo = normalize(y1_co2[epic_i[i]])
    normo_h = normalize(y1_h2o[epic_i[i]])
    normo_d = normalize(y1_dus[epic_i[i]])
    normm = np.array((normo_h,normo,normo_d),dtype=float)
    normed.append(normm)
    norma = np.array((normalize(smoo[0]),normalize(smoo[1]),normalize(smoo[2])),dtype=float)
    smonorm.append(norma)
###
#so normed[i] gives 1 epoch, x_foldtimes[epic_i[i]] gives the phase point for each point in epoch
#let's smooth each normed
#i have to check my notes but I am figuring that we should smooth before normalizing so
#I need to edit way above here

##################
#### plotting ####
###################
#ax.scatter(dateA,y1_h2o,s=1)
#ax.scatter(x_foldtimes[epic_i[6]],normed[6],s=1)
#not sure if there's a way for me to automate this (where the pre/post encounter split is in epochs) exactly... 
Pre = range(0,5)
Post = range(5,len(normed))
for j in (Pre,Post): #one plot for pre one for post
    fig,ax = plt.subplots()
    fig.figsize = (8,6)
    fig.dpi = 140
    for i in j:
        ax.scatter(x_foldtimes[epic_i[i]],normed[i][1,:,0],s=1,color='green',label='CO2')
        ax.scatter(x_foldtimes[epic_i[i]],normed[i][0,:,0],s=1,color='blue',label='H2O')
        #ax.scatter(x_foldtimes[epic_i[i]],normed_d[i],s=1,color='red',label='dust')
    ax.set_xlabel("phase")
    ax.set_ylabel("radiance, normalized")
    if j[0]>4.5:
        ax.set_title("Folded Gas Curves, post-encounter")
    else:
        ax.set_title("Folded Gas Curves, pre-encounter")
    plt.show()
    pass
