#Antoine

import numpy as np
from datafunctions import selector
def peak_to_peak():
    return
a = np.load('a_cometmeta.npy')
#
post_peaks_h_1 = []
post_peaks_h_2 = []
post_peaks_h_3 = []
#
post_troug_h_1 = []
post_troug_h_2 = []
post_troug_h_3 = []
#
post_peaks_c_1 = [505.9916684106,508.278491451,510.5972980303,512.8841210706,515.154952341,np.nan]
post_peaks_c_2 = [506.8392321947,509.126055235,511.428870045,513.7156930855,516.018507895,518.321322705]
post_peaks_c_3 = [np.nan,509.717750707,512.0045737475,514.307388557,516.746133408,np.nan]
#
post_troug_c_1 = [506.407454418,508.7262609974,511.0130840377,513.363874156,515.6506971964,518.0014873147]
post_troug_c_2 = [np.nan,509.4298988557, 511.700730127, 514.051520245,516.3863185938, np.nan]
post_troug_c_3 = [507.9746478302, 510.2614708706,512.548293911,514.8511087205,np.nan,np.nan]

peak_1_c = [505.9916684106,506.8392621947,np.nan]
peak_2_c = [508.278491451,509.126055235,509.717750707]
peak_3_c = [510.5972980303,511.428870045,512.0045737475]
peak_4_c = [512.8841210706,513.7156930855,514.307388557]
peak_5_c = [515.154952341,516.018507895,516.746133408]
peak_6_c = [np.nan,518.321322705,np.nan]

trou_1_c = [506.407454418,np.nan,507.9746478302]
trou_2_c = [508.7262609974,509.4298988557,510.2614708706]
trou_3_c = [511.0130840377,511.700730127,512.548293911]
trou_4_c = [513.363874156,514.051520245,514.8511087205]
trou_5_c = [515.6506971964,516.3863185938,np.nan]
trou_6_c = [518.0014873147,np.nan,np.nan]
#
peak_1_h = [506.0236519496,506.8712157337,np.nan]
peak_2_h = [508.31047499,509.158038774,509.749734246]
peak_3_h = [510.6292815693,511.460853584,512.052549056]
peak_4_h = [512.868129301,513.7156930855,514.4673062526]
peak_5_h = [515.20292765,516.018507895,516.85007991]
peak_6_h = [np.nan,518.289339166,np.nan,]

trou_1_h = [506.4554297263,np.nan,507.9906395995]
trou_2_h = [508.7742363056,509.4298988557,510.2934544096]
trou_3_h = [511.093042885,511.780688974,512.56428568]
trou_4_h = [513.3798659253,514.1314790924,514.8671004903]
trou_5_h = [515.7466478134,516.3703268245,np.nan]
trou_6_h = [518.0174790844,np.nan,np.nan]

whole = [  [ [peak_1_h,peak_2_h,peak_3_h,peak_4_h,peak_5_h,peak_6_h] , [trou_1_h,trou_2_h,trou_3_h,trou_4_h,trou_5_c,trou_6_h] ],\
        [ [peak_1_c,peak_2_c,peak_3_c,peak_4_c,peak_5_c,peak_6_c],[trou_1_c,trou_2_c,trou_3_c,trou_4_c,trou_5_c,trou_6_c]  ]]
whole_arr = np.array(whole,dtype=float) #should be 2, 2, 6, 3
whole_arr = whole_arr + 2455000.0
np.save('results_code/peak_times-wild.npy',whole_arr)
print(whole_arr[0,1,1,2])

scans_peaks = np.zeros_like(whole_arr)
for i in (0,1): #h2o and co2
    for j in (0,1): #peaks/trough
        for k in range(6): #6 cycles
            scans_peaks[i,j,k] = [ selector( whole_arr[i,j,k,l] ) for l in range(3) ]
            pass
        pass
    pass
np.save('results_code/peak_indeces.npy',scans_peaks)
#print(scans_peaks)


#print(whole_arr.shape)
#print(trou_2_h[2])
#


peaks1 = [ post_peaks_c_1[i+1]-post_peaks_c_1[i] for i in range(len(post_peaks_c_1)-1) ]
peaks2 = [ post_peaks_c_2[i+1]-post_peaks_c_2[i] for i in range(len(post_peaks_c_2)-1) ]
peaks3 = [ post_peaks_c_3[i+1]-post_peaks_c_3[i] for i in range(len(post_peaks_c_3)-1) ]
peak1to2 = [ post_peaks_c_2[i] - post_peaks_c_1[i] for i in range(len(post_peaks_c_1))  ]
peak2to3 = [ post_peaks_c_3[i] - post_peaks_c_2[i] for i in range(len(post_peaks_c_2))  ]
peak1to3 = [ post_peaks_c_3[i] - post_peaks_c_1[i] for i in range(len(post_peaks_c_2))  ]

print(np.array(peak1to2)*24.)
print(np.array(peak2to3)*24.)
#print(peaks3)

pass
