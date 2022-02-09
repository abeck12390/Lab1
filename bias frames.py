import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

bias_image=fits.open('0cbias.FIT')
bias_1d = bias_image[0].data.flatten()
#plot=plt.hist(bias_1d,range=[950,1300], bins=80);

#print(np.mean(bias_1d))
#print(stats.mode(bias_1d)[0][0])
#print(np.median(bias_1d))
#print(np.std(bias_1d))





cmin=950
cmax=1200
nbins=100
normalization=(cmax-cmin)/nbins*len(bias_1d[(bias_1d>=cmin) & (bias_1d<=cmax)])

clipmin=cmin
clipmax=1030
clippedvalues = bias_1d[(bias_1d>=clipmin) & (bias_1d<=clipmax)]

cutvalues = bias_1d[(bias_1d>=1300)]
fraction_pix = len(cutvalues)/len(bias_1d)

mu=np.mean(clippedvalues)
sig=np.std(clippedvalues)
mode=stats.mode(clippedvalues)[0][0]

print('mu ' + str(mu))
print('sig ' + str(sig))

xarray=np.linspace(cmin,cmax,nbins*10)
yarray=normalization*norm.pdf(xarray,loc=mu, scale=sig)

plt.hist(bias_1d,range=[cmin,cmax], bins=nbins);
plt.yscale('log')
plt.ylim([0.1,1e6])
plt.plot(xarray,yarray,color="red",linewidth=3.0)
plt.axvline(x=mode,linewidth=3.0,color="yellow")

header = bias_image[0].header
gain = header['EGAIN']
muNelectron = gain * sig
print(muNelectron)




plt.show()