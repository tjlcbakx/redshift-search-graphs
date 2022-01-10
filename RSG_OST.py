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



loFreq = (1e-9)*(3e8)/(np.array([589,589])*1e-6)
upFreq = (1e-9)*(3e8)/(np.array([336,336])*1e-6)

RSG.RSGplot(loFreq,upFreq,'RSG_OST.png',z_phot=3.0,sl_freq_obs=[93.463,155.772],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)