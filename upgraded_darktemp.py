#Antoine
#gonna reorganize the dark file

import numpy as np

def sorter(darkrow):
    money = darkrow[0]
    return float(money[0])

darktemp = np.loadtxt("dark_temp.dat",dtype=float,skiprows=1,usecols=(0,1,2,3,4,5,7))
exps = np.loadtxt("dark_temp.dat",dtype=str,skiprows=1,usecols=6)

darklist = [(darktemp[i,:],exps[i]) for i in range(len(darktemp))]
darklist.sort(key=sorter)

print(darklist)
newdarktemp = []
out = open("dark_temp_v2.dat","w")
out.write("julian date, mid-obs // temperature, K (smooth) // dark level, DN/ms // best fit level // exposure time // doy // exposure id // outlier flag\n")
for i in range(len(darklist)):
    eid = darklist[i][1]
    dat = darklist[i][0] #contains 7 bits of data: jd, dark, best fit, temp, doy, hotflag, exposure time
    strin = f"{dat[0]} {dat[1]} {dat[2]} {dat[3]} {dat[4]} {dat[5]} {eid} {dat[6]} \n"
    out.write(strin)
out.close()
#out = open("dark_temp_v2.dat","w")