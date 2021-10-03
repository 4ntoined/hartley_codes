#Antoine
#this code will organize my list of scan (last frames) information

import numpy as np

def sorter(scanrow):
    money = scanrow[0]
    return money[0]

scan_str = np.loadtxt("/home/antojr/stash/datatxt/gokussj4.txt",dtype=str,skiprows=1,usecols=(0,2,4))
scan_flo = np.loadtxt("/home/antojr/stash/datatxt/gokussj4.txt",dtype=float,skiprows=1,usecols=(1,3,5,6))

scanlist = [(scan_flo[i,:],scan_str[i,:]) for i in range(len(scan_str))]
scanlist.sort(key=sorter)

newscan = []
out = open("/home/antojr/stash/datatxt/ssbevegeta.txt","w")
out.write("name // mid-observation time // exposure id // DOY // long date // optical-bench temp // exposure time,probably in milliseconds\n")
for i in range(len(scanlist)):
    nums = scanlist[i][0]   #4 bits, jd doy temp exptime
    strs = scanlist[i][1]   #3 bits, name expid longdate
    strin = f"{strs[0]} {nums[0]} {strs[1]} {int(nums[1])} {strs[2]} {nums[2]} {nums[3]} \n"
    out.write(strin)
out.close()
print("okay we did it")
