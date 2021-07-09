#Antoine
#gonna look at the level of the darks over temp
#name 0// mid-observation time 1// exposure id 2// DOY 3// date 4// optical-bench temp 5// exposure time, 6 probably in milliseconds

import numpy.polynomial.polynomial as poly
import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from temperature_timeline import ttimeline

timer = interp1d(ttimeline[:,0],ttimeline[:,1],kind="linear", bounds_error=False)

## name // mid-observation time // exposure id // DOY // date // optical-bench temp // exposure time,probably in milliseconds
sev_dat = np.loadtxt("seven.dat", dtype=object,skiprows=1)
#sev_means = fits.open("darkmeans_7.fit")
sev_means2 = fits.open("darkmeansv2_7.fit")
eig_dat = np.loadtxt("eight.dat", dtype=object,skiprows=1)
#eig_means = fits.open("darkmeans_8.fit")
eig_means2 = fits.open("darkmeansv2_8.fit")
twe_dat = np.loadtxt("twleve.dat", dtype=object,skiprows=1)
#twe_means = fits.open("darkmeans_12.fit")
twe_means2 = fits.open("darkmeansv2_12.fit")
##
"""
pot = [[float(sev_dat[i,5]),sev_means[0].data[i]/7000.33,sev_means2[0].data[i]/7000.33] for i in range(len(sev_dat))]
pot2 = [[float(eig_dat[i,5]),eig_means[0].data[i]/8000.33,eig_means2[0].data[i]/8000.33] for i in range(len(eig_dat))]
pot3 = [[float(twe_dat[i,5]),twe_means[0].data[i]/12000.33,twe_means2[0].data[i]/12000.33] for i in range(len(twe_dat))]
pot=np.array(pot)
pot2=np.array(pot2)
pot3=np.array(pot3)
"""
###
p1_t = [float(sev_dat[i,1]) for i in range(len(sev_dat))]
p1_x = timer(p1_t)
p1_y = sev_means2[0].data/7000.33

p2_t = [float(eig_dat[i,1]) for i in range(len(eig_dat))]
p2_x = timer(p2_t)
p2_y = eig_means2[0].data/8000.33

p3_t = [float(twe_dat[i,1]) for i in range(len(twe_dat))]
p3_x = timer(p3_t)
p3_y = twe_means2[0].data/12000.33

doy7 = [int(sev_dat[i,3]) for i in range(len(sev_dat))]
doy8 = [int(eig_dat[i,3]) for i in range(len(eig_dat))]
doy12 = [int(twe_dat[i,3]) for i in range(len(twe_dat))]

exp7 = [str(sev_dat[i,2]) for i in range(len(sev_dat))]
exp8 = [str(eig_dat[i,2]) for i in range(len(eig_dat))]
exp12 = [str(twe_dat[i,2]) for i in range(len(twe_dat))]
###
print(type(p1_t))
### cool let's see about a line of best fit
bestfit = poly.Polynomial.fit(p1_x, p1_y, deg=1)
best_b,best_m = bestfit.convert().coef
print("blue line: ",best_b,best_m)
fit_x = np.linspace(136.6,137.3,500)
fit_y = fit_x*best_m + best_b
#
bestfit_2 = poly.Polynomial.fit(p2_x, p2_y, deg=1)  #make this best fit line
best2_b,best2_m = bestfit_2.convert().coef          #extract the coefficients on t^0 and t^1
best2_b -= .003                                     #using this slope to judge outliers
print("pink line: ",best2_b,best2_m)
fit2_x = np.linspace(136.6,137.3,500)               #temperature domain to use for best fit lines
fit2_y = fit2_x*best2_m + best2_b                   #best fit line

fitline = interp1d(fit2_x,fit2_y,kind='linear',bounds_error=False)     #interpolating, to make it behave like a function (not just a list of values along this line)

#file to associate each scan with a smooth temp and a dark level
out=open("dark_temp.dat","w")
out.write("julian date, mid-obs // temperature, K (smooth) // dark level // exposure time // doy // exposure id \n")
#lets go sevens?
counting_weirds = 0
for i in range(len(p1_x)):
    out.write(f"{p1_t[i]} {p1_x[i]} {p1_y[i]} 7000.33 {doy7[i]} {exp7[i]}")
    if fitline(p1_x[i]) > p1_y[i]:
        counting_weirds+=1
        out.write(" high temp for dark level\n")
        print(f"{doy7[i]}:{exp7[i]} : {i} : {p1_x[i]}\n")
    else:
        out.write("\n")
for i in range(len(p2_x)):
    out.write(f"{p2_t[i]} {p2_x[i]} {p2_y[i]} 8000.33 {doy8[i]} {exp8[i]}")
    if fitline(p2_x[i]) > p2_y[i]:
        counting_weirds+=1
        out.write(" high temp for dark level\n")
        print(f"{doy8[i]}:{exp8[i]} : {i} : {p2_x[i]}\n")
    else:
        out.write("\n")
        
for i in range(len(p3_x)):
    out.write(f"{p3_t[i]} {p3_x[i]} {p3_y[i]} 12000.33 {doy12[i]} {exp12[i]}")
    if fitline(p3_x[i]) > p3_y[i]:
        counting_weirds+=1
        out.write(" high temp for dark level\n")
        print(f"{doy12[i]}:{exp12[i]} : {i} : {p3_x[i]}\n")
    else:
        out.write("\n")
out.close()
print(counting_weirds)


"""
##
fig,ax = plt.subplots()
fig.dpi=120
fig.figsize=(10,6)

ax.scatter(pot[:,0],pot[:,1],color="blue",s=1,label="7s")
#plt.show()
ax.scatter(pot2[:,0],pot2[:,1],color="red",s=1,label="8s")
#plt.show()
ax.scatter(pot3[:,0],pot3[:,1],color="green",s=1,label="12s")
ax.legend(loc="best")
ax.set_title("dark vs temperature, non-linearized")
ax.set_xlabel("temp, K (not smoothed)")
ax.set_ylabel("last frame mean/exptime (data/millisecond)")
plt.show()
"""
##
fig,ax = plt.subplots()
fig.dpi=120
fig.figsize=(10,6)
#ax.scatter(pot[:,0],pot[:,2],color="blue",s=1,label="7s")
ax.scatter(p1_x,p1_y,color="blue",s=1,label="7s")
#plt.show()
ax.scatter(p2_x,p2_y,color="red",s=1,label="8s")
#plt.show()
ax.scatter(p3_x,p3_y,color="green",s=1,label="12s")
ax.plot(fit_x,fit_y,color="lightblue",label="fit thru 7")
ax.plot(fit2_x,fit2_y,color="pink",label="fit thru 8")
#
ax.set_xlim(136.6,137.3)
ax.set_ylim(0.57,0.62)
ax.legend(loc="best")
ax.set_title("dark vs temperature, linearized")
ax.set_xlabel("temp, K (not smoothed)")
ax.set_ylabel("last frame mean/exptime (data/millisecond)")
plt.show()