from pypeit_wrapper import pypeit_wrapper 

if False: 
    path_files= r"D:\ExtractSpec\2M4\251026\251026"  ###path to dir with raw files 
    path_work = r"D:\ExtractSpec\2M4\251026"  ###path to working dir 

    ljt= pypeit_wrapper(path_dir = path_files, path_work=path_work , instrument='ljt_yfosc',clean=False) ###clean = True, it will clean working dir before running pypeit 
    ljt.pre_pypeit(check_quality=False, copyfile=True) ###Do some preparation work, copyfile=True, it will copy useful raw files to working dir, but this would take more space on disk. If False, it will create links to original files, but in this case, the original files will also be modified by the procedure 
    ljt.run_pypeit( ) #run the pypeit , You can set some configs allowed for pypeit, like configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    ljt.produce_sensfunc() ##produce the sensfunc file for flux calibaration 
    ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}}) ###path_sens, path to dir containing a sensfunc file, it will be used , if no std was found  in this observation set 
    ljt.codd1d_spec(target_method='coord') ###coadd1d extracted 1d spectra 
    ljt.telluric_correction() ###Do the telluric correction 

if False:
    ###still one error, about for cycle 
    ljt= pypeit_wrapper(path_dir = r"D:\ExtractSpec\2M4\251013\251013_test\251013", path_work=r"D:\ExtractSpec\2M4\251013\251013_test2", instrument='ljt_yfosc',clean=False)
    # ljt.pre_pypeit(check_quality=False) 
    # ljt.run_pypeit( ) #configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    # ljt.produce_sensfunc()
    # ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}})
    ljt.codd1d_spec(target_method='coord') 
    ljt.telluric_correction()

if False: 
    ljt= pypeit_wrapper(path_dir = r"D:\ExtractSpec\2M4\251129\251129", path_work=r"D:\ExtractSpec\2M4\251129", instrument='ljt_yfosc',clean=False)
    # ljt.pre_pypeit(check_quality=False) 
    # ljt.run_pypeit( ) #configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    # ljt.produce_sensfunc()
    # ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}})
    # ljt.codd1d_spec(target_method='coord') 
    ljt.telluric_correction()


if False: 
    from astropy.io import fits 
    import matplotlib.pyplot as plt 
    from astropy.table import Table 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Calibrations\WaveCalib_A_0_DET01.fits")

    plt.plot( hdu[2].data['spec'][0])


    data= Table.read(r"D:\ExtractSpec\2M4\ds92.dat",format='ascii') 
    plt.plot(data['col1'][::-1]+7, data['col2'])
    plt.show() 

if False: 
    import subprocess
    import os 
    print(os.getcwd() )
    subprocess.run(['ls','-l'])


if False: 
    import matplotlib.pyplot as plt 
    from astropy.io import fits 
    hdu=fits.open(r"D:\ExtractSpec\2M4\251129\ljt_yfosc_A\Science\spec1d_ljg2m401-yf01-20251129-0263-e00-J0810+2455_yf01_20251129T192701.541.fits") 
    plt.plot(hdu[4].data['opt_wave'], hdu[4].data['opt_counts']) 


    hdu=fits.open(r"D:\ExtractSpec\2M4\251129\ljt_yfosc_A\Science_ljg2m401-yf01-20251129-0271-e00-HILT600\spec1d_ljg2m401-yf01-20251129-0264-e00-J0810+2455_yf01_20251129T195231.737.fits") 
    plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts']) 
    plt.show() 

    # hdu=fits.open(r"D:\ExtractSpec\2M4\251129\ljt_yfosc_A\coadd1d_ljg2m401-yf01-20251129-0271-e00-HILT600\J0810+2455_spat1485.fits") 
    # ind =hdu[1].data['wave']> 0 
    # plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind]) 
    # plt.show() 

if False: 
    import matplotlib.pyplot as plt 
    from astropy.io import fits 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251129\ljt_yfosc_A\telluric_ljg2m401-yf01-20251129-0271-e00-HILT600\J0810+2455_spat0814_tellcorr.fits")
    ind = hdu[1].data['wave'] > 0 
    plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind]) 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251129\ljt_yfosc_A\telluric_ljg2m401-yf01-20251129-0271-e00-HILT600\J0810+2455_spat0814.fits") 
    ind = hdu[1].data['wave'] > 0 
    plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind])
    plt.show() 
