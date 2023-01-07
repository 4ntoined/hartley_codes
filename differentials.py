#Antoine
#derivative or something I guess

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

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
def plot_line(curves, colors=['blue','red'], labels=['H','C'], zero=False):
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
    yval_mean  = yval / np.mean(yval)
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
    y_deriv_checked = y_deriv[ check_for_99s ]
    time_checked = timeline[ check_for_99s ]
    return (time_checked, y_deriv_checked, rejected)
def a_line(xx, a, b):
    return a*xx+b
a = np.load('a_cometmeta.npy')
tt = a['julian date'].copy()
dat, h1, c1, d1, flag1 = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x4_424km-corrected.txt",dtype=float,unpack=True,skiprows=1)
#plot her
#plot_curve([c1,h1])
#masking the data for no nucleuses
check_for_nucleus =  np.abs(c1) > 1e-3

c1_mask = c1[ check_for_nucleus ]
h1_mask = h1[ check_for_nucleus ]
tt_mask = tt[ check_for_nucleus ]

### testing the new function ###
t_h, y_h, rejected_h = get_derivative(tt_mask, h1_mask, 6., even_sampling=True)
t_c, y_c, rejected_c = get_derivative(tt_mask, c1_mask, 6., even_sampling=True)


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

