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

loFreq = np.array([88.815, 100.565, 92.515, 104.265, 96.215, 107.965, 139.4, 151.15, 143.1, 154.85, 146.79999999999998, 158.54999999999998])
upFreq = np.array([92.565, 104.315, 96.265, 108.015, 99.965, 111.715, 143.15, 154.9, 146.85, 158.6, 150.54999999999998, 162.29999999999998])


RSG.RSGplot([88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29],[88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29,88.815,162.29],'Fig1_step1',z_phot=-99.0,sl_freq_obs=[-99],single_line_colour='#ffffff',multi_line_colour='#ffffff',figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)
RSG.RSGplot(loFreq,upFreq,'Fig1_step2',z_phot=-99.0,sl_freq_obs=[-99],single_line_colour='#ffffff',multi_line_colour='#ffffff',figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)
RSG.RSGplot(loFreq,upFreq,'Fig1_step3',z_phot=3.0,sl_freq_obs=[-99],single_line_colour='#ffffff',multi_line_colour='#ffffff',figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)
RSG.RSGplot(loFreq,upFreq,'Fig1_step4',z_phot=3.0,sl_freq_obs=[-99],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)



orange = '#ff9500'#(1,0.584,0)
blue =  '#007aff'  #(0,.478,1) blue
green = '#4cd964'
red = '#ff3b30'
grey = '#8e8e93'   #(142./255,142./255,147./255)



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
                # f1.plot([redshift_array[z_index],redshift_array[z_index]],[sl_freq_obs[line_choice],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff], color='k',lw=0.2,zorder=12,linestyle=':')
                if SL_vis.sum(axis=0)[z_index] == 1:
                    1+1
                    # f1.arrow(redshift_array[z_index],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff, 0,-0.3 * frequency_diff,shape='full', lw=0.5, length_includes_head=True, head_width=0.1,overhang=5,zorder=300)
                else:
                	1+1
                    # f1.arrow(redshift_array[z_index],frequency_up- frequency_diff*0.15 - line_choice*0.15*frequency_diff, 0,-0.3 * frequency_diff,shape='full', lw=0.5, length_includes_head=True, head_width=0.1,overhang=5,zorder=300)
    plt.savefig('RSG_'+str(IDname)+'.png',dpi=DPIVal)


RSGplot(loFreq,upFreq,'Fig1_step5',z_phot=3.0,sl_freq_obs=[93.463,155.772],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)
RSG.RSGplot(loFreq,upFreq,'Fig1_step6',z_phot=3.0,sl_freq_obs=[93.463,155.772],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)
# RSG.RSGplot(loFreq,upFreq,'Fig1_step7',z_phot=3.0,sl_freq_obs=[93.463,155.772],figSizeX=6,figSizeY=4,redshift_down=0,redshift_up=7,LSBUSB=True)