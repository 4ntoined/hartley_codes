#Antoine still
#gonna play around with structured arrays because
#i think itd be good to store the metadata of each of these scans
#in a single place for easy access
import numpy as np

scan_str = np.loadtxt("/home/antojr/stash/datatxt/oozaru3.txt",dtype=str,skiprows=1,usecols=(0,2,4))
scan_flo = np.loadtxt("/home/antojr/stash/datatxt/oozaru3.txt",dtype=float,skiprows=1,usecols=(1,3,5,6,7,8))
dark_tem = np.loadtxt("/home/antojr/stash/datatxt/dark_temp_v2.dat",dtype=float,skiprows=1,usecols=(0,1,2,3,4,5,7))
dark_str = np.loadtxt("/home/antojr/stash/datatxt/dark_temp_v2.dat",dtype=str,skiprows=1,usecols=(6))
coords_num = np.loadtxt("/home/antojr/stash/datatxt/ir_coords.txt",dtype=float,usecols=(0,2,3))
coords_eid = np.loadtxt("/home/antojr/stash/datatxt/ir_coords.txt",dtype=str,usecols=(1))
mri_dat = np.loadtxt("/home/antojr/stash/datatxt/mri_interpolated.txt",dtype=float,skiprows=1)
loc_dat = np.loadtxt("/home/antojr/stash/datatxt/nucleus_location_v3.txt",dtype=float)
aper = np.loadtxt("/home/antojr/stash/datatxt/apertureSizes.txt",dtype=float,skiprows=1)
nsf, dbl, nfr = np.loadtxt("/home/antojr/stash/datatxt/nsflip_doubled.txt",dtype=int,skiprows=1,unpack=True,usecols=(1,2,3))
#for each scan there is:
#julian date, smooth temp, dark level, best fit level, exposure time, doy, exposure id, outlier flag,
#filename, long date (skip), ir_coords
typex = np.dtype([('julian date','f8'),('DOY','i4'),('exposure id','U8'),('temperature','f8'), \
                ('dark level','f8'),('dark best fit','f8'),('x-nucleus','f8'), ('y-nucleus','f8'), \
                ('pixel scale','f8'), ('comet dist','f8'), ('aperture radius','i4'), ('aperture size','i4'), \
                ('mri 3-pixel','f8'),('mri 7-pixel','f8'),('mri 12-pixel','f8'),('mri 20-pixel','f8'), \
                ('exposure time','f8'),('outlier flag','?'),('doubled flag','?'),('nsflip flag','?'), \
                ('number frames','i4'), ('filename','U26')])
dats = []
for i in range(len(dark_tem)):
    dats.append(( dark_tem[i,0] , int(dark_tem[i,5]), dark_str[i], dark_tem[i,1], dark_tem[i,2], \
                dark_tem[i,3] , loc_dat[i,1], loc_dat[i,2], scan_flo[i,4], scan_flo[i,5], aper[i,2], \
                aper[i,1], mri_dat[i,0], mri_dat[i,1],mri_dat[i,2],mri_dat[i,3], dark_tem[i,4] , \
                dark_tem[i,6], dbl[i], nsf[i], nfr[i], scan_str[i,0]))
    pass
a = np.array( dats, dtype = typex )
#print( expid2index('314','4200021_',runinfo=True) )
#getScanInfo(160)
#print(jd2index(2455500.9267,runinfo=1))
# we will go through every row
"""
for i in range(len(coords_num)):
    doy, xn, yn, = coords_num[i]
    ein = coords_eid[i]
    #will go over every row in the structured array for matching
    matched = False
    for j in range(len(a)):
        doy_a = a['DOY'][j]
        exp_a = a['exposure id'][j]
        if (doy_a==doy) and (exp_a==ein): #day of year and exposure ids match
            #will need to fill in xn and yn
            a['x-nucleus'][j] = xn
            a['y-nucleus'][j] = yn
            #okay it's over
            matched = True
        pass
    if matched == False:
        print(f"no match found for {doy} {ein}")
    pass

#about to pull the ultimate gamer move

outt = open("nucleus_location.txt","w")
for i in range(len(a)):
    outt.write(f"{a['julian date'][i]} {a['x-nucleus'][i]} {a['y-nucleus'][i]}\n")
    pass
outt.close()
"""
#print(a['y-nucleus'][215:230])
