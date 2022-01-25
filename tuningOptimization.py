##-----------------------------------------
## Code written and edited by Tom Bakx
## tjlcbakx@gmail.com
##-----------------------------------------


##-----------------------------------------
## Header imports, colours
##-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
from random import random
import glob
import RSG
from tqdm import tqdm


orange = '#ff9500'#(1,0.584,0)
blue =  '#007aff'  #(0,.478,1) blue
green = '#4cd964'
red = '#ff3b30'
grey = '#8e8e93'   #(142./255,142./255,147./255)

# Based on the photometric redshifts from Bakx et al. 2020.
z_herbs = np.array([2.19186859, 2.79758652, 3.68950118, 3.00452574, 3.67224612,2.08343975, 2.88648255, 2.53047932, 3.81421492, 2.39080641,2.36160175, 2.2931653 , 4.42502717, 4.04977082, 2.53546913,4.13125973, 3.13316123, 2.3795508 , 3.69238066, 1.86626077,3.52627478, 3.3827414 , 3.99953851, 2.55417985, 3.57625569,2.46946344, 4.89886738, 4.50395695, 2.6880802 , 3.25011581,3.22604547, 2.96665631, 3.11239943, 2.81692217, 2.72178991,3.43768265, 2.44590522, 3.77647762, 2.96976767, 2.94884464,4.27115722, 3.04732141, 3.94939743, 2.11996678, 1.91303853,2.46927962, 2.50622804, 2.31568987, 3.69342457, 3.45367575,2.2264977 , 4.65660711, 2.04674319, 3.76789787, 2.76520355,3.57155072, 3.10078595, 3.18320996, 2.92288049, 3.81079303,4.26121343, 2.3989643 , 2.41466162, 4.61230835, 2.73367044,2.43845409, 3.82073557, 2.19379705, 2.13303289, 2.24386634,3.29546989, 3.77100117, 2.90334917, 2.83503374, 2.38901629,2.49421993, 2.90944992, 3.42570579, 2.84975621, 2.13924181,3.30741637, 2.39342267, 4.67566701, 2.63146934, 2.75155332,3.50481908, 2.32732294, 2.89352825, 4.14979873, 3.98621298,1.96003978, 5.0961295 , 3.08676225, 2.66082447, 4.28589441,2.62855066, 2.67423963, 3.65753391, 2.59634375, 2.47594027,2.25725126, 3.60591005, 2.36000645, 1.95944828, 3.16654878,2.10909085, 2.50682954, 3.18667822, 2.32348022, 3.73948054,2.38252379, 3.70236025, 3.2406187 , 3.00140975, 2.35153775,4.30719179, 3.54916876, 3.57168274, 3.09897795, 3.54828021,3.24261403, 2.99892422, 2.38770728, 2.01236366, 3.17459574,3.22992794, 2.42104138, 2.4550749 , 4.0395271 , 2.02067151,2.88503158, 2.87131708, 3.12520377, 3.7905346 , 3.09877938,3.6669109 , 2.87604818, 2.07527395, 3.32532197, 2.46835884,2.04360009, 3.1394963 , 2.78864932, 2.45022839, 3.78356115,2.10124175, 2.56819065, 2.05691913, 2.33645675, 4.39242384,3.36807314, 3.80526693, 2.17773557, 3.31405298, 3.87342847,2.38403916, 3.21439101, 3.45789572, 2.74976995, 4.40158064,3.53196084, 3.23785403, 2.41019031, 2.82897604, 2.91388164,4.40869455, 3.62370346, 3.96261118, 2.70547747, 4.17878825,3.57781063, 2.54957505, 3.08914272, 2.28816871, 4.01362479,3.25938825, 4.7555208 , 2.58757075, 4.07211012, 2.6189511 ,2.58379855, 2.91412126, 2.92064276, 2.71343349, 3.6898582 ,3.95477604, 2.19844396, 2.96683813, 2.53070078, 2.97237641,3.66703447, 2.3223793 , 2.86341401, 2.75122254, 3.02624635,2.77075485, 2.96771817, 3.35284708, 1.97130142, 2.09816312,3.80344085, 2.07315629, 1.92196618, 4.09351606, 2.97212521,2.81690854, 2.58692162, 3.54605495, 2.87971117])

blendFactor = 0.13*3
scaleFactor = 20
z_herbs_smooth = np.zeros([len(z_herbs)*scaleFactor])

for i in range(scaleFactor):
	z_herbs_smooth[i*len(z_herbs):(i+1)*len(z_herbs)] = z_herbs + blendFactor*np.random.normal(size=len(z_herbs))



lower_tuning3 = RSG.giveALMA(3,0)
upper_tuning3 = RSG.giveALMA(3,1)
lower_tuning4 = RSG.giveALMA(4,0)
upper_tuning4 = RSG.giveALMA(4,1)

# We will want to generate two ladders,
# so we calculate the dynamic range
# leaving 3.75 x 2 at the top-frequency part
dFreq3 = upper_tuning3[0][0]-lower_tuning3[0][0]
dynamicRange3 = 1 - (3.75 * 2 / dFreq3)
dFreq4 = upper_tuning4[0][0]-lower_tuning4[0][0]
dynamicRange4 = 1 - (3.75 * 2 / dFreq4)

nrOfIterations = 100
robustFraction = 0
qualityArray = np.zeros([nrOfIterations,nrOfIterations])
multipleLines = np.zeros([nrOfIterations,nrOfIterations])

overlapFraction = 0.05
# print('(no_lines,one_line,two_lines,more_lines,robust_single_lines,non_robust_double_lines)')

for i in (range(nrOfIterations)):
	print(i)
	tuning3 = RSG.giveALMA(3,dynamicRange3*i/nrOfIterations)
	tuning3[0].append(tuning3[0][-2]+3.75-overlapFraction)
	tuning3[0].append(tuning3[0][-2]+3.75-overlapFraction)
	tuning3[0].append(tuning3[0][-2]+3.75-overlapFraction)
	tuning3[0].append(tuning3[0][-2]+3.75-overlapFraction)
	tuning3[1].append(tuning3[1][-2]+3.75-overlapFraction)
	tuning3[1].append(tuning3[1][-2]+3.75-overlapFraction)
	tuning3[1].append(tuning3[1][-2]+3.75-overlapFraction)
	tuning3[1].append(tuning3[1][-2]+3.75-overlapFraction)
	for j in range(nrOfIterations):
		tuning4 = RSG.giveALMA(4,dynamicRange4*j/nrOfIterations)
		tuning4[0].append(tuning4[0][-2]+3.75-overlapFraction)
		tuning4[0].append(tuning4[0][-2]+3.75-overlapFraction)
		tuning4[0].append(tuning4[0][-2]+3.75-overlapFraction)
		tuning4[0].append(tuning4[0][-2]+3.75-overlapFraction)
		tuning4[1].append(tuning4[1][-2]+3.75-overlapFraction)
		tuning4[1].append(tuning4[1][-2]+3.75-overlapFraction)
		tuning4[1].append(tuning4[1][-2]+3.75-overlapFraction)
		tuning4[1].append(tuning4[1][-2]+3.75-overlapFraction)
		loFreq = [item for sublist in [tuning3[0],tuning4[0]] for item in sublist]
		upFreq = [item for sublist in [tuning3[1],tuning4[1]] for item in sublist]
		tuningQuality = RSG.RSGquality(loFreq,upFreq,z_herbs_smooth,sigma_threshold=5,dzUncertainty=0.07,lin_arr_size=1000,includeCI=False)
		robustness = tuningQuality[2] + tuningQuality[3] - tuningQuality[5]*0.5 + tuningQuality[4] + (tuningQuality[1]-tuningQuality[4])*0.5
		qualityArray[i,j] = robustness
		multipleLines[i,j] = tuningQuality[2] + tuningQuality[3]
		if robustness > robustFraction:
			robustFraction = robustness
			loFreqSave = loFreq
			upFreqSave = upFreq
			print(str(np.round(robustness*100,1))+'% robust + 0.5 x non-robust')
			print(loFreq)
			print(upFreq)


plt.figure(figsize=(4.2,3.5))



c = plt.imshow(qualityArray.transpose(), cmap ='coolwarm', #vmin = qualityArray.min(), vmax = qualityArray.max(),
                 extent =[lower_tuning3[0][0], upper_tuning3[0][0]-3.75*2 ,lower_tuning4[0][0], upper_tuning4[0][0]-3.75*2], 
                 aspect='auto',interpolation ='nearest', origin ='lower')

# plt.contour(multipleLines.transpose(),extent =[lower_tuning3[0][0], upper_tuning3[0][0]-3.75*2 ,lower_tuning4[0][0], upper_tuning4[0][0]-3.75*2],
#	 colors=grey,levels=np.linspace(0,1,int(1/0.05)+1))

cbar = plt.colorbar(c)
cbar.set_ticks([0.85,0.9])
cbar.set_ticklabels(["0.85", "0.90"])
# cbar.set_label('Figure of merit')



plt.scatter(loFreqSave[0],loFreqSave[6],marker='X',color='k',s=40,zorder=200)
plt.scatter(loFreqSave[0],loFreqSave[6],marker='X',color=plt.get_cmap('coolwarm')(255),s=10,zorder=200)

plt.ylabel('Band 4 Frequency [GHz]',fontsize=14)
plt.xlabel('Band 3 Frequency [GHz]',fontsize=14)
plt.yticks([125,130,135,140])
plt.xticks([84,87,90,93])
plt.tight_layout()

plt.savefig('band34_tuning.pdf')
plt.show()
















