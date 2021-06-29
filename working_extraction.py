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
out=open("vegeta.txt","w")
out.write("name // mid-observation time // exposure id // date // optical-bench temp // exposure time,probably in milliseconds\n")
c = []
for i in range(len(b[:,0])):
    files = b[i,2]
    for j in files:
        if j[22:26] == ".fit":
            lastframe = fits.open(os.path.join(b[i,0],j))
            name = j
            obstime = lastframe[0].header["OBSMIDJD"]
            obsdate = lastframe[0].header["OBSDATE"]
            temp = lastframe[0].header["OPTBENT"]
            exposuretime = lastframe[0].header["INTTIME"]
            exposureid = lastframe[0].header["EXPID"]
            data = lastframe[0].data
            if data.shape == (256,512):
                data = np.array(data)
                c.append(data)
                string = f"{name} {obstime} {exposureid} {obsdate} {temp} {exposuretime}"
                out.write(string+"\n")
            else:
                print("bad shape")
            lastframe.close()
        else:
            #print("what was that!? woah..")
            pass
        break #just first file
    if i%40 == 0:
        print(f"sorted through {i} scans")
out.close()
c = np.array(c,dtype=float)
print(c.shape)
fitte = fits.PrimaryHDU(c)
fitte.writeto("collage_v2.fit")
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
