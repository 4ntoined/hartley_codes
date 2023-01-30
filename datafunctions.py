#Antoine
#companion to playingwithdat, prob gonna rename to cometdata
#this one is gonna define some basic functions for accessing the mega array from cometmeta
####################################################################################################################
import numpy as np #love her
from astropy.io import fits
#from cometmeta import a
def getScanInfo(scan_index):
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
    if runinfo:     getScanInfo(scan_i)
    return int(scan_i)
def expid2index(doi,xps,runinfo=False):
    #exposure id given either as string or integer
    #doy given however
    global a
    days  = a['DOY'].astype(str)
    exss = a['exposure id'].copy()
    rdays = days == str(doi)
    rexps = exss == str(xps)
    rboth = np.logical_and(rdays,rexps)
    scan_i = np.squeeze( np.argwhere(rboth)  )
    if scan_i.size < 1:
        raise ValueError('No match found.')
    elif scan_i.size>1:
        raise ValueError('More than one match???')
    if runinfo:     getScanInfo(scan_i)
    return int(scan_i)
#id like to have one do a prompt
#and another take any input?
def selector(scanno,runinfo=False):
    #this will return the scan index and directory as string
    #scanno = input("Which scan:  ")
    #print(int(scanno))
    ### i was checking for length first but i should see if this a
    ### a number or a directory path
    #so
    #if np.isnan(scanno): 
    #    print('Entry was Nan')
    #    return -9999
    try:
        try: #looking out for nans
            if np.isnan(scanno): 
                print('Entry was Nan')
                return -9999
        except TypeError:   #input was a string
            pass            #continue with the rest
        except:
            print('Unexpected Error')
            return -9999
        else: #no nans, try all the number stuff
            if int(float(scanno)) <= 1320 and int(float(scanno)) >= 0:                        #expecting this to break
                #then its an INDEX
                scan_i = int(scanno)
                if runinfo: getScanInfo(scan_i)
                return scan_i
            elif float(scanno) >= 2455494.0 and float(scanno) <= 2455519.0:     #this will break?
                #then its a JULIAN DATE
                scan_i = jd2index(float(scanno),runinfo=runinfo)
                return scan_i
            else:
                #then its some random number
                selector_tutorial()
                return -9999
    except ValueError:
        #then it broke the int/float functions, prob non-numerical input
        pass
#    except TypeError:
#        #probably a nan
#        return
    except:
        #i don't know what went wrong, return error values
        print("Error unexpected. Cool!")
        return -9999
    #then we check for directories, and exp,doy combos
    lsc = len(scanno)
    if lsc >= len( '/chiron4/antojr/calibrated_ir/307.4200012' ):
        #then this is DIRECTORY
        #/chiron4/antojr/calibrated_ir/ is 30 long 307.4200021_ is +12 = 42
        try:
            doi,exp = scanno[30:].split(".")                #expecting her to break the try block
            scan_i = expid2index(doi,exp,runinfo=runinfo)   #if above succeeds this is one next to break
            return scan_i
        except ValueError:
            print("Bonked directory path? :(")
            selector_tutorial()
            return -9999
        except:
            print('Error unexpected. Cool!')
            return -9999
    else:
        #then its an EXPOSURE ID
        try:
            doi, exp = scanno.split()
            scan_i = expid2index(doi,exp,runinfo=runinfo)   #expecting this to break
            return scan_i
        except ValueError:
            print("BONKED FORMAT...")
            selector_tutorial()
            return -9999
        except:
            print('Error unexpected. Cool!')
            selector_tutorial()
            return -9999
    pass
#first time was so fun im gonna do it again
def selector_prompt(runinfo=False, default='2455504.510'):
    #selector with prompt
    given = input("Which scan: ") or default
    return selector(given,runinfo=runinfo)
def unloadCube(scan_index, cubename='', wavename=''):
    global a
    cubo = fits.open( a['directory path'][scan_index] + '/' + cubename )
    dato = cubo[0].data
    dath = cubo[0].header
    cubo.close()
    if wavename: #so that we only unload if a wavename is given
        cubw = fits.open( a['directory path'][scan_index] + '/' + wavename )
        wavo = cubw[0].data
        cubw.close()
        return (dato, wavo, dath)
    else:
        return (dato, dath) 
def selector_tutorial():
    print("Try the Julian Date:         2455509.525")
    print("Or the index of the scan:    0-1320")
    print("Or DOY and Exposure ID like: '307 4200021'")
    print("Or the directory path:       /chiron4/ant...")
    return
a = np.load('a_cometmeta.npy')
pass

