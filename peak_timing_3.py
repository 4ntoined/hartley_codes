#Antoine
#taking the results of derivatives to find extrema

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #time, mritime, c1, h1, m1, c2, h2, m2
    data_dir_2 = '/home/antojr/codespace/results_code/derivative_analysis/'
    derivs = []
    derivv = ('derivs_gastime.npy','derivs_mritime.npy','derivs_curve_h1.npy','derivs_curve_c1.npy', \
        'derivs_curve_m1.npy','derivs_curve_h2.npy','derivs_curve_c2.npy','derivs_curve_m2.npy')
    for i in range( 8 ): derivs.append( np.load(data_dir_2 + derivv[i]) )
    dtime, dmtime, dh1, dc1, dm1, dh2, dc2, dm2 = derivs
    #derivative zeros
    dzeros = []
    dzerov = ('derivs_index_h1.npy','derivs_index_c1.npy','derivs_index_m1.npy', \
        'derivs_index_h2.npy','derivs_index_c2.npy','derivs_index_m2.npy')
    for i in range(len(dzerov)): dzeros.append( np.load(data_dir_2 + dzerov[i]) )
    dih1, dic1, dim1, dih2, dic2, dim2 = dzeros
    #all this mess going into a txt
    #organize by h2o1 co21 mri1, h2o2, co22, mri2
    savehere='results_code/'
    header='jd of zero crossings in first and second derivatives in h2o co2 and mri lightcurve, peak_timing_3.py\n'
    with open(savehere+'timing_extrema.txt','w') as fil:
        fil.write(header)
        #h2o 1
        fil.write('#H2O, first\n')
        for i in range(len(dih1)):
            fil.write(f"{ dtime[ dih1[ i ] ]  }\n")
        #co21
        fil.write('#CO2, first\n')
        for i in range(len(dic1)):
            fil.write(f"{ dtime[ dic1[ i ] ]  }\n")
        #mri 1
        fil.write('#MRI, first\n')
        for i in range(len(dim1)):
            fil.write(f"{ dmtime[ dim1[ i ] ]  }\n")
        #h2o 2
        fil.write('#H2O, second\n')
        for i in range(len(dih2)):
            fil.write(f"{ dtime[ dih2[ i ] ]  }\n")
        #co2 2 
        fil.write('#CO2, second\n')
        for i in range(len(dic2)):
            fil.write(f"{ dtime[ dic2[ i ] ]  }\n")
        #mri 2
        fil.write('#MRI, second\n')
        for i in range(len(dim2)):
            fil.write(f"{ dmtime[ dim2[ i ] ]  }\n")
        pass
    pass


