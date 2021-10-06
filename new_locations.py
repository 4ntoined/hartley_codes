#Antoine
#Im gonna fix the ir coordinates by subtracting the y value
#from whatever the number of frames (height of the image (max y)) is
#will pull that info from the filenames which thank goodness i've retained
#in the mega array
#exhausted honestly there's always something to tweak

import numpy as np
from playingwithdata import a

jd, xs, ys = np.loadtxt("/home/antojr/stash/datatxt/nucleus_location.txt",dtype=float,unpack=True)

ynew = [ float(a['filename'][i][19:22]) - ys[i] for i in range(len(ys)) ]

outt = open("nucleus_locations_v2.txt","w")
for i in range(len(ys)):
    if (ys[i] - -99. < 0.1) or (ynew[i] < 0.):
        outt.write(f"{jd[i]} -99 -99.\n")
    else:
        outt.write(f"{jd[i]} {xs[i]} {ynew[i]}\n")
    pass
outt.close()