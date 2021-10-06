#Antoine
#this one is gonna pull up the mri small aperture photometry and interpolate
#those data with the julian dates of all my scans 
#no reason why this cant go in the mega-array
#that's a new name

import numpy as np
from matplotlib import pyplot as plt
import scipy.interpolate as pol
from playingwithdata import a

cols = np.concatenate((np.arange(1,3),np.arange(4,49)))
tabl = np.loadtxt("/chiron4/antojr/mri_photometry/data/aper_phot.tab",dtype=float,usecols=cols)
filenames, image = np.loadtxt("/chiron4/antojr/mri_photometry/data/aper_phot.tab",dtype=str,usecols=(0,3),unpack=True)
#tabl has had the 1st (0th) and 4th (3rd) columns removed, all the 
#flux columns are shifted 2 down,, 14 -> 12
clear = []
clear_i = []
#print(len(tabl))
for i in range(len(tabl)):
    if image[i] == "CLEAR1": #excluding non clear1 images
        clear.append(tabl[i])
        clear_i.append(i)
#print(len(clear))
tabl = np.array(clear,dtype=float)
#replace -99 with nans
err2= np.argwhere(tabl==-99.)
#print(err[])
#print(err2)
tabl[err2[:,0],err2[:,1]] = np.nan
mri_time = tabl[:,0]
hri_time = a['julian date']
## [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 248]
## 13 - 47 ideally
# I will for now focus on 3, 7, 12, 20
#gonna interpolate over my scan times have to set up the function though
inter1 = pol.interp1d(mri_time,tabl[:,16])
inter2 = pol.interp1d(mri_time,tabl[:,20])
inter3 = pol.interp1d(mri_time,tabl[:,24])
inter4 = pol.interp1d(mri_time,tabl[:,28])
y_1 = inter1(hri_time)
y_2 = inter2(hri_time)
y_3 = inter3(hri_time)
y_4 = inter4(hri_time)


outt = open("mri_interpolated.txt","w")
outt.write("3-pixel aperture // 7 // 12 // 20\n")
for i in range(len(y_1)):
    outt.write(f"{y_1[i]} {y_2[i]} {y_3[i]} {y_4[i]}\n")
    pass    
outt.close()

fig,ax = plt.subplots()
fig.figsize = (10,5.625)
fig.dpi = 140

ax.scatter(hri_time[215:230],y_4[215:230],label="mri flux",color="orange")
#ax.set_xlim()
#ax.set_ylim()
ax.legend(loc="best")
ax.set_xlabel("julian date")
ax.set_ylabel("flux")
ax.set_title("light curve possibly")
plt.show()
