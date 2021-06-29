#Antoine Washington
#gonna write a code to go through all my data and get the important stuff
import os
import numpy as np
import astropy.io.fits as fits

def sorter(filename):
    return filename[19:22]

#directoryInQuestion = "."
directoryInQuestion = input("directory with the data: ") or "/chiron5/Sandbox/holt/Hartley2/ir/raw"
#getting all the directories and subdirectories
allOfIt = []
for paths, dirs, fils in os.walk(directoryInQuestion):
    allOfIt.append([paths,dirs,fils])
a = np.array(allOfIt,dtype=object)
b = []
#getting just the exposure subdirectories
for i in range(len(a[:,0])):
    if len(a[i,0]) >= 49:   #should (SHOULD) pick out the directories that are scan directories not doy directories
        b.append(a[i,:])
b = np.array(b,dtype=object)
#keeping just the fits files
for i in range(len(b[:,0])):    #through all the scan subdirectories
    files = b[i,2]              #look at the files therein
    c=[]
    for j in files:             #iterate through files
        if j[22:26] == ".fit":  #when there's a .fit
            c.append(j)         #save it to c
        else:
            pass
    b[i,2] = c                  #replace files list with just .fit filenames
#b should have all the .fits from all the scans
out=open("piccolo.txt","w")
out.write("name // mid-observation time // exposure id // date // \
            optical-bench temp // exposure time,probably in milliseconds\n")
#d=[]
seven = []
eight = []
twelve = []
for i in range(len(b[:,0])):
    files = b[i,2]
    if len(files) >= 1: #will exclude scans with no fits files (they return an empty list and break they code)
        files.sort(key=sorter)
        lastframe = fits.open(os.path.join(b[i,0],files[-1]))
        name = files[-1]
        obstime = lastframe[0].header["OBSMIDJD"]
        obsdate = lastframe[0].header["OBSDATE"]
        temp = lastframe[0].header["OPTBENT"]
        exposuretime = lastframe[0].header["INTTIME"]
        #exposureid = lastframe[0].header["EXPID"]
        exposureid = b[i,0].split("/")[-1]
        sting = f"{name} {obstime} {exposureid} {obsdate} {temp} {exposuretime}"
        out.write(sting+"\n")
        data = lastframe[0].data
        if data.shape == (256,512):
            if abs(exposuretime - 7000.33) < 0.4:
                seven.append(data)
            elif abs(exposuretime - 8000.33) < 0.4:
                eight.append(data)
            elif abs(exposuretime - 12000.33) < 0.4:
                twelve.append(data)
            else:
                print(f"exptime {exposuretime} ms was not caught in {b[i,0]}")
    else:
        print(f"directory {b[i,0]} had no .fit files")
    if i%40 == 0:
        print(f"examined {i} scans")
out.close()
seven = np.array(seven,dtype=float)
eight = np.array(eight,dtype=float)
twelve = np.array(twelve,dtype=float)
fit7 = fits.PrimaryHDU(seven)
fit8 = fits.PrimaryHDU(eight)
fit12 = fits.PrimaryHDU(twelve)
fit7.writeto("sevensies.fit")
fit8.writeto("eightsies.fit")
fit12.writeto("twelvesies.fit")
print("okay done for now")

"""
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
"""
