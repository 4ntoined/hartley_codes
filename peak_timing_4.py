#Antoine

import numpy as np
from datafunctions import selector
def peak_to_peak():
    return
a = np.load('a_cometmeta.npy')
# PRE 

pp_1_h = [2455499.9787630737, 2455500.570458546, 2455501.465997638 ]
pp_2_h = [2455502.265586114, 2455502.889265125, np.nan ]
tt_1_h = [2455500.330582003, 2455501.114178709, 2455501.8657918763 ]
tt_2_h = [2455502.553437965, np.nan, np.nan ]

pp_1_c = [2455499.9467795347,2455500.554466776,2455501.40203056 ]
pp_2_c = [2455502.2495943443,2455502.8412898164, np.nan ]
tt_1_c = [2455500.2506231554, 2455501.0662034005, 2455501.8338083373 ]
tt_2_c = [2455502.5374461957, np.nan, np.nan ]

pp_1_m = [2455501.469197977, 2455502.3035797765, 2455502.903789027]
pp_2_m = [2455503.724529708,np.nan,np.nan]
tt_1_m = [2455501.9716458726, 2455502.5877697626,2455503.388048764]
tt_2_m = [np.nan,np.nan,np.nan]
#

wholo = [  [ [pp_1_h,pp_2_h] , [tt_1_h,tt_2_h] ],\
        [ [pp_1_c,pp_2_c],[tt_1_c,tt_2_c]  ], \
        [ [pp_1_m,pp_2_m],[tt_1_m,tt_2_m]  ]]
wholo_arr = np.array(wholo,dtype=float) #should be 3, 2, 2, 3 #old = 2, 2, 2, 3
#wholo_arr = whole_arr + 2455000.0
np.save('results_code/derivative_analysis/extrema_pre_times-wild.npy',wholo_arr)
print(wholo_arr[:,1,1,2])
#
scans_peako = np.zeros_like(wholo_arr)
for i in (0,1, 2): #h2o and co2 and mri
    for j in (0,1): #peaks/trough
        for k in range(2): #6 cycles
            scans_peako[i,j,k] = [ selector( wholo_arr[i,j,k,l] ) for l in range(3) ]
            pass
        pass
    pass
np.save('results_code/derivative_analysis/extrema_pre_scans-wild.npy',scans_peako)
print(scans_peako[:,1,1,2])
#
peak_1_c = [505.9916684106,506.8392621947,np.nan]
peak_2_c = [508.278491451,509.126055235,509.717750707]
peak_3_c = [510.5972980303,511.428870045,512.0045737475]
peak_4_c = [512.868129301,513.7156930855,514.307388557]
peak_5_c = [515.138960572,516.018507895,516.83408814]
peak_6_c = [np.nan,518.321322705,np.nan]

trou_1_c = [506.407454418,np.nan,507.9746478302]
trou_2_c = [508.7262609974,509.4298988557,510.2614708706]
trou_3_c = [511.0130840377,511.700730127,512.532302141]
trou_4_c = [513.363874156,514.051520245,514.8671004903]
trou_5_c = [515.6506971964,516.3863185938,np.nan]
trou_6_c = [518.0014873147,np.nan,np.nan]
#
peak_1_h = [506.0236519496,506.8712157337,np.nan]
peak_2_h = [508.31047499,509.158038774,509.749734246]
peak_3_h = [510.6292815693,511.4448618144,512.052549056]
peak_4_h = [512.868129301,513.7156930855,514.4673062526]
peak_5_h = [515.2189194197,516.050491434,516.770121062]
peak_6_h = [np.nan,518.3053309354,np.nan,]

trou_1_h = [506.439437957,np.nan,508.0066313692]
trou_2_h = [508.7742363056,509.4458906255,510.2934544096]
trou_3_h = [511.093042885,511.780688974,512.56428568]
trou_4_h = [513.363874156,514.115487323,514.8830922595]
trou_5_h = [515.7466478134,516.3863185938,np.nan]
trou_6_h = [518.1134297014,np.nan,np.nan]
# mri
peak_1_m = [506.0048701577,506.889269395,507.489478646 ]
peak_2_m = [508.3443221245,509.1923450436,509.803921894]
peak_3_m = [510.6633124123,511.497694212,512.102450503]
peak_4_m = [512.945926382,513.7894022614,514.44644951]
peak_5_m = [515.242181471,516.1015719897,516.9405008294]
peak_6_m = [517.5543511994,np.nan,np.nan]

trou_1_m = [506.445933016,507.1620917814,508.0101147005]
trou_2_m = [508.8035731423,509.46744095,510.3177373894]
trou_3_m = [511.152119189,511.806892917,512.6071719187]
trou_4_m = [513.4347331584,514.130430245,514.896606448]
trou_5_m = [515.7537234467,516.4767027716,517.197408577]
trou_6_m = [np.nan, np.nan, np.nan]
#
whole = [  [ [peak_1_h,peak_2_h,peak_3_h,peak_4_h,peak_5_h,peak_6_h] , [trou_1_h,trou_2_h,trou_3_h,trou_4_h,trou_5_c,trou_6_h] ],\
        [ [peak_1_c,peak_2_c,peak_3_c,peak_4_c,peak_5_c,peak_6_c],[trou_1_c,trou_2_c,trou_3_c,trou_4_c,trou_5_c,trou_6_c]  ], \
        [ [peak_1_m,peak_2_m,peak_3_m,peak_4_m,peak_5_m,peak_6_m],[trou_1_m,trou_2_m,trou_3_m,trou_4_m,trou_5_m,trou_6_m]  ]]
whole_arr = np.array(whole,dtype=float) #should be 3, 2, 6, 3 #old = 2, 2, 6, 3
whole_arr = whole_arr + 2455000.0
np.save('results_code/derivative_analysis/extrema_post_times-wild.npy',whole_arr)
print(whole_arr[:,1,1,2])

scans_peaks = np.zeros_like(whole_arr)
for i in (0,1, 2): #h2o and co2 and mri
    for j in (0,1): #peaks/trough
        for k in range(6): #6 cycles
            scans_peaks[i,j,k] = [ selector( whole_arr[i,j,k,l] ) for l in range(3) ]
            pass
        pass
    pass
np.save('results_code/derivative_analysis/extrema_post_scans.npy-wild',scans_peaks)
print(scans_peaks[:,1,1,2])
#print(scans_peaks)


#print(whole_arr.shape)
#print(trou_2_h[2])
#


#peaks1 = [ post_peaks_c_1[i+1]-post_peaks_c_1[i] for i in range(len(post_peaks_c_1)-1) ]
#peaks2 = [ post_peaks_c_2[i+1]-post_peaks_c_2[i] for i in range(len(post_peaks_c_2)-1) ]
#peaks3 = [ post_peaks_c_3[i+1]-post_peaks_c_3[i] for i in range(len(post_peaks_c_3)-1) ]
#peak1to2 = [ post_peaks_c_2[i] - post_peaks_c_1[i] for i in range(len(post_peaks_c_1))  ]
#peak2to3 = [ post_peaks_c_3[i] - post_peaks_c_2[i] for i in range(len(post_peaks_c_2))  ]
#peak1to3 = [ post_peaks_c_3[i] - post_peaks_c_1[i] for i in range(len(post_peaks_c_2))  ]

#print(np.array(peak1to2)*24.)
#print(np.array(peak2to3)*24.)
#print(peaks3)

pass
