import numpy as np
from scipy.signal import lombscargle as lomb
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector

ind, tims = np.loadtxt('/home/antojr/stash/datatxt/scantimes.txt',unpack=True,skiprows=1)
lit27 = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v2_27.txt',unpack=True)
lit54 = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v2.txt',unpack=True)
lit27_area = np.loadtxt('/home/antojr/hartley2/shape_model/litness_v3_27.txt',unpack=True) 
lit27_jet = np.loadtxt('/home/antojr/hartley2/shape_model/litness_jet_v1.txt',unpack=True) 

#lit27_jet2 = np.loadtxt('/home/antojr/stash/datatxt/litness_jet_86-30.txt',unpack=True)
lit_jetsun = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun80-90.txt',unpack=True)
lit_jet2 = np.loadtxt('/home/antojr/stash/datatxt/litness_jet80-90.txt',unpack=True)

jet1 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_-90+90.txt',unpack=True)
jet2 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_-60+90.txt',unpack=True)
jet3 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_-30+90.txt',unpack=True)
jet4 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+00+90.txt',unpack=True)
jet5 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+30+90.txt',unpack=True)
jet6 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+60+90.txt',unpack=True)
jet7 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+90+90.txt',unpack=True)
jet8 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+86+210.txt',unpack=True)
jet9 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+90+30.txt',unpack=True)
lit27_jet2 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+86+30.txt',unpack=True)
### latitudes @ 90E ###
jet10 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+80+90.txt',unpack=True)
jet11 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+75+90.txt',unpack=True)
jet12 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+70+90.txt',unpack=True)
jet13 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+65+90.txt',unpack=True)
jet14 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+55+90.txt',unpack=True)
jet15 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+50+90.txt',unpack=True)
jet16 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+45+90.txt',unpack=True)
jet17 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+40+90.txt',unpack=True)
### longitudes @ 80N ###
jet18 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+80+00.txt',unpack=True)
jet19 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+80+180.txt',unpack=True)
jet20 = np.loadtxt('/home/antojr/stash/datatxt/litness_jetsun_+80+270.txt',unpack=True)

dateA, h2oA, co2A , dystA,flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_v9_15.txt",dtype=float,unpack=True,skiprows=1)
maxes, daats, doys, exps = np.loadtxt("/home/antojr/stash/datatxt/mri_maxes_v3.txt",skiprows=1,dtype=object,unpack=True)
maxes = maxes.astype(int)

y_lit27 = lit27.copy()
y_lit54 = lit54.copy()
y_lit27area = lit27_area.copy()
y_lit27jet = lit27_jet.copy()
y_lit27jet2 = lit27_jet2.copy()
y_jetsun =  lit_jetsun.copy()
y_jet2 = lit_jet2.copy()

x_t = tims.copy()
### splitting up the lcs before doing the most
cut = selector('2455504.1') +3 
x_t2 = x_t[cut:]
y542 = y_lit54[cut:]
y272 = y_lit27[cut:]

### some periodigrams
lots = int(1e4)
x_period = np.linspace(0.01, 5, lots)
pgram54 = lomb(x_t, y_lit54, x_period, normalize = False)
#pgram54 = lomb(x_t2, y542, x_period, normalize = True)
#pgram27 = lomb(x_t2, y272, x_period, normalize = True)

#getting the mri out to compare
y_mri_dist = a['mri 7-pixel'] / a['comet dist']**0
#scl = abs(y_mri_dist[400]/y_lit27jet[400])
#scl2 = abs(y_mri_dist[400]/y_lit27jet2[400])
#print(scl)

"""
fig,ax=plt.subplots()
fig.dpi=140
fig.figsize = (10,6)
ax.plot(x_t, y_lit27 )
#ax.plot(x_t2,y542)
#ax.plot(x_period,pgram27)
#ax.plot(x_period,pgram54)
xlims = (2455505.5,2455510.5)
ax.set_xlim(xlims[0],xlims[1])
plt.show(block=False)
"""
fig,ax=plt.subplots()
fig.dpi=140
fig.figsize = (10,6)
#ax.plot(x_t, y_lit27jet2, color='blue', label='86N, 30E' )

#ax.plot(x_t, jet1, color='purple', label='90 S' )
#ax.plot(x_t, jet2, color='royalblue' , label='60 S')
#ax.plot(x_t, jet3, color='deepskyblue', label='30 S')
#ax.plot(x_t, jet4, color='limegreen', label='0 N')
#ax.plot(x_t, jet5, color='gold', label='30 N')
#ax.plot(x_t, jet6, color='darkorange', label='60 N')
#ax.plot(x_t, jet7, color='red', label='90 N')
#ax.plot(x_t, jet8, color='green', label='86N, 210E')
#ax.plot(x_t, jet9, color='pink', label='90N, 90E')
ax.plot(x_t, jet10, color='magenta', label='80N, 90E')
#ax.plot(x_t, jet11, color='steelblue', label='75N, 90E')
#ax.plot(x_t, jet12, color='darkmagenta', label='70N, 90E')
#ax.plot(x_t, jet13, color='chocolate', label='65N, 90E')
#ax.plot(x_t, jet14, color='darkseagreen', label='55N, 90E')
#ax.plot(x_t, jet15, color='crimson', label='50N, 90E')
#ax.plot(x_t, jet16, color='lime', label='45N, 90E')
#ax.plot(x_t, jet17, color='darkkhaki', label='40N, 90E')
ax.plot(x_t, jet18, color='violet', label='80N, 0E')
#ax.plot(x_t, jet19, color='yellow', label='80N, 180E')
ax.plot(x_t, jet20, color='darkgoldenrod', label='80N, 270E')


#ax.plot(x_t, y_jet2, color='pink' )
#ax.plot(x_t, y_mri_dist*1e9, color='k')
#ax.plot(x_t, y_500jet)
#ax.plot(x_t, y_jetnuke +1)
#ax.plot(x_t, y_mri_dist*1e8, color='k')
ax.scatter(x_t, co2A*1e2,s=1,color='k',zorder=10)
ax.vlines(x_t[maxes],ymin=0,ymax=0.1,linewidth=1.,color='grey')

#ax.plot(x_t2,y542)
#ax.plot(x_period,pgram27)
#ax.plot(x_period,pgram54)
xlims = (2455505.5,2455512.5)
ax.set_xlim(xlims[0],xlims[1])
#ax.set_xlim((0.1,1))
ax.set_ylim((-1e-4,0.007))
ax.set_xlabel('Julian Date')
ax.set_ylabel('Brightness')
ax.legend(loc='best')
#plt.savefig('synthcurve_5days.png',dpi=fig.dpi)
plt.show(block=True)
#input('enter')

