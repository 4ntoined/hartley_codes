#Antoine
#going to see about picking out the peaks in the periodogrms

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

a=np.load('a_cometmeta.npy')
if __name__=='__main__':
    pgrams = np.load('/home/antojr/codespace/results_code/pgrams_gas.npy')
    
    x_period, hh1, cc1, hh2, cc2 = pgrams['period'],pgrams['pre h'],pgrams['pre c'],pgrams['pos h'],pgrams['pos c']
    go1=[]
    pgramz = (hh1, cc1,hh2, cc2)
    for i in pgramz: go1.append( signal.argrelextrema(i, np.greater, order=1)[0] )
    h1maxi, c1maxi, h2maxi, c2maxi = go1
    #print(np.sum(cc2[c2maxi]))
    #for i in range(len(c2maxi)): print( x_period[c2maxi[i]], cc2[ c2maxi[i] ]  )
    #go2 = []
    go3 = []
    maxis = (h1maxi,c1maxi,h2maxi,c2maxi)
    for i in range(4): #over the four/six curves
        go2 = []
        usemax = maxis[i]
        for j in range(len( usemax )): #for each max identified
            go2.append( ( x_period[ usemax[j] ], pgramz[i][ usemax[j] ] ) )
            #go2 = ( x_period[   maxis[i][j]   ],  pgramz[i][j]  )  
        go3.append(np.array(go2, dtype= np.dtype([('period','f8'),('signal','f8') ] )  ))
    h1set, c1set, h2set, c2set = go3[0],go3[1],go3[2],go3[3]
    #print( go3[0]['period'],'\n\n',go3[1] )
    #print()
    #print( go3[2],'\n\n',go3[3] )
    #plotting so i dont go crazy
    sanity_plot = False
    if sanity_plot:
        fig,ax = plt.subplots()
        ax.plot( x_period, cc2)
        ax.vlines( x_period[ c2maxi ], ymin=-0.1,ymax=1.2 )
        plt.show()
    #print(h1set[0:2])
    # lets do a 5% signal cutoff
    cutoff5 = []
    for i in (h1set, c1set, h2set, c2set):
        strong_mask = i['signal'] >= 0.05 
        cutoff5.append( i[strong_mask] )
    h1best, c1best, h2best, c2best = cutoff5
    #print(h1set, '\n\n', h1best)
    #writing the results to a txt file
    savetxt=True
    savedir='/home/antojr/codespace/results_code/'
    savename='lomb_periods_gas.txt'
    headertxt = '#strong signals and period in gascurves_x5, made with periodgram_analysis.py'
    if savetxt:
        with open(savedir + savename,'w') as fil:
            fil.write(headertxt+'\n')
            fil.write('#pre-encounter\n#H2O\n')
            for i in range(len(h1best)):
                fil.write(f"{h1best['period'][i]}, {h1best['signal'][i]}\n")
            fil.write('#CO2\n')
            for i in range(len(c1best)):
                fil.write(f"{c1best['period'][i]}, {c1best['signal'][i]}\n")
            fil.write('#post-encounter\n#H2O\n')
            for i in range(len(h2best)):
                fil.write(f"{h2best['period'][i]}, {h2best['signal'][i]}\n")
            fil.write('#CO2\n')
            for i in range(len(c2best)):
                fil.write(f"{c2best['period'][i]}, {c2best['signal'][i]}\n")
            pass
        pass
else:
    pass

