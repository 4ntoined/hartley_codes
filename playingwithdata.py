#Antoine still
#gonna play around with structured arrays because
#i think itd be good to store the metadata of each of these scans
#in a single place for easy access
import numpy as np
def getScanInfo(scan_index,printout=False):
    global a
    dat = a[scan_index]
    lbl = a.dtype.names
    print("index : " + str(scan_index))
    for i in range(len(lbl)):
        print(lbl[i] + " : " + f"{dat[i]}")
    return
def jd2index(julian, runinfo= False ):
    #julian should be precise down to 0.001 for my data
    global a
    times = a['julian date'].copy()
    finder = np.abs(times - julian)
    closest = np.min(finder)
    scan_i = np.squeeze( np.argwhere(finder <= closest))
    #print(scan_i)
    if runinfo:
        getScanInfo(scan_i)
    return scan_i
def expid2index(doi,xps,runinfo=False):
    #exposure id given as string
    #doy doesnt matter
    global a
    days  = a['DOY'].astype(str)
    exss = a['exposure id'].copy()
    rdays = days == str(doi)
    rexps = exss == str(xps)
    rboth = np.logical_and(rdays,rexps)
    scan_i = np.squeeze( np.argwhere(rboth)  )
    if scan_i.size < 1:
        raise ValueError('No match found.')
    if runinfo:
        getScanInfo(scan_i)
    return scan_i
#id like to have one do a prompt
#and another take any input?
def selector():
    #this will return the scan index and directory as string
    scanno = input("Which scan:  ")
    ### i was checking for length first but i should see if this a
    ### a number or a directory path
    #so
    try:
        if int(scanno) <= 1320 and int(scanno) >= 0:                        #expecting this to break
            #then its an INDEX
            #do the math
            scan_i = int(scanno)
            direc = '/chiron4/antojr/calibrated_ir/' + str(a['DOY'][scan_i]) + a['exposure id'][scan_i]
            return (scan_i, direc)
        elif float(scanno) >= 2455494.0 and float(scanno) <= 2455519.0:     #this will break?
            #then its a JULIAN DATE
            scan_i = 0
            direc = ''
            return (scan_i, direc)
        else:
            #then its some random number
            return (-9999, 'bunked')
    except ValueError:
        #then it broke the int/float functions, prob non-numerical input
        #so we'll keep going
        print("...")
    except:
        #i don't know what went wrong, return error values
        print("Error unexpected. Cool!")
        return (-9999, 'bunked')
    #uhhh
    #then we check for directories, and exp,doy combos
    #'307 4200024'
    lsc = len(scanno)
    if lsc >= len( '/chiron4/antojr/calibrated_ir/307.4200012' ):
        #then this is DIRECTORY
        # !!! check for nonsense strings !!! checked !!!
        #/chiron4/antojr/calibrated_ir/ is 30 long 307.4200021_ is +12 = 42
        #print("directory")
        try:
            direc = scanno
            doi,exp = scanno[30:].split(".")                #expecting her to break the try block
            scan_i = expid2index(doi,exp,runinfo=False)     #if above succeeds this is one next to break
            return (scan_i ,direc)
        except ValueError:
            print("Bonked directory path? :(")
            return (-9999, 'bonked')
        except:
            print('Error unexpected. Cool!')
            return (-9999, 'bonked')
    else:
        #then its an EXPOSURE ID
        try:
            #might be nonsense and not 
            doi, exp = scanno.split()
            scan_i = expid2index(doi,exp,runinfo=False)     #expecting this to break
            direc = '/chiron4/antojr/calibrated_ir/' + str(a['DOY'][scan_i]) + a['exposure id'][scan_i]
            return (scan_i ,direc)
        except ValueError:
            print("BONKED FORMAT...")
            print("try the julian date or index (all digits)...")
            print("or exposure ID like: '307 4200021' or directory path.")
            return (-9999, 'bonked')
        except:
            print('Error unexpected. Cool!')
            print("try the julian date or index (all digits)...")
            print("or exposure ID like: '307 4200021' or directory path.")
            return (-9999, 'bonked')
    pass
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
