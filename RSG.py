##-----------------------------------------
## Code written and edited by Tom Bakx
## tjlcbakx@gmail.com
##-----------------------------------------


##-----------------------------------------
## Header imports, colours
##-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt


orange = '#ff9500'#(1,0.584,0)
blue =  '#007aff'  #(0,.478,1) blue
green = '#4cd964'
red = '#ff3b30'
grey = '#8e8e93'   #(142./255,142./255,147./255)


##-----------------------------------------
## Spectral lines
##-----------------------------------------

c = 299792458 #m/s
# all freq. in GHz
CO10 = 115.27120180
HCN10 = 88.63393600
H2O211 = 752.03314300
H2O202 = 987.92675900
SIII33 =  (1e-9)*c/(33.48e-6) # SIII
SiII34 	= (1e-9)*c/(34.82e-6)
OIII52 	= (1e-9)*c/(51.81e-6)
NIII57 	= (1e-9)*c/(57.32e-6)
OI63 	= (1e-9)*c/(63.18e-6)
OIII88 	= (1e-9)*c/(88.36e-6)
NII121 	= (1e-9)*c/(121.9e-6)
OI145 	= (1e-9)*c/(145.5e-6)
CII157 	= (1e-9)*c/(157.7e-6)
CI370 	= (1e-9)*c/(370.5e-6)
CI609 	= (1e-9)*c/(609.6e-6)
NII205 	= (1e-9)*c/(205e-6)  

##-----------------------------------------
## RSG plot
##-----------------------------------------

def RSGplot(filter_down,filter_up,IDname,z_phot=-99,sl_freq_obs=[-99],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,single_line_colour='#FFD79F',multi_line_colour='#9DDBFF',LSBUSB=False,DPIVal=400,nr_of_CO_lines = 20,dzUncertainty=0.13):
    sl_freq_obs.sort(reverse=True)
    dz_phot = (z_phot+1)*dzUncertainty
    ##-----------------------------------------
    ## Define your redshift, frequency, SL
    ##-----------------------------------------
    # Create a redshift array:
    data_size = 10000
    redshift_array = np.linspace(redshift_down,redshift_up,data_size)
    # CI and H2O, yes or no?
    SL_rest_freq = []
    for i in range(nr_of_CO_lines):
        SL_rest_freq.append((i+1)*CO10)
    #OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205
    #CI370 ,CI609 ,H2O211,H2O202
    for i in [OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205,CI370 ,CI609 ,H2O211,H2O202]:
        SL_rest_freq.append(i)
    # Create an array of the freq. of each SL at each redshift
    # SL[5,200] = the frequency of line 6 at redshift redshift_array[200]
    SL_array = np.zeros([len(SL_rest_freq),data_size])
    for q in range(data_size):
        for j in range(len(SL_rest_freq)):
            SL_array[j,q] = SL_rest_freq[j]/(1+redshift_array[q])
    ##-----------------------------------------
    ## Give the bandpass and SL's covered
    ##-----------------------------------------
    filter_down = np.array(filter_down)
    filter_up = np.array(filter_up)
    frequency_down = filter_down.min() * 0.85
    frequency_up = filter_up.max() + filter_down.min() * 0.15
    frequency_diff = filter_down.min() * 0.15
    # Mark which spectral lines are visible at which redshift
    # SL_vis[6,200] = 1 if SL 6 is visible at redshift redshift_array[200]
    SL_vis = np.zeros([len(SL_rest_freq),data_size])
    for q in range(len(filter_down)):
        SL_vis[(SL_array>filter_down[q])&(SL_array<filter_up[q])]=1
    ##-----------------------------------------
    ## Plot coverage
    ##-----------------------------------------
    plt.figure(figsize = (figSizeX,figSizeY))
    f1 = plt.axes([.125,.125,.8,.8])
    # Plot all the lines
    for i in range(len(SL_rest_freq)):
        if i < nr_of_CO_lines:
            f1.plot(redshift_array,SL_array[i,:],color='k')
        else:
            f1.plot(redshift_array,SL_array[i,:],color=blue,linestyle='--')
    # plot the bands in the left-hand of the figure
    if LSBUSB: 
        f1.set_xlim([redshift_down-0.15 - 0.06*0.5*len(filter_down),redshift_up])
        from matplotlib.pyplot import cm
        colorpicker=cm.magma(np.linspace(0.2,0.8,int(0.5*len(filter_down))))
        for i in range(len(filter_down)):
            f1.plot([redshift_down-0.1- np.floor(i*0.5)*0.06,redshift_down-0.1 - np.floor(i*0.5)*0.06],[filter_down[i],filter_up[i]],color=colorpicker[int(i*0.5)],linewidth=2)
    else:
        f1.set_xlim([redshift_down-0.15 - 0.06*len(filter_down),redshift_up])
        from matplotlib.pyplot import cm
        colorpicker=cm.magma(np.linspace(0.2,0.8,int(len(filter_down))))
        for i in range(len(filter_down)):
            f1.plot([redshift_down-0.1- i*0.06,redshift_down-0.1 - i*0.06],[filter_down[i],filter_up[i]],color=colorpicker[i],linewidth=2)
    # Plot the redshift uncertainty
    f1.errorbar(z_phot,frequency_down + 0.5*frequency_diff ,  xerr=dz_phot,marker='o',color='k',zorder=100)
    # Fill in the coverage, where we detect 1 line SL_vis[:28,:].sum(axis=0)>0 and for more than 1 line: SL_vis[:28,:].sum(axis=0)>1
    for i in range(len(filter_down)):
        f1.fill_between(redshift_array, filter_down[i], filter_up[i], where=SL_vis[:28,:].sum(axis=0)>0 , facecolor=single_line_colour, interpolate=True)
        f1.fill_between(redshift_array, filter_down[i], filter_up[i], where=SL_vis[:28,:].sum(axis=0)>1 , facecolor=multi_line_colour, interpolate=True)
    # make the plot a bit cleaner by fading out the lines on the top and bottom
    f1.fill_between(redshift_array,frequency_down,filter_down.min(),facecolor='w',alpha=0.7,zorder=10)
    f1.fill_between(redshift_array,frequency_up,filter_up.max(),facecolor='w',alpha=0.7,zorder=10)
    # Pretend the y-axis is only up until redshift_down ;)
    f1.axvline(redshift_down,ymin=0,ymax=frequency_up*1.1,color='k',linewidth=0.7,zorder=12)
    f1.set_ylim([frequency_down,frequency_up])
    # set the labels and the title
    f1.set_xlabel('Redshift')
    f1.set_ylabel('Frequency [GHz]')
    f1.set_xticks(np.arange(np.floor(redshift_down), np.ceil(redshift_up)+1, 1.0))
    ##-----------------------------------------
    ## Plot lines at the correct frequency
    ##-----------------------------------------
    # Horizontal line for the frequency
    for i in range(len(sl_freq_obs)):
        f1.axhline(sl_freq_obs[i],linewidth=0.5,color=grey)
    # Plot a little ball on the cross between horizontal and spectral line lines
    for line_choice in range(len(sl_freq_obs)):
        # if the associated redshift is within the redshift regime, plot the line
        for co_choice in range(SL_array.shape[0]):
            if ((SL_rest_freq[co_choice]/sl_freq_obs[line_choice]) - 1 > redshift_down) and ((SL_rest_freq[co_choice]/sl_freq_obs[line_choice]) - 1 < redshift_up):
                z_index = np.argmin(abs(SL_array[co_choice,:] - sl_freq_obs[line_choice]))
                if SL_vis[:28,:].sum(axis=0)[z_index] == 1:
                    f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],color = single_line_colour,linewidth=1,zorder=200,s=30)
                    f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],color = 'k',linewidth=1,zorder=150,s=40)
                elif SL_vis[:28,:].sum(axis=0)[z_index] > 1:
                    f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],color = multi_line_colour,linewidth=1,zorder=200,s=30)
                    f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],color = 'k',linewidth=1,zorder=150,s=40)
                else:
                    #f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],color = 'w',linewidth=1,zorder=200,s=30)
                    f1.scatter(redshift_array[z_index],sl_freq_obs[line_choice],edgecolor = 'k',color='none',linewidth=0.3,zorder=150,s=40)
    for line_choice in range(len(sl_freq_obs)):
        # if the associated redshift is within the redshift regime, plot the line
        for co_choice in range(SL_array.shape[0]):
            if ((SL_rest_freq[co_choice]/sl_freq_obs[line_choice]) - 1 > redshift_down) and ((SL_rest_freq[co_choice]/sl_freq_obs[line_choice]) - 1 < redshift_up):
                z_index = np.argmin(abs(SL_array[co_choice,:] - sl_freq_obs[line_choice]))
                f1.plot([redshift_array[z_index],redshift_array[z_index]],[sl_freq_obs[line_choice],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff], color='k',lw=0.2,zorder=12,linestyle=':')
                if SL_vis.sum(axis=0)[z_index] == 1:
                    f1.arrow(redshift_array[z_index],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff, 0,-0.3 * frequency_diff,shape='full', lw=0.5, length_includes_head=True, head_width=0.1,overhang=5,zorder=300)
                else:
                    f1.arrow(redshift_array[z_index],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff, 0,-0.3 * frequency_diff,shape='full', lw=0.5, length_includes_head=True, head_width=0.1,overhang=5,zorder=300)
    plt.savefig('RSG_'+str(IDname)+'.png',dpi=DPIVal)




def giveALMA(band, lower_freq_ratio):
	### lower-freq runs from 0 to 1,
	### where 0 has the lowest possible lower_freq
	### and 1 has the highest possible lower_freq
	### This function returns the lower and upper freq
	### of both the lower and upper sideband
	### eg: giveALMA(3,0) = ([84.0, 95.75], [87.75, 99.5])
	### eg: giveALMA(3,1) = ([100.5, 112.25], [104.25, 116.0])
	if band == 3:
		df = 116 - 84 - 15.5
		f0 = 84
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 4:
		df = 163 - 125 - 15.5
		f0 = 125
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 5:
		df = 211-158 - 15.5
		f0 = 158
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 6:
		df = 275 - 211 - 15.5
		f0 = 211
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 7:
		df = 373-275 - 15.5
		f0 = 275
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 8:
		df = 500 - 385 - 15.5
		f0 = 385
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 9:
		df = 602 - 720 - 15.5
		f0 = 602
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	elif band == 10:
		df = 950 - 787 - 15.5
		f0 = 787
		low_arr = [f0 + df*lower_freq_ratio, f0 + df*lower_freq_ratio + 11.75]
		upp_arr = [f0 + df*lower_freq_ratio+3.75, f0 + df*lower_freq_ratio + 11.75 + 3.75]
	else:
		low_arr = [0,0]
		upp_arr = [0,0]
		print('Warning: band '+str(band)+' not between 3 and 8')
	return low_arr, upp_arr


def tauCalculator(PWV,printTau='False'):
    '''
    This program provides the Tau for different Percipable Water Vapours, and linearly interpolates
    between the values 0.5, 1, 2, 6. Outside of these extremes, we take the values 0.5 and 6, respectively.
    '''
    import numpy as np
    if 'trans' not in globals():
        global trans
        trans = np.loadtxt('./pgplot.csv', dtype=np.float, delimiter=",", unpack = False)
    PWVARRAY = np.array([0.3, 0.5, 0.75, 1., 1.5, 2., 2.5, 3., 4., 5.])
    a = np.argmin(abs(PWVARRAY - PWV))
    if printTau == True:
        print('PWV  = ' + str(PWVARRAY[a]))
    outputArray = np.zeros([8301,2])
    outputArray[:,1] = trans[:,1+a]
    outputArray[:,0] = trans[:,0]
    return outputArray



def giveMultiFactors(a,b):
    multiFac = 1
    for i in range(2,max(a,b)):
        if (a%i == 0) and (b%i == 0):
            multiFac = i
    if multiFac == 1:
        return min(a,b)
    else:
        return min(a,b)*(multiFac-1)/multiFac- min(a,b)


def RSGquality(filter_down,filter_up,redshift_array,includeCI = False, nr_of_CO_lines=20,lin_arr_size=10000,sigma_threshold=5,dzUncertainty=0.13):
    # We split the redshift spacing up into a linear array (redshift_lin), and then do a
    # nearest fit of the redshift array supplied by the user (redshift_array)
    # We ensure the redshift array is wide enough using, also to exclude redshifts:
    redshift_lin = np.linspace(0,1.5*redshift_array.max(),lin_arr_size)
    # Each of the look-up tables:
    redshift_lin_seen = np.zeros([lin_arr_size])
    # Our code assumes robust until told otherwise. For this array, 1 is robust, 0 is degenerate
    redshift_lin_seen_one = np.ones([lin_arr_size])
    redshift_lin_seen_two = np.ones([lin_arr_size])
    # The arrays where we place the look-up values of the user-provided z-arrays
    redshift_array_seen = np.zeros([len(redshift_array)])
    redshift_array_seen_one = np.zeros([len(redshift_array)])
    redshift_array_seen_two = np.zeros([len(redshift_array)])
    # Transform the bandwidths into arrays
    filter_down = np.array(filter_down)
    filter_up = np.array(filter_up)
    # Create a line table we can use for redshift searches
    SL_rest_freq = []
    # Add CO lines
    for i in range(nr_of_CO_lines):
        SL_rest_freq.append((i+1)*CO10)
    # OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205
    # CI370 ,CI609 ,H2O211,H2O202 , 
    # Optionally add additional lines.
    # We recommend not including CI lines, unless the survey is sufficiently deep
    if includeCI:
        for i in [OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205,CI370,CI609]:
            SL_rest_freq.append(i)
    else:
        for i in [OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205]:
            SL_rest_freq.append(i)
    # Create an array for increased computing speed
    SL_rest_freq = np.array(SL_rest_freq)
    # Generate basic coverage of number of lines per redshift region
    for i in range(len(redshift_lin)):
        # Transform the spectral lines to observed freq.
        freq_lines = SL_rest_freq/(1+redshift_lin[i])
        # Create a table of lines, so we don't double-count when bandwidths overlap
        freq_seen = np.zeros([len(freq_lines)])
        # Loop over the available bandwidths
        for j in range(len(filter_down)):
            freq_seen[(freq_lines > filter_down[j]) & (freq_lines < filter_up[j])] = 1
        # The number of lines seen is equal to the sum of the above
        redshift_lin_seen[i] = freq_seen.sum()
    # In the following, we test the robustness of individual lines, and the
    # degeneracy in two-line detections
    for i in range(len(redshift_lin)):
        # Select only single-line solutions
        if redshift_lin_seen[i] == 1:
            # Recreate the number of lines within our bandwidth
            freq_lines = SL_rest_freq/(1+redshift_lin[i])
            freq_seen = np.zeros([len(freq_lines)])
            for j in range(len(filter_down)):
                freq_seen[(freq_lines > filter_down[j]) & (freq_lines < filter_up[j])] = 1
            # Calculate what line was seen
            Jco = np.argmax(freq_seen)+1
            # If it is not a CO line, we consider the line robust given the larger redshift difference between different line solutions
            if Jco > nr_of_CO_lines:
                redshift_lin_seen_one[i] = 2
            else:
                # Using eq. 1 from Bakx&Dannerbauer, we calculate the dz from a change
                # in CO(J, J-1) to CO(J-1, J-2)
                dz = 1*(1+redshift_lin[i])/Jco
                # We can test the robustness by looking up to dz/(1+z) = 13% 
                # CO solutions 'far', and testing their robustness
                for l in range(nr_of_CO_lines):
                    #
                    if (l+1) == Jco:
                        # do nothing
                        1+1
                    elif abs((l+1 - Jco)*dz/(1+redshift_lin[i])) > sigma_threshold*dzUncertainty: #0.13
                        # do nothing
                        1+1
                    else:
                        k = abs(l+1 - Jco)
                        # We look up the associated index with +(k+1) * dz
                        SecondSolutionIndex_up = np.argmin(abs(redshift_lin[i] - redshift_lin + dz*(k+1)))
                        # Check if the line would be within our expected redshift window
                        if (SecondSolutionIndex_up > -1) & (SecondSolutionIndex_up < lin_arr_size):
                            # If our (k+1) * dz solution would find more than one line, we can call
                            # those solutions 'excludable'. We don't want to override any
                            # past decisions towards non-robustness though.
                            if (redshift_lin_seen[SecondSolutionIndex_up] > 1) and (redshift_lin_seen_one[i] != 0):
                                # do nothing
                                1+1
                            elif redshift_lin[SecondSolutionIndex_up] < 1:
                                # do nothing
                                1+1
                            else:
                                # Since 0 lines are excluded, we have a degenerate solution within (k+1) * dz
                                redshift_lin_seen_one[i] = 0
                        # same as above, but then for -(k+1) * dz
                        SecondSolutionIndex_down = np.argmin(abs(redshift_lin[i] - redshift_lin - dz*(k+1)))
                        if (SecondSolutionIndex_down > -1) & (SecondSolutionIndex_down < lin_arr_size):
                            if (redshift_lin_seen[SecondSolutionIndex_down] > 1) and (redshift_lin_seen_one[i] != 0):
                                1+1
                            elif redshift_lin[SecondSolutionIndex_down] < 1:
                                # do nothing
                                1+1
                            else:
                                redshift_lin_seen_one[i] = 0
        # We test the case where only two lines are detected.
        # The number of greatest common dividers drops fast with more than 2 lines
        # So we exclude this as a significant component towards degenerate solutions
        if redshift_lin_seen[i] == 2:
            # Observed frequencies
            freq_lines = SL_rest_freq/(1+redshift_lin[i])
            freq_seen = np.zeros([len(freq_lines)])
            for j in range(len(filter_down)):
                freq_seen[(freq_lines > filter_down[j]) & (freq_lines < filter_up[j])] = 1
            # In case any of the two lines consists of a non CO-detection, we call it robust
            if freq_seen[nr_of_CO_lines:].sum() > 0:
                redshift_lin_seen_two[i] == 2
            else:
                # Give the CO transitions detected
                # First, an array of CO indices
                CO_trans = np.arange(1,len(freq_seen) + 1)
                # Filtering to get the CO solutions
                CO_obs = CO_trans[freq_seen == 1]
                # Use the above script to get the nearest CO degeneracy
                J_other = giveMultiFactors(CO_obs[0],CO_obs[1])
                Jco = min(CO_obs)
                dz = (1+redshift_lin[i])/Jco
                # Test if this solution is already X sigma away
                if abs(J_other*dz/(1+redshift_lin[i])) > dzUncertainty*sigma_threshold:
                    redshift_lin_seen_two == 1
                # Otherwise, we check degeneracy of the neighbouring solution
                else:
                    # The offset to the next solution is J_other plus/minus the lowest transion
                    for k in [J_other]:
                        SecondSolutionIndex_up = np.argmin(abs(redshift_lin[i] - redshift_lin + dz*(k+1)))
                        if (SecondSolutionIndex_up > -1) & (SecondSolutionIndex_up < lin_arr_size):
                            # If we detect more / less than 2 lines, it is robust
                            if (redshift_lin_seen[SecondSolutionIndex_up] != 2) and (redshift_lin_seen_two[i] != 0):
                                1+1
                            elif redshift_lin[SecondSolutionIndex_up] < 1:
                                # do nothing
                                1+1
                            else:
                                # If we detect exactly two lines, it is degenerate
                                redshift_lin_seen_two[i] = 0
                        # Same as above for -(1+k) *dz
                        SecondSolutionIndex_down = np.argmin(abs(redshift_lin[i] - redshift_lin - dz*(k+1)))
                        if (SecondSolutionIndex_down > -1) & (SecondSolutionIndex_down < lin_arr_size):
                            if (redshift_lin_seen[SecondSolutionIndex_down] != 2) and (redshift_lin_seen_two[i] != 0):
                                1+1
                            elif redshift_lin[SecondSolutionIndex_down] < 1:
                                # do nothing
                                1+1
                            else:
                                redshift_lin_seen_two[i] = 0
    for i in range(len(redshift_array)):
        redshift_array_seen[i] = redshift_lin_seen[np.argmin(abs(redshift_array[i] - redshift_lin))]
        if redshift_array_seen[i] == 1:
            redshift_array_seen_one[i] = redshift_lin_seen_one[np.argmin(abs(redshift_array[i] - redshift_lin))]
        if redshift_array_seen[i] == 2:
            redshift_array_seen_two[i] = redshift_lin_seen_two[np.argmin(abs(redshift_array[i] - redshift_lin))]
    no_lines = (redshift_array_seen == 0).sum()/len(redshift_array)
    one_line = (redshift_array_seen == 1).sum()/len(redshift_array)
    two_lines = (redshift_array_seen == 2).sum()/len(redshift_array)
    more_lines = (redshift_array_seen > 2).sum()/len(redshift_array)
    robust_single_lines = (redshift_array_seen_one[redshift_array_seen == 1]>0).sum()/len(redshift_array)
    non_robust_double_lines = (redshift_array_seen_two[redshift_array_seen == 2]==0).sum()/len(redshift_array)
    return np.array([no_lines,one_line,two_lines,more_lines,robust_single_lines,non_robust_double_lines])


def makeSLED(coTransitions, coIntFluxes, coIntErrors,figSizeX=4,figSizeY=4,ylimMultiplier=1.4):
    coTransitions = np.array(coTransitions); coIntFluxes = np.array(coIntFluxes); coIntErrors = np.array(coIntErrors);    
    plt.figure(figsize = (figSizeX,figSizeY))
    f1 = plt.axes([.175,.125,.8,.8])
    # Load the CO SLEDS
    fixsen_mw_indisk_co=    np.array([1,2,3,4,5,6,7,8])
    fixsen_mw_indisk_ico=   np.array([0.5,1.15,1.267,0.85,0.58,0.08333,0.04286,0.225])/0.5
    fixsen_mw_indisk_ico_err=   np.array([0.3,0.1,0.1,0.075,0.12,0.1167,0.1429,0.1])/0.5
    coLinear = np.arange(1,coTransitions.max()+2)
    thermalizedCO = coLinear**2
    harrington_co = np.arange(1,13)
    harrington_ico = np.array([1, 0.73,0.75,0.46,0.36,0.28,0.18,0.08,0.07,0.07,0.05,0.02])*harrington_co**2
    harrington_ico_err = np.array([0,0.10, 0.11, 0.07, 0.06, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02, 0.01])*harrington_co**2
    # Normalize all observations to the thermalized profile
    lowestDetectedCOTransition = coTransitions[coIntFluxes>0][0]
    if lowestDetectedCOTransition > 8:
        print('Cannot reflect the milky way accurately')
        normalizeMilkyWay = fixsen_mw_indisk_ico[8 - 1]/thermalizedCO[8 - 1]
        if lowestDetectedCOTransition > 11:
            print('Cannot reflect Harrington profile accurately')
            normalizeHarrington = harrington_ico[11 - 1]/thermalizedCO[11 - 1]
        else:
            normalizeHarrington = harrington_ico[lowestDetectedCOTransition - 1]/thermalizedCO[lowestDetectedCOTransition - 1]
    else:
        normalizeHarrington = harrington_ico[lowestDetectedCOTransition - 1]/thermalizedCO[lowestDetectedCOTransition - 1]
        normalizeMilkyWay = fixsen_mw_indisk_ico[lowestDetectedCOTransition - 1]/thermalizedCO[lowestDetectedCOTransition - 1]
    harrington_ico = harrington_ico /normalizeHarrington
    harrington_ico_err = harrington_ico_err /normalizeHarrington
    fixsen_mw_indisk_ico = fixsen_mw_indisk_ico/normalizeMilkyWay
    fixsen_mw_indisk_ico_err = fixsen_mw_indisk_ico_err/normalizeMilkyWay
    refFlux = thermalizedCO[coTransitions[coIntFluxes>0][0]-1]
    normalizeFlux = coIntFluxes[coIntFluxes>0][0]/refFlux
    # Plot the different SLEDs
    plt.plot(coLinear,thermalizedCO,lw=2,ls=':',label='Thermalized',color='k')
    f1.fill_between(harrington_co,harrington_ico+harrington_ico_err,harrington_ico-harrington_ico_err,color='k',alpha=0.2,label='Harrington+21',lw=0)
    plt.fill_between(fixsen_mw_indisk_co,fixsen_mw_indisk_ico-fixsen_mw_indisk_ico_err,fixsen_mw_indisk_ico+fixsen_mw_indisk_ico_err,color='darkviolet',alpha=0.3,label='Milky Way',lw=0)
    plt.errorbar(coTransitions[coIntFluxes>0],coIntFluxes[coIntFluxes>0]/normalizeFlux,coIntErrors[coIntFluxes>0]/normalizeFlux,marker='o',color='k',label='Observed lines')
    if len(coTransitions[coIntFluxes<0])>0:
        plt.errorbar(coTransitions[coIntFluxes<0],3*coIntErrors[coIntFluxes<0]/normalizeFlux,coIntErrors[coIntFluxes<0]/normalizeFlux,marker='o',uplims=True,color='grey',ls='none',label='Non-detections')
    plt.xlabel(r'CO transition J$_{\rm up}$')
    plt.ylabel('Velocity-integrated flux [scaled]')
    plt.legend(loc='upper left',facecolor='white',edgecolor='none')
    plt.xlim(0.5,coTransitions.max()+0.5)
    coIntFluxes[coIntFluxes<0] = 3*coIntErrors[coIntFluxes<0]
    plt.ylim(0,coIntFluxes.max()/normalizeFlux*ylimMultiplier)


# def RSGquality(filter_down,filter_up,redshift_array,nr_of_CO_lines = 20):
#     source_lines = np.zeros([len(redshift_array)])
#     source_lines_excl_low = np.zeros([len(redshift_array)])
#     source_lines_excl_high = np.zeros([len(redshift_array)])
#     SL_rest_freq = []
#     filter_down = np.array(filter_down)
#     filter_up = np.array(filter_up)
#     for i in range(nr_of_CO_lines):
#         SL_rest_freq.append((i+1)*CO10)
#     #OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205
#     #CI370 ,CI609 ,H2O211,H2O202 , 
#     # for i in [OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205]:
#     # SL_rest_freq.append(i)
#     # For each of the simulated sources in redshift_array
#     for i in range(len(redshift_array)):
#         # For each possible line that we can detect
#         for j in range(len(SL_rest_freq)):
#             # Across each filter that we target
#             for k in range(len(filter_down)):
#                 # If the redshifted line is within our filters
#                 if (SL_rest_freq[j]/(1+redshift_array[i])) > filter_down[k] and (SL_rest_freq[j]/(1+redshift_array[i])) < filter_up[k]:
#                     # Add one line to the nr. of expected lines:
#                     source_lines[i] += 1
#                     # What happens if we mis-interpret the line for an adjacent CO line
#                     freq_line = SL_rest_freq[j]/(1+redshift_array[i])
#                     # We would have the following redshift solutions instead
#                     if j > 0:
#                         z_line_low = SL_rest_freq[j-1]/freq_line -1
#                         z_line_high = -99
#                     if j < nr_of_CO_lines-1:
#                         z_line_high = SL_rest_freq[j+1]/freq_line -1
#                         z_line_low = -99
#                     # How many lines would we detect for these redshift solutions
#                     # Iterate again over the nr. of filters:
#                     for l in range(len(filter_down)):
#                         # Iterate over the number of CO lines
#                         for m in range(nr_of_CO_lines):
#                             if (SL_rest_freq[m]/(1+z_line_low)) > filter_down[l] and (SL_rest_freq[m]/(1+z_line_low)) < filter_up[l]:
#                                 source_lines_excl_low[i] += 1
#                             if (SL_rest_freq[m]/(1+z_line_high)) > filter_down[l] and (SL_rest_freq[m]/(1+z_line_high)) < filter_up[l]:
#                                 source_lines_excl_high[i] +=1
#                             if j == 0:
#                                 if (SL_rest_freq[j+1]/(1+z_line_low)) > filter_down[l] and (SL_rest_freq[j+1]/(1+z_line_low)) < filter_up[l]:
#                                     source_lines_excl_high[i] += 1
#                                     source_lines_excl_low[i] +=2
#                             if j == nr_of_CO_lines -1:
#                                 if (SL_rest_freq[j+1]/(1+z_line_high)) > filter_down[l] and (SL_rest_freq[j+1]/(1+z_line_high)) < filter_up[l]:
#                                     source_lines_excl_high[i] += 2
#                                     source_lines_excl_low[i] +=1
#     no_lines = (source_lines==0).sum()/len(source_lines)
#     one_line = (source_lines==1).sum()/len(source_lines)
#     two_lines = (source_lines>1).sum()/len(source_lines)
#     excl_lines = ((source_lines_excl_low[source_lines==1]>1) & (source_lines_excl_high[source_lines==1]>1)).sum()/len(source_lines)
#     return np.array([no_lines,one_line,two_lines,excl_lines])


# def RSGquality(filter_down,filter_up,redshift_array,nr_of_CO_lines = 20):
#     SL_rest_freq = []
#     filter_down = np.array(filter_down)
#     filter_up = np.array(filter_up)
#     for i in range(nr_of_CO_lines):
#         SL_rest_freq.append((i+1)*CO10)
#     # OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205
#     # CI370 ,CI609 ,H2O211,H2O202 , 
#     # for i in [OIII52,NIII57 ,OI63 ,OIII88 ,NII121 ,OI145 ,CII157 ,NII205]:
#     # SL_rest_freq.append(i)
#     SL_rest_freq = np.array(SL_rest_freq)
#     freq_lines = np.outer(1/(redshift_array+1),SL_rest_freq)
#     detection_table = np.zeros([len(redshift_array),len(SL_rest_freq)])
#     for i in range(len(filter_down)):
#         detection_table[(freq_lines > filter_down[i]) & (freq_lines < filter_up[i])] = 1
#     source_lines = detection_table.sum(axis=1)
#     no_lines = (source_lines==0).sum()/len(source_lines)
#     one_line = (source_lines==1).sum()/len(source_lines)
#     two_lines = (source_lines>1).sum()/len(source_lines)
#     co_line_detected = np.zeros([(source_lines==1).sum()])
#     co_index = np.arange(1,nr_of_CO_lines+1)
#     for i in range((source_lines==1).sum()):
#         co_line_detected[i] = co_index[detection_table[source_lines==1][i]==1]
#     redshift_array_up = ((co_line_detected+1)*(1+redshift_array[source_lines==1])/co_line_detected) - 1
#     co_line_detected[co_line_detected==1] = 3
#     redshift_array_down = ((co_line_detected-1)*(1+redshift_array[source_lines==1])/co_line_detected)  - 1
#     freq_lines_up = np.outer(1/(redshift_array_up+1),SL_rest_freq)
#     detection_table_up = np.zeros([len(redshift_array_up),len(SL_rest_freq)])
#     freq_lines_down = np.outer(1/(redshift_array_down+1),SL_rest_freq)
#     detection_table_down = np.zeros([len(redshift_array_down),len(SL_rest_freq)])
#     for i in range(len(filter_down)):
#         detection_table_up[(freq_lines_up > filter_down[i]) & (freq_lines_up < filter_up[i])] = 1
#         detection_table_down[(freq_lines_down > filter_down[i]) & (freq_lines_down < filter_up[i])] = 1
#     source_lines_up = detection_table_up.sum(axis=1)
#     source_lines_down = detection_table_down.sum(axis=1)
#     excl_lines = ((source_lines_up>1) & (source_lines_down > 1)).sum()/len(source_lines)
#     # excl_lines = ((source_lines_up[source_lines==1]>1)&(source_lines_down[source_lines==1]>1)).sum()/len(source_lines)
#     # freq_of_sources_with_one_line = freq_lines[source_lines==1,detection_table[source_lines==1,:]==1]
#     # redshifts_of_sources_with_one_line = redshift_array[source_lines==1]
#     # excl_lines = ((source_lines_excl_low[source_lines==1]>1) & (source_lines_excl_high[source_lines==1]>1)).sum()/len(source_lines)
#     return np.array([no_lines,one_line,two_lines,excl_lines]) #np.array([no_lines,one_line,two_lines,excl_lines])


































