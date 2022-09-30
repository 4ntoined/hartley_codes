import numpy as np
from scipy.signal import lombscargle as lomb
import matplotlib.pyplot as plt
from cometmeta import a
from datafunctions import selector

def figg():
    fig,ax = plt.subplots()
    fig.figsize=(10,6)
    fig.dpi=140   
    return fig, ax
def axxx(figgs, axxs, ymax=1., d1=316.0, d2=318.0):
    axxs.set_xlim(d1,d2)
    axxs.set_ylim(-ymax*0.07,ymax)
    axxs.set_xlabel('Day of year')
    axxs.set_ylabel('Brightness [arbitrary units]')
    #ax.set_title("")
    #axxs.legend(loc='best')
    return

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

dateA, h2oA, co2A , dystA,flag = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x2_15.txt",dtype=float,unpack=True,skiprows=1)
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
doyc=2455196.5
d1, d2 = 2455507.45, 2455513.05
d1-=doyc
d2-=doyc
maxy=0.0352

fig,ax=figg()
#ax.plot(x_t-doyc, y_lit27jet2, color='blue', label='86N, 30E' )

ax.plot(x_t-doyc, jet1, color='purple', label='90S' )
#ax.plot(x_t-doyc, jet2, color='royalblue' , label='60S, 90E')
#ax.plot(x_t-doyc, jet3, color='deepskyblue', label='30S, 90E')
#ax.plot(x_t-doyc, jet4, color='limegreen', label='0N, 90E')
#ax.plot(x_t-doyc, jet5, color='darkgoldenrod', label='30N, 90E')
#ax.plot(x_t-doyc, jet6, color='orangered', label='60N, 90E')
#ax.plot(x_t-doyc, jet7, color='red', label='90N')
#ax.plot(x_t-doyc, jet8, color='green', label='86N, 210E')
#ax.plot(x_t-doyc, jet9, color='pink', label='90N')
#ax.plot(x_t-doyc, jet10, color='magenta', label='80N, 90E')
#ax.plot(x_t-doyc, jet11, color='steelblue', label='75N, 90E')
#ax.plot(x_t-doyc, jet12, color='darkmagenta', label='70N, 90E')
#ax.plot(x_t-doyc, jet13, color='chocolate', label='65N, 90E')
#ax.plot(x_t-doyc, jet14, color='darkseagreen', label='55N, 90E')
#ax.plot(x_t-doyc, jet15, color='crimson', label='50N, 90E')
#ax.plot(x_t-doyc, jet16, color='lime', label='45N, 90E')
#ax.plot(x_t-doyc, jet17, color='darkkhaki', label='40N, 90E')
#ax.plot(x_t-doyc, jet18, color='violet', label='80N, 0E')
#ax.plot(x_t-doyc, jet19, color='yellow', label='80N, 180E')
#ax.plot(x_t-doyc, jet20, color='darkgoldenrod', label='80N, 270E')

#ax.plot(x_t, y_jet2, color='pink' )
#ax.plot(x_t, y_mri_dist*1e9, color='k')
#ax.plot(x_t, y_500jet)
#ax.plot(x_t, y_jetnuke +1)
#ax.plot(x_t, y_mri_dist*1e8, color='k')
ax.scatter(x_t-doyc, co2A*25*40,s=1,color='k',zorder=10, label='$CO_2$ data')
#ax.vlines(x_t[maxes]-doyc,ymin=0,ymax=0.1,linewidth=1.,color='grey')

#ax.plot(x_t2,y542)
#ax.plot(x_period,pgram27)
#ax.plot(x_period,pgram54)

axxx(fig, ax, d1=d1, d2=d2, ymax=maxy)
plt.savefig('/home/antojr/dps_bucket/synthetic_curves/90S_focus_2.png',dpi=fig.dpi)#,bbox_inches='tight')
plt.show(block=True)
#input('enter')

