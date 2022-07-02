#Antoine
#this program creates a numpy structured array with all the data for my comet
#it should have 1321 rows, ordered by time the data were taken or 'julian date'
####################################################################################################################
#gonna play around with structured arrays because
#i think itd be good to store the metadata of each of these scans
#in a single place for easy access
####################################################################################################################
#about to pull the ultimate gamer move
import numpy as np
#load in all the data
data_directory = '/home/antojr/stash/datatxt'
scan_str     = np.loadtxt(data_directory+"/oozaru3.txt",dtype=str,skiprows=1,usecols=(0,2,4))
scan_flo     = np.loadtxt(data_directory+"/oozaru3.txt",dtype=float,skiprows=1,usecols=(1,3,5,6,7,8))
dark_tem     = np.loadtxt(data_directory+"/dark_temp_v2.dat",dtype=float,skiprows=1,usecols=(0,1,2,3,4,5,7))
dark_str     = np.loadtxt(data_directory+"/dark_temp_v2.dat",dtype=str,skiprows=1,usecols=(6))
coords_num   = np.loadtxt(data_directory+"/ir_coords.txt",dtype=float,usecols=(0,2,3))
coords_eid   = np.loadtxt(data_directory+"/ir_coords.txt",dtype=str,usecols=(1))
mri_dat      = np.loadtxt(data_directory+"/mri_interpolated.txt",dtype=float,skiprows=1)
loc_dat      = np.loadtxt(data_directory+"/nucleus_location_v3.txt",dtype=float)
aper         = np.loadtxt(data_directory+"/apertureSizes.txt",dtype=float,skiprows=1)
nsf,dbl,nfr  = np.loadtxt(data_directory+"/nsflip_doubled.txt",dtype=int,skiprows=1,unpack=True,usecols=(1,2,3))
iss,directs  = np.loadtxt(data_directory+'/directories.txt',dtype=str,unpack=True,skiprows=1)
####################################################################################################################
#for each scan there is:
#julian date, smooth temp, dark level, best fit level, exposure time, doy, exposure id, outlier flag,
#filename, long date (skip), ir_coords (and more lol)
####################################################################################################################
### create the dtype array, with the data types of each column in the array
typex = np.dtype([('julian date','f8'),('DOY','i4'),('exposure id','U8'),('temperature','f8'), \
                ('dark level','f8'),('dark best fit','f8'),('x-nucleus','f8'), ('y-nucleus','f8'), \
                ('pixel scale','f8'), ('comet dist','f8'), ('aperture radius','i4'), ('aperture size','i4'), \
                ('mri 3-pixel','f8'),('mri 7-pixel','f8'),('mri 12-pixel','f8'),('mri 20-pixel','f8'), \
                ('exposure time','f8'),('outlier flag','?'),('doubled flag','?'),('nsflip flag','?'), \
                ('number frames','i4'), ('filename','U26'), ('directory path','U42') ])
dats = []                               #list to put all the data together
for i in range(len(dark_tem)):
    dats.append(( dark_tem[i,0], int(dark_tem[i,5]), dark_str[i], dark_tem[i,1], dark_tem[i,2], \
                dark_tem[i,3], loc_dat[i,1], loc_dat[i,2], scan_flo[i,4], scan_flo[i,5], aper[i,2], \
                aper[i,1], mri_dat[i,0], mri_dat[i,1], mri_dat[i,2], mri_dat[i,3], dark_tem[i,4], \
                dark_tem[i,6], dbl[i], nsf[i], nfr[i], scan_str[i,0], directs[i] ))
a = np.array( dats, dtype = typex )     #the array is set

