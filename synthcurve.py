import numpy as np
from scipy.signal import lombscargle as lomb
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector
ind, tims = np.loadtxt('/home/antojr/stash/datatxt/scantimes.txt',unpack=True,skiprows=1)
lit27 = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v2_27.txt',unpack=True)
lit54 = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v2.txt',unpack=True)
lit27_area = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v3_27.txt',unpack=True) 
y_lit27 = lit27.copy()
y_lit54 = lit54.copy()
y_lit27area = lit27_area.copy()
x_t = tims.copy()
### splitting up the lcs before doing the most
cut = selector('2455504.1') +3 
x_t2 = x_t[cut:]
y542 = y_lit54[cut:]
y272 = y_lit27[cut:]

### some periodigrams
lots = int(1e4)
x_period = np.linspace(0.1, 5, lots)
#pgram54 = lomb(x_t2, y_lit54, x_period, normalize = False)
pgram54 = lomb(x_t2, y542, x_period, normalize = False)
pgram27 = lomb(x_t2, y272, x_period, normalize = False)

fig,ax=plt.subplots()
fig.dpi=140
fig.figsize = (10,6)
ax.plot(x_t, y_lit27 )
#ax.plot(x_t2,y542)
#ax.plot(x_period,pgram27)
#ax.plot(x_period,pgram54)
#xlims = (2455505.5,2455510.5)
#ax.set_xlim(xlims[0],xlims[1])
plt.show(block=False)

fig,ax=plt.subplots()
fig.dpi=140
fig.figsize = (10,6)
ax.plot(x_t, y_lit27area )
#ax.plot(x_t2,y542)
#ax.plot(x_period,pgram27)
#ax.plot(x_period,pgram54)
#xlims = (2455505.5,2455510.5)
#ax.set_xlim(xlims[0],xlims[1])
plt.show(block=False)

