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
            matched = False
            coordo = ( self.co_xxx[i], self.co_yyy[i])
            tdoy = self.co_doy[i]
            #we will actually only look for a match where we know the days already match..duh
            searcc = np.squeeze( np.argwhere( self.me_doy == tdoy ) )
            #print(searcc)
            #check for duplicate scans within searcc
            star1 = [ self.me_exp[k][4:12] for k in searcc]

            for j in searcc:
                #we know days already match? just check for expid
                newid = self.me_exp[j]
                oldid = self.co_exp[i]
                matt = newid[:7] #cuts hours from new ids
                if matt == oldid:
                    #it's a match to a non-underscored scan
                    # do further checks for
                    matched=True
                    xy[j] = coordo
                    #xy[j] = [ coordo[0], coordo[1] ]
                elif matt==oldid[:7]:
                    #it's a match to the underscore
                    matched=True
                    xy[j] = [ coordo[0], coordo[1] ]
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
                pass
            pass
        #done with all the coordinates, finish up
        if savehere:    np.save(savehere,xy)
        return xy

        def corrections(self):
            return

def basic(x):
    #fgh: ghi
    xx = x[:3]
    return xx

if __name__ == '__main__':
    #
    coords_path = '/home/antojr/stash/datatxt/ir_coords.txt'
    meta_path = '/home/antojr/stash/datatxt/filtered_list.txt'
    saveloc = '/home/antojr/codespace/wild_nukes.npy'
    c1 = code(meta_path,coords_path)
    c1.matcher(savehere=saveloc)
    pass
else:
    pass
