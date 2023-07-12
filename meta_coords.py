#Antoine
#this one should do my nucleus locating things for h2

import numpy as np

class code:
    def __init__(self,metapath,coordspath):
        #
        meta = np.loadtxt(metapath,skiprows=1,dtype=object)
        coords = np.loadtxt(coordspath,dtype=object)
        self.num = meta.shape[0]
        self.cnum = coords.shape[0]
        self.co_doy = coords[:,0].astype(int)
        self.co_exp = coords[:,1].astype(str)
        self.co_xxx = coords[:,2].astype(float)
        self.co_yyy = coords[:,3].astype(float)
        #
        me_expid = meta[:,1].astype(str)
        me_doy = []
        me_exp = []
        for i in me_expid:
            me_doy.append( i[:3] )
            me_exp.append( i[4:] )
        self.me_doy = np.array(me_doy,dtype=int)
        self.me_exp = np.array(me_exp,dtype=str)
        self.framecounts = meta[:,4].astype(int)
        #me_doy = [ i[:3]   for i in me_expid ]
        #me_exp = [ i[] fo ]
        #print(me_doy,me_exp)
        #### 
        return
    def matcher(self,savehere=''):
        #def: efg
        xy = np.zeros((self.num,2),dtype=float  )
        for i in range(self.cnum):
            #iterating over the coordinates
            #print('coord row start', i)
            matched = False
            coordo = ( self.co_xxx[i], self.co_yyy[i])
            tdoy = self.co_doy[i]
            oldid = self.co_exp[i]
            #we will actually only look for a match where we know the days already match..duh
            searcc = np.squeeze( np.argwhere( self.me_doy == tdoy ) )
            searci = range(len(searcc))
            #print(searcc)
            #check for duplicate scans within searcc
            #star1 = [ self.me_exp[k][:7] for k in range(self.num)] #for all scans
            star1 = [ self.me_exp[k][:7] for k in searcc] #for all scans
            #star2 = [ star1[i] for i in searcc ]
            star3 = [ np.argwhere( np.array(star1,dtype=str) == k ) for k in star1 ]
            # for each element in star1, the exposure ids that match the doy, we'll see if
            # it has a twin somewhere in the set
            #star2 = [ len( np.argwhere( np.array(star1,dtype=str) == k )) > 1 for k in star1 ]
            #star3 = [ np.argwhere( np.array(star1,dtype=str) == k ) for k in star1]
            #print(searcc)
            #print(star1)
            #print(star3)
            for j in searci:
                #we know days already match? just check for expid
                newid = self.me_exp[ searcc[ j ]]
                matt = newid[:7] #cuts hours from new ids
                labl = newid[8:]
                #print(j)
                #print(star3[j].shape)
                dupes = star3[j]
                #print(dupes.shape)
                #print(type(dupes))
                #ndupes1  = type(dupes) == int
                if dupes.shape[0] == 1:   ndupes = 1
                else:                   ndupes = len(dupes)
                #this exposure id has a duplicate
                #print(dupes)
                if ndupes > 1:
                    outt = list(dupes)
                    #for i in outt: print(self.)
                    outt.remove(j)
                    outt = outt[0]
                    #print(outt)
                    #labl1 = self.me_exp[dupes[0]][8:]
                    #labl2 = self.me_exp[dupes[1]][8:]
                    #print(self.me_exp[outt[0]])
                    other_label = self.me_exp[searcc[outt[0]]][8:]
                    #print(other_label)
                    #print(labl,other_label)
                    duper = int(other_label) < int(labl)
                    #print(duper)
                    if duper: matt = matt + '_'
                #print(oldid,newid,matt)
                #print(matt)
                if matt == oldid:
                    #it's a match to a non-underscored scan
                    # do further checks for
                    matched=True
                    xy[searcc[j]] = coordo
                    #xy[j] = [ coordo[0], coordo[1] ]
                #elif matt==oldid[:7]:
                #    #it's a match to the underscore
                #    matched=True
                #    xy[j] = [ coordo[0], coordo[1] ]
                else:
                    #no match here
                    pass
                pass
            #
            if matched:
                #what to do/say/record when the coord was matched
                pass
            else:
                #and not matched
                print(f'no match: {tdoy}.{self.co_exp[i]}')
                #print(oldid)
                pass
            pass
        #done with all the coordinates, finish up
        if savehere:    np.save(savehere,xy)
        self.xycoords = xy
        return xy

    def corrections(self,savehere=''):
        #correcting y by doubling and flipping
        #xy_correct = np.zeros((self.num,2),dtype=float)
        zeers = self.xycoords[:,0] == 0.0
        new_y = [ self.framecounts[i] - self.xycoords[i,1] - 1. for i in range(self.num) ]
        for i in range(self.num):
            doy = self.me_doy[i]
            fc = self.framecounts[i]
            if ((doy >= 298) and (doy <= 300)) or ((doy >= 309) and (doy <= 320)): #doubling
                new_y[i] = fc * 2.- self.xycoords[i,1] - 1.
            pass
        self.xycoords[:,1] = new_y
        self.xycoords[zeers] = [0.,0.]
        if savehere: np.save(savehere,self.xycoords)
        return self.xycoords.copy()
def basic(x):
    #fgh: ghi
    xx = x[:3]
    return xx

if __name__ == '__main__':
    #
    coords_path = '/home/antojr/stash/datatxt/ir_coords.txt'
    meta_path = '/home/antojr/stash/datatxt/filtered_list.txt'
    saveloc = '/home/antojr/codespace/bb_nukes.npy'
    #saveloc = '/home/antojr/codespace/wild_nukes.npy'
    c1 = code(meta_path,coords_path)
    cort = c1.matcher()
    #print(cort)
    curt = c1.corrections(saveloc)
    #print(curt)
    pass
else:
    pass
