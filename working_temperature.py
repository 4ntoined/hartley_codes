#some temperature experiments
import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
#should also come up with a julian date conversion
def julian_to_doy(julian_date):
    #2455494.50735550 2010-10-25T00:10:29.518
    #2455494.5 = (25 october midnight,) 298.0 + x
    # julian_date = x + doy
    #x = 2455494.5-298
    return julian_date - 2455196.5
def doy_to_stringdate(doy):
    #298 25 october, 304 31 october, 305 1 november
    #assuming not leap year (a la 2010)
    mm = 15
    for i in range(len(thirtyfirsts)):
        #check how many months have gone by
        if doy <= thirtyfirsts[i]: #check if day count surpasses month checkpoints #doy 1 = 1 jan, doy 0 is nonsense
            mm = i #when it does, take note of the month 1 jan, 2 feb, 12 dec
            break
    dd = doy - thirtyfirsts[mm-1]
    return str(np.floor(dd)) +"-"+ months_string[mm]

###marking the days of the year where the month turns over###
daysmonths = [31,28,31,30,31,30,31,31,30,31,30,31]
i=0
thirtyfirsts = [0]
while i<len(daysmonths)-1:
    thirtyfirsts.append(thirtyfirsts[-1]+daysmonths[i])
    i+=1
#print(thirtyfirsts)
months_string = ["Buf","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
#print(doy_to_stringdate(304))
##############################################################

temp1 = fits.open("temp_jd.fit")
temp1.info()
temp1 = temp1[0].data
temp2 = fits.open("smooth_tem.fit")
temp2.info()
temp2 = temp2[0].data
temp1[:,1]-=0.9

###extra data thanks to calibrated file temps
timess,tem,smotem,expid = np.loadtxt("gap_temps.dat",skiprows=1,unpack=True)

#gonna interpolate these once smoothed temperatures with julian date
tlin = interp1d(temp1[:,0],temp1[:,1],kind='linear')
tcube = interp1d(temp1[:,0],temp1[:,1],kind='cubic')
qlin = interp1d(timess,smotem, kind='linear', bounds_error=False)

#gonna import scan observation jd for comparison
#scan_dat = np.loadtxt("Hartley_flyby_IR_data_table.dat",delimiter = " ",skiprows=5,usecols= 4,comments="DOY")
scan_file = open("Hartley_flyby_IR_data_table.dat","r")
scan_timeline = []
expos=[]
for i in scan_file:
    if i[0:2] == "hi":
        words = i.split()
        tyme = float(words[4])
        expo = int(words[3])
        scan_timeline.append(tyme)
        expos.append(expo)
    #print("working..")
scan_file.close()


scan_times = np.array(scan_timeline)
#print(scan_times.shape)
#print(scan_times)

#interpolated temperatures at the julian date of scans
y_lin = tlin(scan_times)
y_cub = tcube(scan_times)
q_lin = qlin(scan_times)
#we can convert from julian date to doy for convenience in the plot
scan_times_doy = julian_to_doy(scan_times)
x_temp = julian_to_doy(temp1[:,0])
timess_doy = julian_to_doy(timess)

#let's write some data
fout = open("scan_date_temp.dat","w")
fout.write("Antoine W., May 2021\n")
fout.write("day of year // exposure id // temperature (interpolated from HRI telemetry) // julian date // date and month\n")
for i in range(len(y_lin)):
    fout.write(f"{scan_times_doy[i]} {expos[i]} {y_lin[i]} {scan_times[i]} {doy_to_stringdate(scan_times_doy[i])}\n")
    #print("writing...")
fout.close()

#print(julian_to_doy(2455512.1))
#print(doy_to_stringdate(julian_to_doy(2455512.1)))

store = 0.
fout2 = open("lookingForGaps.dat","w")
fout3 = open("lookingForGaps_theGaps.dat","w")
fout2.write("time since *last* temperature point (days) :: julian date of temperature point\n")
fout2.write("20 minutes = 0.013888... days\n")
gaps = []
gap_index = []
for i in range(len(temp1[:,0])):
    diff = temp1[i,0] - store
    store = temp1[i,0]
    if diff > 0.0139:
        print(diff, end='')
        print(f" :: {temp1[i,0]} :: {i}")
        fout3.write(f"{diff} {temp1[i,0]}\n")
        gaps.append(temp1[i,0])
        gap_index.append(i)
    fout2.write(f"{diff} {temp1[i,0]}\n")
fout2.close()
fout3.close()
print(gap_index)

gaps_doy = []
for i in gaps:
    gaps_doy.append(julian_to_doy(i))

#here's some plotting
fig, ax = plt.subplots()
fig.figsize=(8,6)
fig.dpi=120

for i in range(1,len(gap_index)):
    ax.plot(x_temp[gap_index[i-1]:gap_index[i]],temp1[gap_index[i-1]:gap_index[i],1],color='darkorange',lw=.3)
    #ax.scatter(scan_times_doy[gap_index[i-1]:gap_index[i]],y_lin[gap_index[i-1]:gap_index[i]],color='red',s=1.)
##ax.plot(x_temp,temp2,label="extra smooth temp",color='red',lw=.3,zorder=2)
#ax.plot(timess_doy,tem,label="optbent")
ax.scatter(timess_doy,smotem, label="smobent",s=1,zorder=5,color='purple')
ax.scatter(timess_doy,tem, label="temp",s=1,zorder=4,color='red')
#ax.scatter( scan_times_doy, q_lin, label = "scans on smobent",s=3,color='red', zorder =6)

#ax.scatter(scan_times_doy,y_cub,label="scans, cubic interp",color='blue',s=.8,zorder=4)
###################
#scaling and things
#log scale
#ax.set_yscale("log")
#ticks and lines
#ax.set_xticks(x_temp)
ax.vlines(gaps_doy,ymin=136,ymax=138,lw=0.5,color='pink')
#xlimits
#ax.set_xlim((2455497,2455519))
ax.set_xlim((297.5,321.5))
ax.set_xlim((317.5,319))
#ylimits
ax.set_ylim((136.2,137.8))
#ax.set_ylim((136.7,136.9))
####################
#text related things
ax.legend(loc='best')
ax.set_xlabel("day of year 2010")
ax.set_ylabel("temp K")
#ax.grid(which="both")
ax.set_title("temp over time")
plt.show()