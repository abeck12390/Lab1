import numpy as np
from astropy.io import fits
#Creating the master dark--------------------------------------------------------------------
data= np.zeros((10, 1024, 1024))
master_dark = np.zeros((1024,1024))
for i in range (0,10):
    file = "10dark_" + str(i) +".FIT"
    dark = fits.open(file)
    current_dark=dark[0].data
    #print(current_dark)
    for n in range(0,1024):
        for j in range(0,1024):
            data[i,n,j]=current_dark[n,j]

median_list=[]
for n in range(0,1024):
    for j in range(1024):
        median_list.clear()
        for i in range(0,10):
            median_list.append(data[i,n,j])
        master_dark[n,j] = np.median(median_list)
print(master_dark)

new_dark = fits.PrimaryHDU(master_dark)
new_dark.writeto('master_dark.fits')



