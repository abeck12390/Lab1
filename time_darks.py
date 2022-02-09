import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('TkAgg')
import math
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
from scipy.optimize import curve_fit


data= np.zeros((7, 1024, 1024))

for i in range (0,7):
    file = "timedark" + str(i) + ".FIT"
    timedark = fits.open(file)
    current_dark=timedark[0].data
    #print(current_dark)
    for n in range(0,1024):
        for j in range(0,1024):
            data[i,n,j]=current_dark[n,j]


#for n in range(0,7):
#    current_image = data[n].flatten()
#    print(n)
#    plot=plt.hist(current_image,range=[900,upper_bound[i]], bins=80);
#    plt.yscale('log')
#    plt.show()
upper_bound = [1025,1030,1050,1065,1075,1100,1120]

data_within = []
mu = []
std = []
statstd = []
leftovermu = []
for n in range(0,7):
    current_data = data[n].flatten()
    data_within.append(current_data[(current_data>=np.min(current_data)) & (current_data <= upper_bound[n])])
    leftovermu.append(np.average(current_data[((current_data >= upper_bound[n])) & (current_data <= np.max(current_data))]))
    mu.append(np.average(data_within[n]))
    std.append(np.std(data_within[n]))
    #print(data_within[n])
    #print(mu[n])
    #print(std[n])
    statstd.append(std[n]/math.sqrt(len(data_within[n])))
    #print(statstd[n])
    #print("changed bounds")
    #data_within.append(current_data[(current_data >= np.min(current_data)) & (current_data <= (upper_bound[n]-50))])
    #mu.append(np.average(data_within[n]))
    #std.append(np.std(data_within[n]))
    #print(data_within[n])
    #print(mu[n])
    #print(std[n])
    #statstd.append(std[n]/math.sqrt(len(data_within[n])))
    #print(statstd[n])
print(mu)
print(leftovermu)
exptime = [10,30,50,70,90,110,130]

#plt.errorbar(exptime, mu, yerr=statstd,fmt='o', label="data")
plt.errorbar(exptime, leftovermu, yerr=statstd,fmt='o', label="data")
plt.xlabel('Exposure time (s)')
plt.ylabel('Average number of counts leftover')

def func(x,a,b):
    return a+b*x
best_vals, covar = curve_fit(func, exptime, mu, sigma=statstd)
a=best_vals[0]
b=best_vals[1]


x = np.linspace(0, 150, num=100)
yfit = func(x,a,b)
plt.plot(x,yfit,label="fit")
print(b)
plt.legend()
plt.show()


