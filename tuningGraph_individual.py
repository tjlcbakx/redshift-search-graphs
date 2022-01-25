
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


orange = '#ff9500'#(1,0.584,0)
blue =  '#007aff'  #(0,.478,1) blue
green = '#4cd964'
red = '#ff3b30'
grey = '#8e8e93'   #(142./255,142./255,147./255)


# ALMA B3 \& B4 &  \\

loFreq = np.array([84.2,125])#np.array([89.625,101.55,139,150.95]) #np.array([89.618,89.618+7.75+ 3.875, 93.373, 93.373+7.75+ 3.875, 97.098, 97.098+7.75+ 3.875, 139.014, 139.014+7.75+ 3.875,  142.756, 142.756+7.75+ 3.875, 146.495, 146.495+7.75+ 3.875])
upFreq = np.array([114.9,140.5+3.75*5])#np.array([100.85,112.775,150.225,162.2]) #3.875+ np.array([89.618,89.618+7.75+ 3.875, 93.373, 93.373+7.75+ 3.875, 97.098, 97.098+7.75+ 3.875, 139.014, 139.014+7.75+ 3.875,  142.756, 142.756+7.75+ 3.875, 146.495, 146.495+7.75+ 3.875]) 


# Based on the photometric redshifts from Bakx et al. 2020.
z_herbs = np.array([2.19186859, 2.79758652, 3.68950118, 3.00452574, 3.67224612,2.08343975, 2.88648255, 2.53047932, 3.81421492, 2.39080641,2.36160175, 2.2931653 , 4.42502717, 4.04977082, 2.53546913,4.13125973, 3.13316123, 2.3795508 , 3.69238066, 1.86626077,3.52627478, 3.3827414 , 3.99953851, 2.55417985, 3.57625569,2.46946344, 4.89886738, 4.50395695, 2.6880802 , 3.25011581,3.22604547, 2.96665631, 3.11239943, 2.81692217, 2.72178991,3.43768265, 2.44590522, 3.77647762, 2.96976767, 2.94884464,4.27115722, 3.04732141, 3.94939743, 2.11996678, 1.91303853,2.46927962, 2.50622804, 2.31568987, 3.69342457, 3.45367575,2.2264977 , 4.65660711, 2.04674319, 3.76789787, 2.76520355,3.57155072, 3.10078595, 3.18320996, 2.92288049, 3.81079303,4.26121343, 2.3989643 , 2.41466162, 4.61230835, 2.73367044,2.43845409, 3.82073557, 2.19379705, 2.13303289, 2.24386634,3.29546989, 3.77100117, 2.90334917, 2.83503374, 2.38901629,2.49421993, 2.90944992, 3.42570579, 2.84975621, 2.13924181,3.30741637, 2.39342267, 4.67566701, 2.63146934, 2.75155332,3.50481908, 2.32732294, 2.89352825, 4.14979873, 3.98621298,1.96003978, 5.0961295 , 3.08676225, 2.66082447, 4.28589441,2.62855066, 2.67423963, 3.65753391, 2.59634375, 2.47594027,2.25725126, 3.60591005, 2.36000645, 1.95944828, 3.16654878,2.10909085, 2.50682954, 3.18667822, 2.32348022, 3.73948054,2.38252379, 3.70236025, 3.2406187 , 3.00140975, 2.35153775,4.30719179, 3.54916876, 3.57168274, 3.09897795, 3.54828021,3.24261403, 2.99892422, 2.38770728, 2.01236366, 3.17459574,3.22992794, 2.42104138, 2.4550749 , 4.0395271 , 2.02067151,2.88503158, 2.87131708, 3.12520377, 3.7905346 , 3.09877938,3.6669109 , 2.87604818, 2.07527395, 3.32532197, 2.46835884,2.04360009, 3.1394963 , 2.78864932, 2.45022839, 3.78356115,2.10124175, 2.56819065, 2.05691913, 2.33645675, 4.39242384,3.36807314, 3.80526693, 2.17773557, 3.31405298, 3.87342847,2.38403916, 3.21439101, 3.45789572, 2.74976995, 4.40158064,3.53196084, 3.23785403, 2.41019031, 2.82897604, 2.91388164,4.40869455, 3.62370346, 3.96261118, 2.70547747, 4.17878825,3.57781063, 2.54957505, 3.08914272, 2.28816871, 4.01362479,3.25938825, 4.7555208 , 2.58757075, 4.07211012, 2.6189511 ,2.58379855, 2.91412126, 2.92064276, 2.71343349, 3.6898582 ,3.95477604, 2.19844396, 2.96683813, 2.53070078, 2.97237641,3.66703447, 2.3223793 , 2.86341401, 2.75122254, 3.02624635,2.77075485, 2.96771817, 3.35284708, 1.97130142, 2.09816312,3.80344085, 2.07315629, 1.92196618, 4.09351606, 2.97212521,2.81690854, 2.58692162, 3.54605495, 2.87971117])

z_spt = np.array([2.351, 4.123, 3.444, 4.877, 3.090, 4.910, 3.614, 3.443, 4.233, 2.515, 3.957, 4.299, 4.803, 2.788, 4.349, 5.018, 3.233, 5.702, 5.626, 3.595, 6.901, 2.935, 4.510, 4.296, 5.655, 5.654, 2.683, 4.056, 4.225, 5.135, 3.852, 4.480, 2.011, 3.988, 4.856, 4.799, 2.233, 3.404, 3.779, 4.737, 3.368, 3.399, 2.786, 4.269, 3.128, 2.583, 3.164, 4.438, 5.323, 4.815, 2.481, 2.026, 2.727, 3.347, 2.452, 3.998, 4.090, 3.155, 4.436, 3.260, 4.768, 2.780, 4.567, 3.760, 3.851, 5.194, 2.894, 2.507, 4.280, 3.141, 5.293, 2.726, 4.756, 3.862, 2.876, 3.900, 4.302, 5.811, 5.578, 1.867, 3.070])

blendFactor = 0.13*3
scaleFactor = 20
z_herbs_smooth = np.zeros([len(z_herbs)*scaleFactor])
z_spt_smooth = np.zeros([len(z_spt)*scaleFactor])

for i in range(scaleFactor):
	z_herbs_smooth[i*len(z_herbs):(i+1)*len(z_herbs)] = z_herbs + blendFactor*np.random.normal(size=len(z_herbs))
	z_spt_smooth[i*len(z_spt):(i+1)*len(z_spt)] = z_spt + blendFactor*np.random.normal(size=len(z_spt))


fig = plt.figure(figsize=(4,3),constrained_layout=True)
fig.text(0.01,0.5,'Robust redshift coverage [0 - 1]',rotation=90,fontsize=12,verticalalignment='center')
fig.text(0.525,0.02,'Redshift',fontsize=12,horizontalalignment='center')
f_ax1 = plt.axes([0.15,0.15,0.8,0.8])

threshold_high = 5
threshold_low = 5
dz_low = 0.07
dz_high = 0.13

for i in range(10):
	# Generate a redshift distribution between z and z + 1
	redshiftDistribution = np.linspace(i,i+1,100)
	print('loFreq')
	# A variable to get the graph to look as I want
	iOffset = 0
	# Generate three 'tuningQualities' for 1) typical observations, 2) including CI & H2O, and 3) reduced dz/(1+z) or sigma_threshold
	tuningQuality = RSG.RSGquality(loFreq,upFreq,redshiftDistribution,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000)
	tuningQuality_withCI_lines = RSG.RSGquality(loFreq,upFreq,redshiftDistribution,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000,includeCI=True)
	tuningQuality_with_lower_sigma = RSG.RSGquality(loFreq,upFreq,redshiftDistribution,sigma_threshold=threshold_low,dzUncertainty=dz_low,lin_arr_size=1000)
	if i == 8:
		tuningQuality = RSG.RSGquality(loFreq,upFreq,z_herbs_smooth,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000)
		tuningQuality_withCI_lines = RSG.RSGquality(loFreq,upFreq,z_herbs_smooth,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000,includeCI=True)
		tuningQuality_with_lower_sigma = RSG.RSGquality(loFreq,upFreq,z_herbs_smooth,sigma_threshold=threshold_low,dzUncertainty=dz_low,lin_arr_size=1000)
		iOffset= 0.33
	elif i == 9:
		tuningQuality = RSG.RSGquality(loFreq,upFreq,z_spt_smooth,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000)
		tuningQuality_withCI_lines = RSG.RSGquality(loFreq,upFreq,z_spt_smooth,sigma_threshold=threshold_high,dzUncertainty=dz_high,lin_arr_size=1000,includeCI=True)
		tuningQuality_with_lower_sigma = RSG.RSGquality(loFreq,upFreq,z_spt_smooth,sigma_threshold=threshold_low,dzUncertainty=dz_low,lin_arr_size=1000)
		iOffset = 0.66
	# Define NoDetections, Non-robust detections, robust detections, CI-based robust detections and lower SN or dz/(1+z) robust detections.
	NoDetections = tuningQuality[0]
	NonRobustDetections = tuningQuality[1]
	RobustDetections = tuningQuality[2] + tuningQuality[3]
	CI_detections = tuningQuality_withCI_lines[2] + tuningQuality_withCI_lines[3] - tuningQuality_withCI_lines[5] + tuningQuality_withCI_lines[4]
	lowerSN_detections = tuningQuality_with_lower_sigma[2] + tuningQuality_with_lower_sigma[3] - tuningQuality_with_lower_sigma[5] + tuningQuality_with_lower_sigma[4]
	f_ax1.bar(i+iOffset+0.5,NonRobustDetections+RobustDetections,zorder=1,color='#FFD79F',width=1.0)
	f_ax1.bar(i+iOffset+0.5,RobustDetections,zorder=2,color='#9DDBFF',width=1.0)
	f_ax1.bar(i+iOffset+0.5,tuningQuality[4],bottom=RobustDetections,hatch='////',lw=0.0,edgecolor='#9DDBFF',fill=False,width=1.0,zorder=4)
	f_ax1.bar(i+iOffset+0.5,-1*tuningQuality[5],bottom=RobustDetections,hatch='\\\\\\\\',lw=0.0,edgecolor='#FFD79F',fill=False,width=1.0,zorder=4)
	# Plot a grey line for CI detections
	f_ax1.step([i+iOffset,i+iOffset+1],[CI_detections,CI_detections],lw=1,color=grey,zorder=5,ls=':')
	# Plot a black dashed line for lower-SN or dz/(1+z) detections
	f_ax1.step([i+iOffset,i+iOffset+1],[lowerSN_detections,lowerSN_detections],lw=1,color='k',zorder=5,ls='--')
	# Add text to describe the source
	f_ax1.text(0.5,0.04,'Band 3 & 4 linescan',zorder=30)
	# Print the 'tuningQuality'; repeat for the other 8 assessments
	print(tuningQuality)

f_ax1.axvline(8,lw=0.75,ls='--',color='k')

# Complicated formatting things to make a nice graph
from matplotlib.ticker import NullFormatter
nullfmt = NullFormatter()
f_ax1.get_xaxis().set_ticks([])
f_ax1.get_yaxis().set_ticks([]) 

f_ax1.set_yticks([0,0.25,0.5,0.75,1.0])
f_ax1.set_yticklabels(['0','0.25','0.5','0.75','1'])

f_ax1.set_xticks([0,2,4,6,8,7.5+1+ 0.33, 1+8.5+0.66 ])
f_ax1.set_xticklabels(['0','2','4','6','','HerBS   ','   SPT'])

f_ax1.set_xlim(0,11)
f_ax1.set_ylim(0,1.0)

# Save & show individual file
plt.savefig('RedshiftSearchEfficiency_individual.pdf')

plt.show()