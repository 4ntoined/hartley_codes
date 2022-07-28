#Antoine
#

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as fit
from cometmeta import a
from datafunctions import selector, selector_prompt

select = selector_prompt(default='307 4000011')
dato = fit.open( a['directory path'][select] + '/cube_gasmaps_final_enhance_v6.fit')
#wavo = fit.open
gasmaps = dato[0].data
colos, ysize, xsize1 = gasmaps.shape
#imag = gasmaps.copy()
imag = gasmaps[:,:,170:]
xsize2 = imag.shape[2]

mean = np.nanmean(imag,axis=(1,2))
#print(mean.shape)
#h2o_mean, co2_mean, dus_mean = np.nanmean(imag[0,:,:]), np.nanmean(imag[1,:,:]), np.nanmean(imag[2,:,:])
medi = np.nanmedian(imag,axis=(1,2))
stan = np.nanstd(imag,axis=(1,2))
var = stan**2
maxx = np.nanmax(imag,axis=(1,2))
for i in (0,1,2):
    print(mean[i],medi[i],stan[i],var[i],maxx[i])
fig,ax = plt.subplots()
fig.figsize=(10,5.6)
fig.dpi=140
ax.hist(imag[0,:,:])
ax.vlines((mean[0], mean[0]+var[0]), ymin=0,ymax=50)
plt.show()

