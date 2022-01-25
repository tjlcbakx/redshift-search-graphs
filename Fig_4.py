##-----------------------------------------
## Code written and edited by Tom Bakx
## tjlcbakx@gmail.com
##-----------------------------------------


##-----------------------------------------
## Header imports, colours
##-----------------------------------------


import numpy as np
import matplotlib.pyplot as plt
import RSG

loFreq = np.array([89.13, 100.88, 92.83, 104.58, 96.53, 108.28, 139.85, 151.6, 143.54999999999998, 155.29999999999998, 147.24999999999997, 158.99999999999997])
upFreq = np.array([92.88, 104.63, 96.58, 108.33, 100.28, 112.03, 143.6, 155.35, 147.29999999999998, 159.04999999999998, 150.99999999999997, 162.74999999999997])

RSG.RSGplot(loFreq,upFreq,'Fig4',z_phot=2.25,sl_freq_obs=[107.229, 160.844],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)

