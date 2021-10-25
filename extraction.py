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
out=open("oozaru.txt","w")
file7 = open("seven_v2.dat","w")   #will record same data as out for each one of the exposures
file8 = open("eight_v2.dat","w")
file12 = open("twleve_v2.dat","w")

for i in (out,file7,file8,file12):
    i.write("name // mid-observation time // exposure id // DOY // date // optical-bench temp // exposure time // pixel scale // distance to comet\n")

seven = []
eight = []
twelve = []
for i in range(len(b[:,0])):
    files = b[i,2]
    if len(files) >= 1: #will exclude scans with no .fit files (they return an empty list and break they code)
        files.sort(key=sorter)                                  #sorts the files in each directory based on number
        lastframe = fits.open(os.path.join(b[i,0],files[-1]))   #grab the last file/frame
        name = files[-1]                                        #col 0
        obstime = lastframe[0].header["OBSMIDJD"]               #col 1
        obsdate = lastframe[0].header["OBSDATE"]                #col 4
        temp = lastframe[0].header["OPTBENT"]                   #col 5
        exposuretime = lastframe[0].header["INTTIME"]           #col 6
        exposureid = b[i,0].split("/")[-1]                      #col 2
        doy = b[i,0].split("/")[-2]                             #col 3
        pxlscl = lastframe[0].header['PXLSCALE']                #col 7
        distcom = lastframe[0].header['CTRDIST']                #col 8
        sting = f"{name} {obstime} {exposureid} {doy} {obsdate} {temp} {exposuretime} {pxlscl} {distcom}\n"
        out.write(sting)                                   #write the data to a file
        data = lastframe[0].data
        if data.shape == (256,512):                             #exludes 2 frames from 2 scans
            if (name[19:22] == "011") or (name[19:22] == "036"):
                print(f"don't think frame {name[19:22]} was the last frame in {b[i,0]}")
            else:
                if abs(exposuretime - 7000.33) < 0.4:
                    seven.append(data)
                    file7.write(sting)
                elif abs(exposuretime - 8000.33) < 0.4:
                    eight.append(data)
                    file8.write(sting)
                elif abs(exposuretime - 12000.33) < 0.4:
                    twelve.append(data)
                    file12.write(sting)
                else:
                    print(f"exptime {exposuretime} ms was not caught in {b[i,0]}")
    else:
        print(f"directory {b[i,0]} had no .fit files")
    if i%40 == 0:
        print(f"examined {i} scans")
out.close()
file7.close()
file8.close()
file12.close()
seven = np.array(seven,dtype=float)
eight = np.array(eight,dtype=float)
twelve = np.array(twelve,dtype=float)
#gonna write up some headers for these fitses

h7 = fits.Header()
h8 = fits.Header()
h12 = fits.Header()

for i in ((h7,"7"),(h8,"8"),(h12,"12")):
    i[0]["comment"] = f"collage of {i[1]}s exposure darks"
    i[0]["axis1"] = "spectral-d"
    i[0]["axis2"] = "scan-d"
    i[0]["axis3"] = "frames"

fit7 = fits.PrimaryHDU(seven,header=h7)
fit8 = fits.PrimaryHDU(eight,header=h8)
fit12 = fits.PrimaryHDU(twelve,header=h12)
#fit7.writeto("sevensies_v3.fit")
#fit8.writeto("eightsies_v3.fit")
#fit12.writeto("twelvesies_v3.fit")
print("okay done for now")

