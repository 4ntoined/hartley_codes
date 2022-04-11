#gonna create the function of temperature over time, filling in fits header info
# for hri telemetry where needed, and dealing with outlier temps
#leggo
import numpy as np
import astropy.io.fits as fit
import matplotlib.pyplot as plt

def jd_sorter(timeline_candidate):
    #dig into each 3-point (time, smooth temp, not smooth temp)
    # and return julian date
    return timeline_candidate[0]
#hri telemetry stuff
hritemp = fit.open("/home/antojr/hartley2/calibration/temp_jd.fit")
hritemp = hritemp[0].data
hritemp[:,1]-=0.9
#data from scan fits headers where hri telemetry falls out
gaptimes,gaptem,gapsmo,expid = np.loadtxt("/home/antojr/stash/datatxt/gap_temps.dat",skiprows=1,unpack=True)
#compiling the timeline
temptimeline = []
for i in range(len(hritemp[:,0])):    #will collect all the hri telemetyr data
    temptimeline.append((hritemp[i,0],hritemp[i,1],np.nan))
## keeping it simple, I think gonna take jd and smooth temp
for i in range(len(gaptimes)):
    temptimeline.append((gaptimes[i],gapsmo[i],gaptem[i]))
## all the sauce should be here, now we need to sort
temptimeline.sort(key=jd_sorter)
# okay that should be all the sorting
print(len(temptimeline))
#for i in range(len(temptimeline[17500:18500])):
#    print(temptimeline[i+17500],i+17500)
ttimeline = np.array(temptimeline, dtype=float)
## manual fixing of temperature outliers
ttimeline[18444:18463,1] = 136.755

fig,ax = plt.subplots()
fig.figsize= (8,6)
fig.dpi=120
ax.scatter(ttimeline[:,0],ttimeline[:,1],s=1)
ax.set_xlim(2455493.5,2455519.5)
ax.set_ylim(136.7,137.36)
ax.set_xlabel("julian date")
ax.set_ylabel("temperature, kelvin")
plt.show()