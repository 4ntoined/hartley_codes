#Antoine
#this one will look at the scans and take inventory
#record important information
from astropy.io import fits
def inven(scandir):
    frame1 = fits.open(scandir)
    hdr = frame1[0].header
    jd = hdr['obsmidjd']
    pxlscl = hdr['pxlscale']
    img_mode = hdr['imgmoden']
    isbinff = img_mode == 'BINFF'
    exp_time = hdr['inttime']
    doy = scandir[36:39]
    expp = scandir[40:50]
    saveit = (doy,expp,jd,exp_time,isbinff,pxlscl, )
    return saveit

print( inven('/alcyone1/antojr/downloading_h2/raw/298_4000015_20/hi10102520_4000015_001.fit') )


