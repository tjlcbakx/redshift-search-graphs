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

# RSG.makeSLED([1,2,3,4,6,7],[0.18,0.51,-99,2.06,2.40,-99],[0.05,0.12,0.49,0.53,0.58,1.69])
# plt.show()
RSG.makeSLED([3,4],[-99,1],[1/8,1/8])
plt.savefig('Fig5_nondetected_lower_redshift_solution.png',dpi=400)
# plt.show()
plt.close()

RSG.makeSLED([4,6],[-99,1],[1/8,1/8])#,ylimMultiplier=2)
plt.savefig('Fig5_nondetected_upper_redshift_solution.png',dpi=400)
# plt.close()

# plt.show()