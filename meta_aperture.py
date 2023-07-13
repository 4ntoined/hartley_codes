#Antoine
#this one will probe the cometocentric distance over time right

import numpy as np
from matplotlib import pyplot as plt
#from cometmeta import a

def sizeToRadius(apsize):
    ra = apsize/2
    rb = (apsize-1)/2
    return np.where(apsize%2 == 0, ra, rb)
def apsize(scale_data,view):
    """
    scale: array of floats, pixel scale for each scan in m/pxl
    view:  float, desired aperture side length in meters
    """
    ans = view / scale_data
    return ans
def saveit(dato):    
    return
###

meta_dir = '/home/antojr/stash/datatxt/filtered_list.txt'
saveto = '/home/antojr/codespace/bb_apsizes.npy'

#apers = np.load('apsizes_424800m.npy')
#errrs = np.load('aperror_141600.npy')
#errrs = np.load('aperror_424800m.npy')

meta_jd, meta_scl = np.loadtxt(meta_dir,skiprows=1,dtype=float,usecols=(2,6),unpack=True) #units of meters per pixel
###
#y_pscale_km = a['pixel scale'] / 1e3
#view = 4.24800e5 #meters
#ap_size = view / a['pixel scale'] #number of pixels needed for view
#np.save('apsizes_424km_floats.npy',ap_size)
vieww = 4.24800e5 #meters
app = apsize(meta_scl,vieww)
np.save(saveto,app)

#print(app)
'''
sizer = np.array(ap_size,dtype=int)
rads = sizeToRadius(sizer)
rads = rads.astype(int)

outt = open("apertureSizes_wild.txt","w")
outt.write("jd, aperture size, radius #for a 150km view\n")
for i in range(len(sizer)):
    outt.write(f"{a['julian date'][i]} {sizer[i]} {rads[i]}\n")
outt.close()
'''
#print(np.argwhere(apers > 3))

fig,ax = plt.subplots()
fig.figsize = (8,4.5)
fig.dpi = 140

ax.scatter(meta_jd,app,color="green",s=.7)
#ax.set_xlim((2455504.5,2455519.5))
#ax.set_yticks(np.arange(0,27))
#ax.set_title("aperture size for 150km view")
ax.set_ylabel("number of pixels")
ax.set_xlabel("julian date")
#plt.savefig("aperture_size2_50km.png")
ax.grid()
plt.show()
