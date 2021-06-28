#Antoine Washington
#gonna write a code to go through all my data and get the important stuff
import os
import numpy as np
import astropy.io.fits as fits

def getIt(path):
    #this function will get the interesting info from a fits given its path
    return

#directoryInQuestion = "."
directoryInQuestion = input("directory with the data: ")
ps = []
ds = []
fs = []
for paths, dirs, fils in os.walk(directoryInQuestion):
    ps.append(paths)
    ds.extend(dirs)
    fs.extend(fils)
    break               #only iterates through the top directory, otherwise we'd get all the subdirectories as well
#ps holds the path of the top directory
#ds is the name of every subdirectory in the top (doy)
#fs is the name of every file (no files) in top
a=[]
c=[]
for i in ds:                                                                #will iterate through all the doy directories
    for paths, dirs, fils in os.walk(os.path.join(directoryInQuestion, i)): #will iterate through all subdirectories in doy (exposures)
        a.append([i,dirs,paths])
        break
#each entry of a holds: (0) doy, (1) exposure ids/sub-doy directories, (2)path to doy directory
a = np.array(a,dtype=object)
b = []
out = open("paths.txt","w")
for i in range(len(a[:,2])):    #iterates through all doys
    for j in a[i,1]:            #iterate through each day's scans
        for paths,dirs,fils in os.walk(os.path.join(directoryInQuestion,a[i,2],j)):
            b.append([a[i,2],j,fils,paths])
            break
#each entry holds: (0) path to doy directory (1) exposure id (2) files therein (3) path to exposure id directory
b = np.array(b, dtype=object)
c = []
for i in range(len(b[:,0])):    #each exposure/scan
    filez = b[i,2]
    out.write(f"\n{b[i,3]} // {b[i,1]}\n")
    for j in filez:             #go through all the files
        out.write(f"{j}\n")
        if j[22:26] == ".fit":  #to secure just the fits files
            c.append(j)
    lastone = c[-1]
    fi = fits.open(os.path.join(b[i,3],lastone))
    print(fi[0].header["INTTIME"])
    fi.close()

out.close()
