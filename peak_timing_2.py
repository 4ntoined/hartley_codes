#Antoine

import numpy as np
import matplotlib.pyplot as plt

peak_data = np.load('results_code/peak_times.npy')

peak_data *= 24.*60.
#peak_data[h2o/co2, peak/trough, 6 cycles, 3 per cycle]

# peak-n to peak-n

peak1s = [ peak_data[:,:,i+1,0] - peak_data[:,:,i,0] for i in range(len(peak_data[0,0,:,0])-1) ]
#print(peak1s)
peak1s = np.array(peak1s)
#print(peak1s.shape) peak1s[5 cycle diffs, h2o/co2, peak/trough]
peak2s = [ peak_data[:,:,i+1,1] - peak_data[:,:,i,1] for i in range(len(peak_data[0,0,:,1])-1) ]
peak3s = [ peak_data[:,:,i+1,2] - peak_data[:,:,i,2] for i in range(len(peak_data[0,0,:,2])-1) ]
peak2s = np.array(peak2s)
peak3s = np.array(peak3s)
#hour conversion
#peak1s *= 24.
#peak2s *= 24.
#peak3s *= 24.
#rid of nans
peak1s = np.where( np.isnan(peak1s), -9999., peak1s )
peak2s = np.where( np.isnan(peak2s), -9999., peak2s )
peak3s = np.where( np.isnan(peak3s), -9999., peak3s )


print('H2O, peak 1s')
print(peak1s[:,0,0])
print('CO2, peak 1s')
print(peak1s[:,1,0])
print('H2O, peak 2s')
print(peak2s[:,0,0])
print('CO2, peak 2s')
print(peak2s[:,1,0])
print('H2O, peak 3s')
print(peak3s[:,0,0])
print('CO2, peak 3s')
print(peak3s[:,1,0])

print('H2O, trough 1s')
print(peak1s[:,0,1])
print('CO2, trough 1s')
print(peak1s[:,1,1])
print('H2O, trough 2s')
print(peak2s[:,0,1])
print('CO2, trough 2s')
print(peak2s[:,1,1])
print('H2O, trough 3s')
print(peak3s[:,0,1])
print('CO2, trough 3s')
print(peak3s[:,1,1])

print('peak')
#gas differences
peak1diff = peak_data[0,0,:,0] - peak_data[1,0,:,0] 
print( peak_data[0,0,:,0] - peak_data[1,0,:,0]  )
peak2diff =  peak_data[0,0,:,1] - peak_data[1,0,:,1]  
print( peak_data[0,0,:,1] - peak_data[1,0,:,1]  )
peak3diff =  peak_data[0,0,:,2] - peak_data[1,0,:,2]  
print( peak_data[0,0,:,2] - peak_data[1,0,:,2]  )
print('trough')
trou1diff = peak_data[0,1,:,0] - peak_data[1,1,:,0]
print( peak_data[0,1,:,0] - peak_data[1,1,:,0]  )
trou2diff = peak_data[0,1,:,1] - peak_data[1,1,:,1]
print( peak_data[0,1,:,1] - peak_data[1,1,:,1]  )
trou3diff = peak_data[0,1,:,2] - peak_data[1,1,:,2]
print( peak_data[0,1,:,2] - peak_data[1,1,:,2]  )
storr = []
for i in (peak1diff,peak2diff,peak3diff,trou1diff,trou2diff,trou3diff): storr.append( np.where(np.isnan(i), -9999., i )  )
peak1diff,peak2diff,peak3diff,trou1diff,trou2diff,trou3diff = storr

fig,ax = plt.subplots()
fig.dpi=140
fig.figsize=(12,5.5)

#ax.scatter(range(5),peak1s[:,0,0], label='h2o peak 1', color='cornflowerblue' )
#ax.scatter(range(5),peak1s[:,1,0], label='co2 peak 1', color='green' )
#ax.scatter(range(6),peak1diff, label='peak 1 diffs', color='purple' )
#ax.scatter(range(6),peak2diff, label='peak 2 diffs', color='red' )
#ax.scatter(range(6),peak3diff, label='peak 2 diffs', color='goldenrod' )

ax.scatter(range(6),trou1diff, label='trough 1 diffs', color='purple' )
ax.scatter(range(6),trou2diff, label='trough 2 diffs', color='red' )
ax.scatter(range(6),trou3diff, label='trough 3 diffs', color='goldenrod' )

ax.legend(loc='best')
plt.show()

