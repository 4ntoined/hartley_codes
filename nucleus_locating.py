#Antoine
#comparing two sets of coordinates or something
import numpy as np
import matplotlib
import matplotlib.colors
import matplotlib.pyplot as plt
from playingwithdata import a
#
date1, x1, y1 = np.loadtxt("/home/antojr/stash/datatxt/nucleus_location_v3.txt",dtype=float,unpack=True)
date2, doy2, xo, yo, y2, x2 =np.loadtxt("/home/antojr/stash/datatxt/positions_edit.dat",dtype=float,skiprows=2,unpack=True)
#print(loc_old[1])
nsflags = a['nsflip flag'].copy()
doubles = a['doubled flag'].copy()
### to go from A to B: yB = yA when no nsflip, #frames(dont double?) xB = 255-xA
x2 = 255-x2
y2[]..
#
fig, ax = plt.subplots()
fig.figsize = (10,6)
fig.dpi = 140
#
ax.scatter(date1,x1)
ax.set_xlabel('julian date')
ax.set_ylabel('x-coordinate of nucleus')
ax.set_title('x-coord of nucleus [python coords]')
#
plt.show()
