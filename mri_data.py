#Antoine
#mri data from fresh

import numpy as np
#import matplotlib.pyplot as plt
#spline, periodicities, lomb, scargle, rfft

if __name__ == '__main__':
    mri_data = np.loadtxt('/home/antojr/hartley2/mri_aperture_photometry.tab',dtype=object, unpack=False)
    
    mri_dates = mri_data[:,1].astype(float)     #days
    mri_doys = mri_data[:,2].astype(int)        #days
    mri_filter = mri_data[:,3].astype(str)
    mri_cometx = mri_data[:,4].astype(float)    #pixels
    mri_comety = mri_data[:,5].astype(float)    #pixels
    #mri_exposuretime = mri_data[:,6].astype(float)
    #mri_framesize = mri_data[:,7].astype(float)
    mri_qualityflag = mri_data[:,10].astype(int)
    #mri_sundist = mri_data[:,11].astype(float) #AU
    #mri_scdist = mri_data[:12].astype(float) #km
    #mrI_phaseangle 13
    #mri_solarelongation 14
    mri_aper = mri_data[:,15:].astype(float)    #W/m2/micron #flux
    #print(mri_aper)
    #print(mri_aper.shape)
    #print(mri_data.shape)
    #print(mri_aper.shape)
    #getting rid of non clear1 filters
    filter_mask =  (  np.logical_and(  mri_filter == 'CLEAR1', mri_qualityflag == 0 )   )
    #print(mri_aper.shape)
    mri_dates = mri_dates[filter_mask]
    mri_aper = mri_aper[filter_mask]
    #print(mri_aper.shape)
    apsizes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, \
        35, 40, 45, 50, 55, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 248]
    #print(mri_aper[:,2],mri_aper[:,3])
    typex = np.dtype([('date','f8'),('0-pix','f8'),('1-pix','f8'),('2-pix','f8'),\
    ('3-pix','f8'),('4-pix','f8'),('5-pix','f8'),('6-pix','f8'),('7-pix','f8'),\
    ('8-pix','f8'),('9-pix','f8'),('10-pix','f8'),('12-pix','f8'),('14-pix','f8'),\
    ('16-pix','f8'),('18-pix','f8'),('20-pix','f8'),('25-pix','f8'),('30-pix','f8'),\
    ('35-pix','f8'),('40-pix','f8'),('45-pix','f8'),('50-pix','f8'),('55-pix','f8'),\
    ('60-pix','f8'),('80-pix','f8'),('100-pix','f8'),('120-pix','f8'),('140-pix','f8'),\
    ('160-pix','f8'),('180-pix','f8'),('200-pix','f8'),('220-pix','f8'),('240-pix','f8'),\
    ('248-pix','f8')])
    
    #print(mri_dates.reshape((-1,1)).shape, mri_aper[4].shape )
    
    daydat = np.concatenate((mri_dates.reshape((-1,1)),mri_aper),axis=1)
    #print(tuple(daydat[0]))
    daydat2 = [tuple(i) for i in daydat]
    mri_aper2 = np.array(daydat2,dtype=typex)
    #print(mri_aper2[''][1:5])
    np.save('results_code/mri_aperturedata_3.npy',mri_aper2)
else:
    pass

