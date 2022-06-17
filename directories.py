import os
import numpy as np
import astropy.io.fits as fits

def sortDires(row):     #key for sorting directories by time data were taken
    cal = fits.open(row+"/cal_001.fit")
    tym = cal[0].header["OBSMIDJD"]
    cal.close()
    return tym

q = []
for paths, dirs,fils, in os.walk("/chiron4/antojr/calibrated_ir/"):
    q.append(paths)
    #print(paths)
q = q[1:]
q.sort(key=sortDires)
#q = np.array(q,dtype=object)

with open("directories.txt","w") as fil:
    fil.write("index // directory of scan time-order :: created with directories.py\n")
    for i in range(len(q)):
        fil.write(f"{i} {q[i]}\n")
    pass

#for i in range(0,10):
    #print(f"{i} {q[i]}")
