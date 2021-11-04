#Antoine
#this code will organize my list of scan (last frames) information

import numpy as np

def sorter(scanrow):
    money = scanrow[0]
    return money[0]

scan_str = np.loadtxt("/home/antojr/stash/datatxt/oozaru2.txt",dtype=str,skiprows=1,usecols=(0,2,4))
scan_flo = np.loadtxt("/home/antojr/stash/datatxt/oozaru2.txt",dtype=float,skiprows=1,usecols=(1,3,5,6,7,8))

scanlist = [(scan_flo[i,:],scan_str[i,:]) for i in range(len(scan_str))]
scanlist.sort(key=sorter)

newscan = []
out = open("/home/antojr/stash/datatxt/oozaru3.txt","w")
out.write("name // mid-observation time // exposure id // DOY // long date // optical-bench temp // exposure time // pixel scale // distance to comet\n")
for i in range(len(scanlist)):
    nums = scanlist[i][0]   #6 bits, jd doy temp exptime pixel_scale(km/pix) dist to comet
    strs = scanlist[i][1]   #3 bits, name expid longdate
    strin = f"{strs[0]} {nums[0]} {strs[1]} {int(nums[1])} {strs[2]} {nums[2]} {nums[3]} {nums[4]} {nums[5]}\n"
    out.write(strin)
out.close()
print("okay we did it")
