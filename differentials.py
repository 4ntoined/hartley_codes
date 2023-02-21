#Antoine
#derivative or something I guess

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from distance_corrections_gascurve import masking

def plot_scatter(curves, colors=['blue','red'], labels=['H','C'], zero=False):
    """
    curves is a list of pairs of arrays to plot
    curves =  [[x1,y1],[x2,y2],... ]
    """
    fig,ax = plt.subplots()
    fig.dpi=140
    fig.figsize=(11,6)
    #
    for i in range(len(curves)):
        ax.scatter(curves[i][0],curves[i][1],color=colors[i],label=labels[i], s=1.)
        #
    if zero: ax.hlines((0.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1])
    ax.set_ylabel('Flux')
    ax.set_xlabel('Julian Date')
    ax.legend(loc='best')
    #
    plt.show()
    return
def plot_line(curves, colors=['blue','red'], labels=['H','C'], zero=False, title=''):
    """
    curves is a list of curves
    """
    fig,ax = plt.subplots()
    fig.dpi=140
    fig.figsize=(11,6)
    #
    for i in range(len(curves)):
        ax.plot(curves[i][0],curves[i][1],color=colors[i],label=labels[i])
        #
    if zero: ax.hlines((0.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1])
    ax.set_ylabel('Flux')
    ax.set_xlabel('Julian Date')
    if title: ax.set_title(title)
    ax.legend(loc='best')
    #
    plt.show()
    return
def new_derivatives(hourperiod, time_array, gas_array):
    period = hourperiod / 24.  #hrs / 24 (hrs/day)
    derivs = []
    groupies_count = 0
    for i in range( len( time_array )):
        earlybound = time_array[i] - period / 2.
        lateybound = time_array[i] + period / 2.
        groupies = np.argwhere( np.logical_and( time_array > earlybound, time_array < lateybound ))
        #print(len(groupies))
        #we've identified all the scans indeces in the period
        #we're gonna turn them into segments of the lightcurve and fit lines to them
        #with these fit lines we'll measure the slope and call it the numerical derivative
        #so who's gonna code that
        if len(groupies) > 2:
            #this line fits a line to this portion of the co2 lightcurve
            #if gas=='green': ops, cov = curve_fit( a_line, tt_mask[groupies[0][0]:groupies[-1][0]], c1_mask[groupies[0][0]:groupies[-1][0]] )
            #" " H2o lightcurve
            #elif gas=='blue': 
            ops, cov = curve_fit( a_line, time_array[groupies[0][0]:groupies[-1][0]], gas_array[groupies[0][0]:groupies[-1][0]] )
            #using the timeline array and fit parameters to make the line of fit
            fitline = a_line(time_array[groupies[0][0]:groupies[-1][0]], ops[0], ops[1])
            #calculating the derivative at this time/for this period
            y2 = fitline[-1]
            y1 = fitline[0]
            deriv = (y2-y1)/ ( time_array[ groupies[-1] ] - time_array[ groupies[0] ])
        else:
            groupies_count+=1
            print(str(time_array[i]) +  " :not enough groupies")
            deriv = -99.
        derivs.append(deriv)
    return (derivs, groupies_count)
def find_zeros_bad(curve):
    """
    curve is 1d array-like
    will return indices where we cross from negative to positive
    """
    checking_for_positives = True
    switches = []
    for i in range(len(curve)):
        point = curve[i]
        #check if point is positive
        posit = point > 0.
        if checking_for_positives and posit:
            checking_for_positives = False
            switches.append(i)
        elif (not checking_for_positives) and (not posit):
            checking_for_positives = True
            switches.append(i)
        pass
    return switches
def find_zeros(curve):
    """
    take pairs of neighboring points across the curve and determine if there is a sign flip between them
    """
    pairs = [ float(curve[i] / curve[i+1]) for i in range(len(curve)-1)]
    #print(pairs)
    pairs = np.array(pairs, dtype=float)
    #print(pairs)
    ans = np.argwhere( pairs < 0.)
    return ans
def get_derivative(times, yval, period, even_sampling = False, num_samples = 1500):
    """
    times = an array of time values
    yval = an array of data values to go along with time
    even_sampling set to True to use even sampling along time-axis
    num_samples to set number of even samples 
    """
    #before using you should get rid of error values ie -99 or 0 in lightcurves
    #normalize by dividing out mean
    yval_mean = yval.copy()
    #even sampling if you want
    if even_sampling:
        #do all the even sampling stuff
        #creating an even time sampling
        timeline = np.linspace(times[0],times[-1], num_samples, dtype=float)
        #creating interpolation object from data
        data_interp = interp1d(times, yval_mean, kind='linear', fill_value = 0.)
        #using interpolation object to create new (even) data array
        y_data = data_interp(timeline) #co2 lightcurve plotted for even timesteps
    else:
        #for going with the given
        timeline = times.copy()
        y_data = yval_mean.copy()
    #counting me how many we lost 
    y_deriv, rejected = new_derivatives(period, timeline, y_data)
    y_deriv = np.array(y_deriv, dtype=float)
    check_for_99s = np.ravel( y_deriv > -99. )
    #rejected = np.count_nonzero(~check_for_99s)
    y_deriv_checked = y_deriv[ check_for_99s ].squeeze()
    time_checked = timeline[ check_for_99s ]
    #for i in (time_checked, y_deriv_checked): print(i.shape)
    return (time_checked, y_deriv_checked, rejected)
def a_line(xx, a, b):
    return a*xx+b
if __name__ == '__main__':
    a = np.load('a2_cometmeta.npy')
    #dat, h1, c1, d1, flag1 = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x4_424km-corrected.txt",dtype=float,unpack=True,skiprows=1)
    #loading in the curves
    gases = np.load('results_code/gascurves_x5-eorrect.npy')
    mridata = np.load('results_code/mri_dorrect.npy')
    #assigning the curves
    h1, c1, d1 = gases['h2o'], gases['co2'], gases['dust']
    mri14 = mridata['14-pix'].copy()
    #assinging the timing data
    #gasdate = a['julian date'].copy()
    tti = a['julian date'].copy()
    mridate = mridata['date'].copy()
    #plot her
    #plot_curve([c1,h1])
    #masking the data for no nucleuses
    #check_for_nucleus =  np.abs(c1) > 1e-3
    #c1_mask = c1[ check_for_nucleus ]
    #h1_mask = h1[ check_for_nucleus ]
    #tt_mask = tt[ check_for_nucleus ]
    
    ### new variable names + meaning  yval_mean  = yval / np.mean(yval)
    yh = h1 / np.mean(c1)
    yc = c1 / np.mean(c1)
    ym  = mri14 / np.mean(mri14) 
    tt = tti.copy()
    
    ### first derivatives : change in flux over time : speed 
    #   zero = peaks and troughs of lightcurve : positive and negative = slope of lightcurve
    print('==== getting first derivative ====')
    t_h, dy_h, rejected_dh = get_derivative(tt, yh, 6., even_sampling=True)
    t_c, dy_c, rejected_dc = get_derivative(tt, yc, 6., even_sampling=True)
    t_m, dy_m, rejected_dm = get_derivative(mridate, ym, 6., even_sampling=True, num_samples=24400)
    print('lost for lack of neighbors: ' + str(rejected_dh) + ',' + str(rejected_dc))
    # look for the zeros
    zeros1_h= np.squeeze( find_zeros(dy_h) )
    zeros1_c= np.squeeze( find_zeros(dy_c) )
    zeros1_m= np.squeeze( find_zeros(dy_m) )
    ### second derivatives : change in flux speed over time : acceleration 
    #   zero = inflection points in lightcurve : positive and negative = concavity (up and down) of lightcurve ###
    print('==== getting second derivative ====')
    tt_h, ddy_h, rejected_ddh = get_derivative(t_h, dy_h, 6.) #, even_sampling=True)
    tt_c, ddy_c, rejected_ddc = get_derivative(t_c, dy_c, 6.) #, even_sampling=True)
    tt_m, ddy_m, rejected_ddm = get_derivative(t_m, dy_m, 6., even_sampling=True, num_samples=24400)
    print('lost for lack of neighbors: ' + str(rejected_ddh) + ',' + str(rejected_ddc))
    #zeros2_c= find_zeros(ddy_c)
    #zeros2_h= find_zeros(ddy_h)
    zeros2_h= np.squeeze( find_zeros(ddy_h) )
    zeros2_c= np.squeeze( find_zeros(ddy_c) )
    zeros2_m= np.squeeze( find_zeros(ddy_m) )
    #print(len(tt_h),len(ddy_h))
    ### third derivatives : change in flux acceleration : jerk
    print('==== getting third derivative ====')
    ttt_h, dddy_h, rejected_dddh = get_derivative(tt_h, ddy_h, 2.) #, even_sampling=True)
    ttt_c, dddy_c, rejected_dddc = get_derivative(tt_c, ddy_c, 2.) #, even_sampling=True)
    ttt_m, dddy_m, rejected_dddm = get_derivative(tt_m, ddy_m, 2., even_sampling=True, num_samples=24400)
    print('lost for lack of neighbors: ' + str(rejected_dddh) + ',' + str(rejected_dddc)) 
    zeros3_h= np.squeeze( find_zeros(dddy_h) )
    zeros3_c= np.squeeze( find_zeros(dddy_c) )
    zeros3_m= np.squeeze( find_zeros(dddy_m) )
    #### work with the zeros ####
    #print(t_c[np.squeeze(zeros1_c)])
    t_zero_h = t_h[ zeros1_h ]
    t_zero_c = t_c[ zeros1_c ]
    t_zero_m = t_m[ zeros1_m ]
    t_zero_h2 = tt_h[ zeros2_h ]
    t_zero_c2 = tt_c[ zeros2_c ]
    t_zero_m2 = tt_m[ zeros2_m ]
    save_folder1 = 'results_code/derivative_analysis/'
    #np.save("times_zeros_h.npy",t_zero_h)
    #np.save("times_zeros_c.npy",t_zero_c)
    #np.save("times_zeros_h2.npy",t_zero_h2)
    #np.save("times_zeros_c2.npy",t_zero_c2)
    #print(np.sum(tt_h - t_h))
    #print(np.sum(tt_c-t_c))000
    np.save(save_folder1+"derivs_gastime.npy",t_c)
    np.save(save_folder1+"derivs_mritime.npy",t_m)
    np.save(save_folder1+"derivs_index_h1.npy",zeros1_h)
    np.save(save_folder1+"derivs_index_c1.npy",zeros1_c)
    np.save(save_folder1+"derivs_index_m1.npy",zeros1_m)
    np.save(save_folder1+"derivs_index_h2.npy",zeros2_h)
    np.save(save_folder1+"derivs_index_c2.npy",zeros2_c)
    np.save(save_folder1+"derivs_index_m2.npy",zeros2_m)
    np.save(save_folder1+"derivs_curve_h1.npy", dy_h)
    np.save(save_folder1+"derivs_curve_c1.npy", dy_c)
    np.save(save_folder1+"derivs_curve_m1.npy", dy_m)
    np.save(save_folder1+"derivs_curve_h2.npy", ddy_h)
    np.save(save_folder1+"derivs_curve_c2.npy", ddy_c)
    np.save(save_folder1+"derivs_curve_m2.npy", ddy_m)
    
    header1 = 'times of H2O 1st derivative zero crossings (before crossing): made by derivative.py'
    with open('lc_1deri_h-trash.txt','w') as fil:
        fil.write(header1 + '\n')
        for ih in range(np.size(zeros1_h)):
            fil.write( f"{ t_zero_h[ ih ]}\n" )
        pass
    header2 = 'times of CO2 1st derivative zero crossings (before crossing): made by derivative.py'
    with open('lc_1deri_c-trash.txt','w') as fil:
        fil.write(header2 + '\n')
        for ih in range(np.size(zeros1_c)):
            fil.write( f"{ t_zero_c[ ih ]}\n" )
        pass
    
    #curveset0 = [ [tt, y_c] ] #0th
    #curveset1 = [ [t_h,dy_h],[t_c,dy_c],[t_m,dy_m] ] #1st
    #curveset2 = [ [tt_h,ddy_h],[tt_c,ddy_c] ] #2nd
    #curveset3 = [ [ttt_h,dddy_h],[ttt_c,dddy_c] ] #3rd
    #curveset4 = [ [t_c,dy_c],[tt_c,ddy_c] ] #1st and 2nd, Co2
    #curveset5 = [ [tt_c,ddy_c],[ttt_c,dddy_c] ] #2nd and 3rd, Co2
    
    #for i in range(len(zeros1_c)):
    #    print(t_c[zeros1_c[i]])
    for i in range(len(zeros1_h)):
        print(t_h[zeros1_h[i]])
    
    
    print(len( zeros1_h), ',', len(zeros1_c))
    #plot_scatter( )
    plot_line(curveset1, title = 'First Deriv')
    #plot_line(curveset2, title = 'Second Deriv')
    #plot_line(curveset3, title = 'Third Deriv')
    #plot_line(curveset4 , title='First and Second', labels=['1st','2nd'])
    #plot_line(curveset5 , title='Second and Third', labels=['2nd','3rd'])
    
    fig,ax = plt.subplots()
    ax.scatter(tt, y_c/np.max(y_c), color='k', s=1., label='CO2 data')
    ax.plot(t_h, dy_c/np.max(dy_c), color='green', label='CO2 1-derivative')
    #ax.plot(t_h, ddy_c/np.max(ddy_c), color='red', label='CO2 2-derivative')
    #ax.scatter(tt, y_h/np.max(y_h), color='k', s=1., label='H2O data')
    ax.plot(t_h, dy_h/np.max(dy_h), color='blue', label='H2O 1-derivative')
    #ax.scatter(eventime,c_deri2, s=2.,marker='.', color='green')
    ax.hlines((0.),linewidth=0.7,color='k',xmin=tt[0],xmax=tt[-1])
    #ax.vlines(t_h[ zeros1_c],linewidth=0.7, color='k', ymin=-5., ymax = 5.)
    ax.vlines(t_h[ zeros1_h],linewidth=0.7, color='k', ymin=-5., ymax = 5.)
    #ax.vlines( [2455499.3, 2455503.3],linewidth=3.,color='k', ymin=-5, ymax=5. )
    #ax.vlines(eventime[resuh],linewidth=0.7, color='red', ymin=-5., ymax = 5.)
    ax.legend(loc='best')
    plt.show()

else:
    pass

"""
#meaning the data, for sanities' sake
c1_mask = c1_mask / np.mean(c1_mask)
h1_mask = h1_mask / np.mean(h1_mask)

### differentials, basic bad method ###
dtt = np.diff(tt_mask)
dyy = np.diff(c1_mask)
dyh = np.diff(h1_mask)
dydt = dyy/dtt #co2 rough derivative 
dhdt = dyh/dtt #h2o ""
#plot_line([dyy],['darkorange'],['derivative'])
#for i in dydt: print(i)
######################################

### interpolating across a more regular time axis ###
eventime = np.linspace(tt_mask[0],tt_mask[-1], 1500, dtype=float)
c_interp = interp1d(tt_mask, c1_mask, kind='linear', fill_value = 0.)
h_interp = interp1d(tt_mask, h1_mask, kind='linear', fill_value = 0.)
even_c = c_interp(eventime) #co2 lightcurve plotted for even timesteps
even_h = h_interp(eventime) #h2o "                                   "

#comparing data to even sampling measures
#plot_scatter([[tt_mask, c1_mask],[eventime,even_c]], labels=['data','even sampling'], zero=True)

#I turned it up
if len(sys.argv) >  1: take_anumber = float(sys.argv[1])
else: take_anumber = 6.
#take_anumber=6.
print(take_anumber)
## these use the observered data, missing nucleus scans removed ##
c1_derivative, n1 = new_derivatives(take_anumber, tt_mask, c1_mask)
h1_derivative, n2 = new_derivatives(take_anumber, tt_mask, h1_mask)
# these use the even timeline and related gascurves 
c_deri2, n3 = new_derivatives(take_anumber, eventime, even_c)
h_deri2, n4 = new_derivatives(take_anumber, eventime, even_h)
#turning them into arrays
c1_derivative = np.array(c1_derivative,dtype=float)
h1_derivative = np.array(h1_derivative,dtype=float)
c_deri2 = np.array(c_deri2,dtype=float)
h_deri2 = np.array(h_deri2,dtype=float)
#throwing out the no groupies misses
check_for_99s = c1_derivative > -99.
check_for_99s = np.ravel(check_for_99s)
c1_derivative = c1_derivative[ check_for_99s ]
h1_derivative = h1_derivative[ check_for_99s ]
print(check_for_99s.shape)
# applying the no groupies mask to the data for plot comparison
tt_mask = tt_mask[ check_for_99s ]
c1_mask = c1_mask[ check_for_99s ]
h1_mask = h1_mask[ check_for_99s ]

check99s_2 = np.ravel(c_deri2 > -99.)
print(check99s_2.shape)
c_deri2 = c_deri2[ check99s_2 ]
h_deri2 = h_deri2[ check99s_2 ]
eventime = eventime[ check99s_2 ]
even_c = even_c[ check99s_2 ]
even_h = even_h[ check99s_2 ]


#comparing differential w data to differential with even sampling
plot_line([[eventime, h_deri2],[tx, yx]], labels=['old','weeeee'], zero=True)


#we have to find where we cross to zero
resus = find_zeros_bad(c_deri2)
print(resus)
resu2 = find_zeros(c_deri2)
resuh = find_zeros(h_deri2)
print("co2 peaks and troughs:", len(resu2), "\n", eventime[resu2])
print("h2o peaks and troughs:", len(resuh), "\n", eventime[resuh])
#print("difference:\n", eventime[resu2]-eventime[resuh])

"""



""" #
#plot_line([c1_derivative])
fig,ax = plt.subplots()
#ax.scatter(tt_mask, c1_mask, color='k', s=1.)
#ax.plot(tt_mask, h1_derivative, color='blue')
#ax.scatter(eventime,c_deri2, s=2.,marker='.', color='green')
#ax.hlines((0.),linewidth=0.7,color='k',xmin=eventime[0],xmax=eventime[-1])
ax.vlines(eventime[resu2],linewidth=0.7, color='k', ymin=-5., ymax = 5.)
ax.vlines(eventime[resuh],linewidth=0.7, color='red', ymin=-5., ymax = 5.)
plt.show()
"""
pass

