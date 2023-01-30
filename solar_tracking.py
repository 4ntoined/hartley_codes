#Antoine

import numpy as np
#from astropy.io import fits
import matplotlib.pyplot as plt

a = np.load('a_cometmeta.npy')
if __name__ == '__main__':
    solar_txt = np.loadtxt('/home/antojr/codespace/results_code/shape_subsolar_lonlat.txt',delimiter=',',skiprows=1,dtype=float)
    obser_txt = np.loadtxt('/home/antojr/codespace/results_code/shape_subobser_lonlat.txt',delimiter=',',skiprows=1,dtype=float)
    gass = np.load('results_code/gascurves_x5-correct.npy')
    h2o, co2, dust, flags = gass['h2o'],gass['co2'], 4, 4
    plt.plot(a['julian date'],solar_txt[:,1],label='solar latitude')
    plt.plot(a['julian date'],solar_txt[:,0],label='solar longitude')
    plt.scatter(a['julian date'], co2/np.mean(co2)*100., s=2.)
    plt.legend(loc='best')
    
    plt.show(block=False)
    #plt.close()
    
    
    #plt.plot(a['julian date'],obser_txt[:,1],label='DI latitude')
    #plt.plot(a['julian date'],obser_txt[:,0],label='DI longitude')
    #plt.legend(loc='best')
    #plt.show(block=False)
    gp = input('enter to win')
else:
    pass
