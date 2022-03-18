#Antoine
#FFT

import numpy as np
import scipy.fft
import matplotlib.pyplot as plt

N=512
delt = 6*np.pi / N
ts = np.linspace(0,delt * N,N,endpoint=False)
xs = 2*np.sin(ts*10) + 0.5*np.sin(ts*2)
ys = scipy.fft.fft(xs)
fs = scipy.fft.fftfreq(N, delt)[:N//2]


fig,ax = plt.subplots()
fig.figsize = (10,5.6)
fig.dpi  = 140
#
#ax.scatter(ts,xs,s=0.7)
ax.plot(ts,xs)
#ax.plot(fs,2/N * np.abs(ys[:N//2]))
#
plt.show()

fig,ax = plt.subplots()
fig.figsize = (10,5.6)
fig.dpi  = 140
#
#ax.scatter(ts,xs,s=0.7)
#ax.plot(ts,xs)
ax.plot(fs,2/N * np.abs(ys[:N//2]))
#
plt.show()

