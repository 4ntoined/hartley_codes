#Antoine
#this one will look at the scans and take inventory
#record important information
import os
from astropy.io import fits
class inventory:
    def __init__(self):
        return
    def walker(self,topdir):
        p,d,f=[],[],[]
        for a,b,c in os.walk(topdir):
            #print(a)
            p.append(a)
            d.append(b)
            f.append(c)
        self.topdir = topdir
        self.scandirs = p[1:]
        self.direct = d[1:]
        self.scanframes = f[1:]
        self.nscans = len(self.scandirs)
        #print(p)
        return (self.scandirs,self.direct,self.scanframes)

    def filter(self,savedir,savename1='full_list.txt',savename2='filtered_list.txt',savename3='frejected_list.txt'):
        headline = '#index // expid // jd // exposuretime [ms] // frame count'+\
            ' // BINFF? // pxlscl [m/pxl] // dist [km] // temp [K] // path\n'
        #print(savedir)
        with open(savedir+savename1,'x') as out1:
            out1.write(headline)
        with open(savedir+savename2,'x') as out2:
            out2.write(headline)
        with open(savedir+savename3,'x') as out2:
            out2.write(headline)
        check_i = 0
        all_i = 0
        bad_i = 0
        for i in range(self.nscans):
            datline = self.inven(i)
            time_good = datline[2] == 7000.33 or datline[2] == 8000.33 or datline[2] == 12000.33
            size_good = datline[4]
            doy_good = datline[0][:3] != '308'
            frame_good = (datline[3] == 16) or (datline[3] == 17) or \
                (datline[3] == 30) or (datline[3] == 32) or (datline[3] == 38)
            check = time_good and size_good and doy_good and frame_good
            #print(check)
            datstring=''
            for j in datline: datstring+=f'{j} '
            datstring+=f'{self.scandirs[i]}\n'
            datstring1 = f'{all_i} '+datstring
            with open(savedir+savename1,'a') as out1: out1.write(datstring1)
            all_i+=1
            if check:
                #datstring = f'{check_i} '
                #for j in datline: datstring+=f'{j} '
                #datstring+=f'{self.scandirs[i]}\n'
                datstring2 = f'{check_i} '+datstring
                with open(savedir+savename2,'a') as out1:   out1.write(datstring2)
                check_i+=1
            else:
                datstring3 = f'{bad_i} '+datstring
                with open(savedir+savename3,'a') as out2: out2.write(datstring3)
                bad_i+=1
            pass
             
            #datstr = [ for i in  ]
            
        return
    def inven(self,index):
        #walk out the directory
        ##p,d,f = [],[],[]
        #for a,b,c in os.walk(scandir):
        #    p.append(a)
        #    f.append(c)
        #    d.append(b)
        #
        #print( f[0].sort() )
        scanpath = self.scandirs[index]
        f0 = self.scanframes[index]
        #print(scanpath)
        #print('q', f0)
        f0.sort()
        #print('y', f0)
        files = f0
        #print('z', files)
        nframes = len(files)
        #use frame1 for data stuff
        frame1 = fits.open(scanpath+'/'+files[0])
        hdr = frame1[0].header
        jd = hdr['obsmidjd']
        pxlscl = hdr['pxlscale']    #meters/pixel
        dist = hdr['ctrdist']       #kilometers
        exp_time = hdr['inttime']   #milliseconds
        temp = hdr['optbent']       #kelvin
        isbinff = hdr['imgmoden'] == 'BINFF'
        doy = scanpath[36:39]
        expp = scanpath[40:50]
        expid = f'{doy}_{expp}'
        saveit = (expid, jd, exp_time, nframes, isbinff, pxlscl, dist, temp)
        frame1.close()
        #lastframe = fits.open(scandir+'/'+files[-1])
        #lastdata = lastframe[0].data.copy()
        return saveit
def sorter(filename):
    return
#print( inven('/alcyone1/antojr/downloading_h2/raw/298_4000015_20/hi10102520_4000015_001.fit') )
if __name__ == '__main__':
    topdir = '/alcyone1/antojr/downloading_h2/rap/'
    scandir = '/alcyone1/antojr/downloading_h2/raw/298_4000015_20/'
    saving = '/alcyone1/antojr/downloading_h2/rap/'
    #pp,dd,ff = walker(topdir)
    #print(pp[0])
    i1 = inventory()
    i1.walker(topdir)
    i1.filter(saving)
    #for i in range(len(pp)):
    #    print(inven(pp[i])[0])
    #pass
else:
    pass
